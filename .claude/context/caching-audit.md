# Caching audit (v0.6.0)

Every `@lazyproperty` and every hand-rolled cache in `src/pptx/`, put in one bucket and judged
sound or fixed. Audited 2026-10-15 on branch `v0.6.0`. At branch open there were 203 decorated
properties in 44 files. The "204 in 45 files" on the card came from a grep that also counted the
decorator's own docstring in `util.py`. The fixes below turned 13 of them into plain properties
or validated caches, which leaves 190.

The bar, from the v0.6.0 card: no cached value may go stale after a mutation the API allows.
Raw XML edits count when the API's own docs or a long-standing idiom use them, such as
`sp.getparent().remove(sp)` to delete a shape.

**The held-proxy rule.** Holding a proxy whose *own* element has been removed is outside the bar.
For example, keep `legend = chart.legend`, then set `chart.has_legend = False`: `legend` now
wraps a detached element, as any proxy would. What is inside the bar is a proxy whose own
element is still in the tree but which hands back a cached child or value that is stale. That is
the case every fix below addresses.

## Findings fixed

Each fix landed with a test that failed before it: commit `5cd3c8f`, `63ab8e4` for the relationship
row, and L1 and L2 before the audit.

| Cache | Bucket | Stale after | Fix | Test |
|---|---|---|---|---|
| `_BaseShapes` name/id index (L1) | 3 | `shape.name = …`, a raw-XML delete or id change | validate on hit | `tests/shapes/test_shapetree.py` `Describe_BaseShapes::it_finds_a_renamed_shape_by_its_new_name` and two more |
| `ImagePart.sha1`, `MediaPart.sha1` (L2) | 3 | `part.blob = …` | `Part._blob_caches` cleared by the blob setter | `tests/parts/test_image.py`, `tests/parts/test_media.py` `it_recomputes_its_sha1_after_its_blob_is_replaced` |
| `MajorGridlines.format` | 2 | `axis.has_major_gridlines = False` | plain property | `tests/chart/test_axis.py` `DescribeMajorGridlines::it_adds_the_gridlines_back_when_formatted_after_they_are_removed` |
| `LineFormat.color` | 2 | `line.fill.background()` (or any fill change) | plain property | `tests/dml/test_line.py` `it_makes_the_line_solid_again_when_its_color_is_set_after_a_fill_change` |
| `Font.color` | 2 | `font.fill.background()`; chart, axis and legend fonts are cached, so it bit there | plain property | `tests/text/test_text.py` `it_makes_the_font_solid_again_…` |
| `ShadowFormat.color` | 2 | `shadow.inherit = True` | plain property | `tests/dml/test_effect.py` `it_adds_a_shadow_again_when_its_color_is_set_after_inheritance_is_restored` |
| `DataLabel.font` | 2 | `has_text_frame = True` or `text_frame` (removes `c:txPr`) | plain property | `tests/chart/test_datalabel.py` `it_writes_its_font_after_a_text_frame_is_added` |
| `ActionSetting._slide_index` | 3 | `prs.slides.move()` / `delete()` | plain property | `tests/test_action.py` `it_finds_the_next_slide_after_the_slides_are_reordered` |
| `FillFormat._fill` (hand-rolled) | 3 | a fill change through a second proxy for the same shape | validate on use: rebuild when the wrapped element has left `_xPr` | `tests/dml/test_fill.py` `it_sees_a_fill_type_changed_through_another_fill_format` and three more |
| `ColorFormat._color` (hand-rolled) | 3 | a color change through a second proxy | validate on use, as for fill | `tests/dml/test_color.py` `it_sees_a_color_type_changed_through_another_color_format` and two more |
| `AdjustmentCollection._adjustments_` (hand-rolled) | 3 | a write through a second collection; this one then overwrote it | read the guides on each access | `tests/shapes/test_autoshape.py` `it_reads_an_adjustment_written_through_another_collection`, `it_keeps_…_when_it_writes` |
| `_Relationship.target_ref`, `target_partname` | 4 | a save, then the first `prs.slides` (which renames slide parts to follow slide order), then a save: the second save wrote the old names, so the slides came back in the wrong order | plain properties | `tests/opc/test_package.py` `Describe_Relationship::it_names_its_target_by_the_partname_the_target_has_now`; `tests/test_roundtrip.py` `it_keeps_the_slide_order_when_saved_before_and_after_listing_the_slides` |
| `_base_placeholder` (5 classes) | 4 | the layout or master placeholder deleted or re-indexed while the placeholder object is held | validate on hit: base still in its tree, both `p:ph` keep the `idx`/`type` they matched by | `tests/shapes/test_placeholder.py` `Describe_InheritsDimensions_base_placeholder` (3 new) |

"Second proxy" is ordinary use. `slide.shapes[0]` builds a new shape object on every call, and so
does each pass of `for shape in slide.shapes`. Each object has its own cached `fill`, `line` and
`adjustments`.

**Cost.** Over the corpus walk, calls into `pptx` rose about 0.4% and wall time 1–3% (three
interleaved runs). Most of the cost is paid back by choice-group getters, which now find a member
with one `iterchildren()` scan instead of a loop. The work-count gate now counts total calls
rather than cProfile's primitive calls. The old count rose 4.4% for the same change, because
un-nesting `lazyproperty.__get__` calls made them count (see `performance.md`).

## Bucket 1: fixed-element proxies (99, sound)

**Rule.** The property wraps `self._element`, or a child that no API removes or replaces. The
proxy reads the XML on every access, so caching it caches nothing that can go stale. Children
fetched with `get_or_add_*` were checked against every `_remove_*`, `get_or_change_to_*` and
`remove()` call in `src/pptx/`.

| Module | Properties | Why the child stays |
|---|---|---|
| `slide.py` (15) | `background`, `placeholders`, `shapes`, `header_footer` (each slide type), `slide_layouts`, `_Background.fill` | `cSld`/`spTree` are required children. `bgPr` replaces a `bgRef` only on first access; `follow_master_background` is read-only. `sldLayoutIdLst` is never removed. |
| `presentation.py` (2) | `slide_masters`, `slides` | `sldMasterIdLst`/`sldIdLst` are never removed. `slides` also renames slide parts once, on first access; part names need not follow slide order, so later moves need no rename. |
| `parts/slide.py` (6), `parts/presentation.py` (1), `parts/chart.py` (2) | `slide`, `slide_layout`, `slide_master`, `notes_slide` (`NotesSlidePart`), `notes_master` (`NotesMasterPart`), `handout_master`, `presentation`, `chart`, `chart_workbook` | wrap the part's root element. `XmlPart._element` is assigned only in `__init__`. |
| `shapes/base.py` (6), `autoshape.py` (3), `picture.py` (3), `connector.py` (1), `group.py` (2) | `click_action`, `shadow`, `glow`, `reflection`, `soft_edge`, `three_d`, `adjustments`, `fill`, `line`, `media_format`, `shapes`; `GroupShape.click_action` raises every time | `cNvPr`, `spPr`/`grpSpPr` and `prstGeom` are never removed. A graphic frame resolves its effect element lazily (`_LazyChild`). `adjustments` itself no longer snapshots (above). |
| `table.py` (9) | `columns`, `rows`, `_Cell.border_*` (6), `_Cell.fill` | `tblGrid` is required; `tcPr` and its `ln*` children are never removed. A deleted row or column removes the cell's own element (held-proxy rule). |
| `text/text.py` (2) | `Font.fill`, `_Run.hyperlink` | `rPr` is never removed. The fill object itself is validated (above). |
| `action.py` (1) | `ActionSetting.hyperlink` | `Hyperlink` reads `hlinkClick`/`hlinkHover` on each access. |
| `dml/fill.py` (5), `line.py` (1), `chtfmt.py` (2), `threed.py` (1) | `_GradFill.gradient_stops`, `_PattFill.back_color`/`fore_color`, `_SolidFill.fore_color`, `_GradientStop.color`, `LineFormat.fill`, `ChartFormat.fill`/`line`, `ThreeDFormat.scene` | `gsLst`, `bgClr`, `fgClr`, `ln` and chart `spPr` are never removed. `c:spPr` is removed only from a `c:dLbl`, which no `ChartFormat` wraps. A replaced `gradFill`/`pattFill`/`solidFill` gets a new fill object (above). |
| `chart/*.py` (37) | `format` on axes, titles, drop/high-low/series lines, error bars, trendlines, legend, plot area, surfaces, series and points; `font` on chart, tick labels, legend and data labels; `plots`, `plot_area`, `series`, `categories`, `points`, `marker`, `data_label(s)`, `error_bars`, `trendlines`, `tick_labels`, `major_gridlines`, up/down bar formats | `txPr` is never removed from a chart, axis, legend or `dLbls`. `marker`, `dPt`, `upBars`/`downBars` and series `dLbls` are never removed. `plot.has_data_labels = False` removes the plot's `dLbls`, but `plot.data_labels` is not cached. |

## Bucket 2: removable-child proxies (5, all fixed)

`MajorGridlines.format`, `LineFormat.color`, `Font.color`, `ShadowFormat.color` and
`DataLabel.font`. See the findings table. Each cached a proxy over a child that another
documented call removes.

## Bucket 3: snapshots (10 kept, sound)

| Cache | Why sound |
|---|---|
| `Image.content_type`, `dpi`, `ext`, `sha1`, `size`, `_pil_props` | `Image` is an immutable value object built from one bytes value. |
| `Video.sha1`, `Audio.sha1` (`media.py`) | immutable value objects, as for `Image`. |
| `ImagePart.sha1`, `MediaPart.sha1` | cleared when the blob is replaced (L2); a lazy blob's bytes are CRC- and size-checked on read. |

The remaining bucket 3 snapshots were the ones fixed above (`_slide_index`, and the hand-rolled
fill, color and adjustment state).

## Bucket 4: part-graph lookups (23, sound)

**Rule.** These are stale only if the relationship is dropped or re-targeted. `drop_rel()` is
called in exactly these places:
- hyperlinks (`action.py`, `text/text.py`);
- embedded fonts (`fonts.py`);
- shape deletion (`shapetree.py`);
- slide deletion and layout removal (`slide.py`);
- SmartArt (`smartart.py`);
- the load-time comment-authors repair, which runs before any user access (`package.py`).

None of those drops a relationship that a cached lookup below follows. `_Relationship` never
reassigns its target. A part's *name* can change, though: `rename_slide_parts()` renames slide
parts on the first `prs.slides`. That is what made `target_ref` stale (fixed above). `Part._rels`
keeps the base URI it was built with, which is sound because a renamed slide stays in
`/ppt/slides/`.

| Cache | Notes |
|---|---|
| `Package.core_properties`, `custom_properties`, `comment_authors` | created if absent, never dropped. |
| `Package._image_parts`, `_media_parts` | stateless; iterate the live relationship graph. |
| `PresentationPart.notes_master`, `notes_master_part`; `NotesSlidePart.notes_master`; `SlidePart.notes_slide` | no API removes a notes master or a notes slide. |
| `ActionSetting._slide`, `_slides` | the shape's own slide and the presentation's slide collection, both fixed. |
| `Part.content_type`, `package`, `rels`, `_rels`; `OpcPackage._rels`; `_RelatableMixin._rels` (abstract); `_Relationships._rels`; `_Relationship.is_external`, `target_mode`, `reltype`, `rId`, `target_part` | fields set once and never reassigned (`_content_type`, `_package`, `_target`). |

## Bucket 5: transient internals (58, sound by lifetime)

**Rule.** The owning object lives for one call or one build, so nothing can change under it.
- `_PackageLoader._content_types`, `_package_reader`, `_parts`, `_xml_rels`: one load.
- `PackageReader._blob_reader`, `_ZipPkgReader._member_names`, `_ZipPkgWriter._zipf`, and
  `_ContentTypesItem._xml`/`_defaults_and_overrides`: one load or one save.
- `_MoviePicElementCreator` (5), `_AudioPicElementCreator` (5), `_OleObjectElementCreator` (11):
  one `add_movie`/`add_audio`/`add_ole_object` call.
- `TcRange` (9, `oxml/table.py`): one merge or split.
- `FreeformBuilder._drawing_operations`: the builder's own work list.
- `CategoryChartData`, `XyChartData` and `BubbleChartData` `._workbook_writer`: the writer reads
  the chart data when it writes.
- `text/fonts.py` (5): one font-file read.
- `xmlchemy` method-name properties (10): computed when element classes are built.

## Hand-rolled caches outside `@lazyproperty`

| Cache | Verdict |
|---|---|
| Shape name/id indexes; `_found_base` (placeholders); `FillFormat._fill_obj`; `ColorFormat._color_obj` | fixed and validated, as above. |
| `qn()` (`functools.lru_cache`), the thread-local compiled-XPath cache, enum `_XML_VALUE_MAPS`, `AutoShapeType._instances`, choice-group member tags | sound: pure functions of constants. |
| `LazyXmlPart` parse-once | sound: once parsed, the tree *is* the part's state and `blob` serializes it. |
| `_ZipPkgReader._archive` / `ZipMember` (lazy blobs) | sound: CRC and size are checked on every read; a changed or missing source raises `PackageError`. |
| `_PartCopier._taken` | transient: one slide import. |

## New caches

None added. The cProfile top 20 of the corpus walk is XML parsing, serialization and element
accessors (`parse_xml`, `xpath`, `get_child_element`, `lazyproperty.__get__`). None of them is a
derived collection recomputed in a loop, which is the only case the card admits.

## Open threads (not defects in a cache)

- `DataLabel.font` after a text frame is added now writes `c:txPr` beside `c:tx`. A fresh
  `point.data_label` always did that. A comment in `datalabel.py` says the pair stops PowerPoint
  saving a *bubble* chart. On PowerPoint 16 (2026-10-15, via COM) such a bubble chart opened
  without repair and saved, so the comment describes an older PowerPoint, if any.
- A placeholder whose search finds no base searches again on each access, because
  `layout.shapes.add_placeholder()` can add a match later. This is rare in real decks.
- The `follow_master_background` docstring describes a setter that does not exist.
