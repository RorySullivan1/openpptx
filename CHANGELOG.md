# Changelog

All notable changes to openpptx are recorded in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). From 1.0.0 the
project follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html). What the public API
is, what counts as a breaking change and how deprecation works are set out in
[`docs/stability.rst`](https://rorysullivan1.github.io/openpptx/stability.html).

1.0.0 is the first release on PyPI. Earlier versions were never published there: they were
tagged in this repository under the name `pypptx`, imported as `pptx`. Module paths in their
entries use the current `openpptx` names; the 1.0.0 section lists the renames.

## [Unreleased]

### Added

- Each release on PyPI also gets a GitHub Release, with its notes from this file and the same
  sdist and wheel attached.

## [1.0.0] - 2026-10-18

The first stable release, and the first on PyPI: `pip install openpptx`. From here on the public
API follows Semantic Versioning. It was preceded by `1.0.0rc1` on the same day, whose code is the
same.

### Added

- A root `LICENSE`: the MIT notice for openpptx, followed by the copyright and permission notice
  of python-pptx, which this code is derived from. The sdist and the wheel both include it, and
  the package metadata declares `License-Expression: MIT`.
- PyPI metadata: project URLs (homepage, documentation, source, issues), classifiers (Python 3.9
  to 3.13, `Typing :: Typed`), keywords, authors, and the README as the project page.
- `docs/stability.rst` defines the public API: `Presentation`, `__version__`, every module in the
  API reference, and `openpptx.exc`. `openpptx.oxml`, `openpptx.opc`, `openpptx.parts`, a listed
  set of implementation modules and any underscored name are internal.
- The same page states what counts as a breaking change, the exception contract, and the
  deprecation policy: a deprecated name warns from the minor release that deprecates it and stays
  for the rest of the 1.x line.
- A snapshot test records every public name, so a change to the public API cannot happen by
  accident.
- The API reference now covers `openpptx.custom_show`, `openpptx.theme`, `openpptx.fonts` and
  `openpptx.smartart`, plus the part-layer classes users receive: `CorePropertiesPart`,
  `CustomPropertiesPart`, `TagsPart` and `Image`.
- Guides for slides, shapes, text, charts, effects and themes, and a migration guide for
  python-pptx users. Every code sample in them runs in the test suite. The documentation is
  published at https://rorysullivan1.github.io/openpptx/.

### Changed

- **Breaking:** the distribution is renamed from `pypptx` to `openpptx`. The PyPI name `pypptx`
  belongs to an unrelated project, so `pip install pypptx` does not install this library.
- **Breaking:** the import package is renamed from `pptx` to `openpptx`: write
  `from openpptx import Presentation`. No compatibility shim is provided. openpptx and
  python-pptx can now be installed side by side.
- **Breaking:** the base exception `PyPptxError` is renamed to `OpenPptxError`, with no alias.
- **Breaking:** `lazyproperty` moved from `openpptx.util` to the internal `openpptx._util`.
- **Breaking:** helpers that were public by accident now have a leading underscore:
  `PlotFactory`, `PlotTypeInspector`, `BaseShapeFactory`, `SlideShapeFactory`,
  `LAYOUT_PLACEHOLDER_BASE_TYPES`, `Subshape`, the `DrawingOperation` type aliases in
  `openpptx.shapes.freeform`, and `TextFinder`, `TextReplacer`, `compile_pattern`,
  `iter_paragraph_chars` and `iter_slide_text_frames` in `openpptx.text.search`.
- **Breaking:** an index out of range on `prs.slides`, `slide_layouts` or `slide_masters` raises
  `IndexError`, as on every other collection and in python-pptx, instead of `SlideError`.
- Enum `from_xml()`, `to_xml()` and `validate()` raise `InvalidValueError` instead of a bare
  `ValueError`. `InvalidValueError` subclasses `ValueError`, so existing handlers still catch it.
- New presentations no longer carry python-pptx's core properties ("generated using python-pptx",
  last modified by "Steve Canny"); the default template now names openpptx.
- Building from source needs `setuptools>=77`, for the PEP 639 licence fields.

### Removed

- **Breaking:** the `openpptx.exceptions` alias of `openpptx.exc`, kept from python-pptx. Import
  from `openpptx.exc`.
- **Breaking:** the top-level `openpptx` package no longer exposes `HandoutMasterPart`,
  `NotesMasterPart`, `NotesSlidePart` or the content-type-to-part-class map. Its public names are
  `Presentation` and `__version__`.

### Fixed

- Enum `validate()` no longer leaks a `TypeError` on Python versions before 3.12; it raises
  `InvalidValueError`.
- `SlideShapes.add_chart()` is annotated to return the `GraphicFrame` it returns, not a `Chart`.
- `Camera.field_of_view` read and wrote the angle 60,000 times too small or too large:
  setting 45 wrote `fov="0"`, and a 45-degree camera read back as 0.00075. It now reads and writes
  degrees.
- `TextFrame.fit_text()` crashed with a `TypeError` when one word was wider than the shape. A size
  at which a word does not fit now counts as too big, and text that fits at no size raises
  `ShapeError` instead of failing inside the fitter.
- A hyperlink in a chart title, an axis title or a data label raised `AttributeError`. It raises
  `ChartError`, which says openpptx cannot read or set one there.
- `Picture.image_width` and `image_height` on a linked picture raise `ShapeError` ("no embedded
  image"), as `Picture.image` does, instead of a `KeyError`.
- Type annotations: lengths such as `ShadowFormat.blur_radius`, `_Paragraph.indent`,
  `Font.spacing` and the `Bevel` and `ThreeDFormat` sizes are typed `Length`, which they always
  were at run time, and `openpptx.dml.threed` is annotated throughout. Pyright reports no return-type or argument-type errors in the package.

## [0.7.1] - 2026-10-16

### Changed

- In regex mode, `^` matches only at the start of a paragraph, not after every line break or
  field. `\b` and lookbehind at the start of a run segment see the text before it.

### Fixed

- A `\v` or `\n` in the replacement text now inserts a line break (`a:br`). Before, `\n` went into
  the text as a raw line feed and `\v` was written as `_x000B_`. The break and each new line take
  the formatting of the first run the match touches.
- A replacement template with a bad group number or an unknown group name raises
  `InvalidValueError` before anything is searched. Before, an unknown group name escaped as a bare
  `IndexError`, and only on a deck that had a match.
- A `count` that is not an `int`, or is a `bool`, raises `InvalidTypeError` instead of a bare
  `TypeError` or `ValueError`.
- `TextMatch` objects from two searches of the same text compare equal, and a match with a
  `shape` can be hashed.
- Removing a run that refers to one relationship twice (`hlinkClick` and `hlinkMouseOver`) no
  longer leaves the relationship orphaned. Any relationship a removed run referred to is dropped
  once nothing else in the part refers to it.

## [0.7.0] - 2026-10-16

### Added

- `TextFrame.replace(old, new, *, count=None, regex=False)` and
  `TextFrame.find_all(pattern, *, regex=False)`, and the same pair on `_Paragraph`. A match may
  span runs. It never crosses a paragraph, a line break or a field, and field text is never
  changed.
- Replaced text takes the formatting of the first run the match touches. The last run keeps its
  remaining text and its own formatting, runs inside the match are removed, and a run left empty
  is removed.
- `Slide.find_text()` / `Slide.replace_text()` and `Presentation.find_text()` /
  `Presentation.replace_text()`, with the same arguments. They cover every shape with text in
  shape-tree order, group members, table cells row by row, and the notes slide if one exists.
- The deck-wide methods never create a notes slide, and leave layouts, masters, charts, SmartArt
  and comments alone.
- Patterns: a `str` is literal unless `regex=True`. A compiled `re.Pattern` implies regex and
  keeps its flags. In regex mode `new` is a template (`\1`, `\g<name>`).
- An empty literal pattern raises `InvalidValueError`, and zero-width regex matches are skipped.
- `count` applies across the whole frame, slide or presentation in document order. `0` replaces
  nothing, and a negative count raises `InvalidValueError`.
- `openpptx.text.search.TextMatch`, an immutable match with `paragraph`, `paragraph_index`,
  `start`, `end`, `text`, `runs` and `shape`. Offsets index `paragraph.text`.
- `TextFrame.iter_runs()`, and `iter_chars()` on `TextFrame` and `_Paragraph`, which yields a
  `TextChar` per character.
- `merge_runs()` on `TextFrame` and `_Paragraph` merges adjacent runs with the same formatting,
  ignoring the proofing state PowerPoint stores on runs (`dirty`, `err`, `smtClean`, `smtId`). It
  is opt-in and returns the number of runs removed.
- When a removed run carries a hyperlink, its relationship is dropped only if nothing else refers
  to it.

### Changed

- `examples/batch_process.py` uses `Presentation.replace_text()`, so it also replaces words split
  across runs.

## [0.6.0] - 2026-10-16

### Changed

- A deck opened from a path leaves its images, media, fonts and other binary parts in the file
  until they are used. A deck with 100 images holds 356 KiB after opening instead of 5,169 KiB.
  A deck opened from a stream, or from a directory, is still read in full.
- No file handle is kept open after loading. The source file must stay unchanged until the
  presentation is saved; a read from a changed or removed source raises `PackageError`.
- **Breaking:** `prs.save(open("deck.pptx", "wb"))` onto the deck's own source file now fails
  with `PackageError` and leaves the file truncated, because opening it for writing empties it
  before its parts are read. `prs.save("deck.pptx")` works.
- Saving a deck opened from a path is slightly slower (about 0.4 ms per save to reopen the
  source).
- Adding a picture or movie to a loaded deck only reads existing images or media of the same
  size when checking for a duplicate.

### Fixed

- On Windows, the source file stayed locked until garbage collection. It is now closed when
  loading ends.
- Saving, then listing `prs.slides` for the first time, then saving again could reverse the slide
  order.
- `get_by_name()`, `get_by_id()` and `in` on a shape collection gave stale results after a shape
  was renamed or its element was removed from the XML.
- Replacing an image or media part's bytes did not update its SHA-1, so a later `add_picture()`
  could match the old image.
- `MajorGridlines.format`, `LineFormat.color`, `Font.color`, `ShadowFormat.color` and
  `DataLabel.font` wrote to a detached element after a call removed their XML (for example
  `has_major_gridlines = False`, `fill.background()` or `shadow.inherit = True`).
- A next-slide or previous-slide click action pointed at the wrong slide after `slides.move()`.
- Two objects for the same shape (each `slide.shapes[0]` builds a new one) could lose or overwrite
  each other's fill, colour or adjustment changes.
- A placeholder held while its layout placeholder was deleted or re-indexed kept using the old
  one.

## [0.5.1] - 2026-10-15

### Added

- `GlowFormat.color`, a `ColorFormat` for the glow colour.

### Fixed

- PowerPoint refused decks with a glow, because the glow had no colour. A glow set with only
  `radius` now gets PowerPoint's default, theme colour `accent1` at 40% opacity.
- PowerPoint refused decks with a shadow set without a colour (`blur_radius`, `distance`,
  `direction`, `alignment` or `rotate_with_shape` alone). Such a shadow now defaults to black at
  40% opacity, the colour of PowerPoint's "Outer Offset" preset.
- PowerPoint refused decks with legacy comments, because the comment authors part was related from
  the package instead of the presentation. Decks written by 0.5.0 or earlier are repaired when
  loaded.
- PowerPoint refused decks with chartex charts, because new charts had no chart-style or
  colour-style part. Each new chart now gets PowerPoint's own style for its type, and chartex
  charts written by 0.5.0 get theirs when the deck is loaded. The chart XML itself is not
  rewritten.

## [0.5.0] - 2026-10-13

### Added

- `Slide.transition`, `SlideLayout.transition` and `SlideMaster.transition` return a read-only
  `SlideTransition` with `type` (`PP_TRANSITION_TYPE`, including the PowerPoint 2010 effects and
  Morph), `speed` (`PP_TRANSITION_SPEED`), `duration`, `advance_on_click`, `advance_after`,
  `direction`, `has_sound` and `preset`.
- A transition wrapped in `mc:AlternateContent` reads the PowerPoint 2010 or Morph form where
  there is one, and the fallback otherwise. Each element reports what it stores; inheritance from
  layout or master is not resolved.
- `Slide.animations` lists `Animation` objects in play order, main sequence first, then triggered
  sequences.
- Each `Animation` has `shape_id`, `shape`, `preset_class` (`PP_ANIMATION_CLASS`), `preset_id`,
  `preset_subtype`, `trigger` (`MSO_ANIMATION_TRIGGER`), `trigger_shape`, `trigger_shape_id`,
  `delay`, `duration` and `paragraphs`.
- `Animation.effect_type` names the effect (`MSO_ANIMATION_EFFECT`) for entrance and exit preset
  IDs 1 to 31, and is `None` for other IDs.
- Reading transitions and animations never changes the XML, and malformed timing markup reads as
  `None` rather than raising.
- `SlideLayouts.add_slide_layout(name, *, blank=False)` adds a layout the way PowerPoint's Insert
  Layout does: a title plus date, footer and slide-number placeholders inherited from the master.
- `LayoutShapes.add_placeholder()` adds a placeholder to a layout and returns a
  `LayoutPlaceholder`.
- `SlideLayouts.duplicate(slide_layout, name=None)` copies a layout, named "1_…", "2_…" as
  PowerPoint does.
- `Presentation.handout_master` returns a read-only `HandoutMaster`, or `None` when the deck has
  none.
- Examples `custom_layouts.py` and `read_animations.py`.

### Changed

- Reading is faster: generated child lookups are about 40% faster and placeholder inheritance
  about 3 times faster, so reading a set of real PowerPoint decks takes about 45% less time.
- Enum lookups from XML values use a dictionary instead of scanning every member.

### Fixed

- Slide master and slide layout ids are allocated in the range the specification requires
  (2147483648 and up). `import_slide` now gives imported masters and layouts valid ids, and drops
  the source master's stale layout entries.

## [0.4.0] - 2026-10-01

### Added

- `InvalidPackageError`, a `PackageError` raised for a file or stream that is not a readable zip,
  a corrupt member, a missing `[Content_Types].xml` or no main document part. A missing path still
  raises `PackageNotFoundError`.
- `InvalidValueError` and `InvalidTypeError`, subclasses of the base exception (then
  `PyPptxError`) and of `ValueError` and `TypeError`. They replace the bare raises reachable from
  the API, including property setters, so `except ValueError` and `except TypeError` keep working.
- `UnsupportedEffectError`, raised by an effect property on a shape that has nowhere to hold the
  effect. It is a `ShapeError` and also a `NotImplementedError` and an `AttributeError`, so
  `hasattr()` stays `False`.
- `GraphicFrame.shadow`, `glow`, `reflection` and `soft_edge` work on tables and charts. Other
  graphic frames raise `UnsupportedEffectError`.

### Changed

- `ShapeError`, `SlideError`, `ChartError` and `TableError` now also subclass `ValueError`.
- `ShapeRange`, placeholder-only and freeform-only access raise `ShapeError`, and data-label
  leader lines and workbook column references raise `ChartError`, instead of a bare `ValueError`.
- An existing file that cannot be read raises `PermissionError` instead of
  `PackageNotFoundError`.

### Fixed

- Internal hyperlinks to a fragment (such as `#_ftn1`, a link to a footnote) were dropped on load.
  They are kept, saved as internal, and stay internal when the slide is duplicated.
- A file that is not a valid zip raised `PackageNotFoundError` ("Package not found") or a raw
  `zipfile.BadZipFile`. It now raises `InvalidPackageError`.
- A failed open no longer prints an `AttributeError` to stderr when the reader is garbage
  collected.
- `shape_type` raised `NotImplementedError` for a shape with no geometry. It now returns
  `MSO_SHAPE_TYPE.AUTO_SHAPE`.
- Glow, reflection, soft edge and 3D on groups and graphic frames crashed with `AttributeError`.
- Setting an integer property to `True` or `False` wrote "True" into the XML; it now raises
  `InvalidTypeError`.
- Simple-type values: NaN and infinity were accepted, angles could overflow, a positive fixed
  angle could be written as the out-of-range 21600000, and a bad universal measure raised
  `KeyError`.

## [0.3.2] - 2026-09-30

### Added

- An HTML API reference built with Sphinx from the docstrings (`docs/`, `docs` extra). Every
  public class, property and method has a docstring.
- `BaseShape.tags`: customer data tags on a shape, the same mapping as `Slide.tags`, stored the
  way PowerPoint stores them. Duplicating, removing or importing a shape carries its tags along.
- `add_chart()` creates all 13 `XL_CHART_TYPE.THREE_D_*` chart types, which raised
  `NotImplementedError` before. New 3D charts get PowerPoint's default camera, floor and walls, so
  `Chart.view_3d`, `Chart.floor`, `Chart.side_wall` and `Chart.back_wall` act on a real 3D plot.
- Example `chart_3d_view.py`.

### Changed

- `Slide.tags` is found through the slide's own tag reference, as PowerPoint reads it. Slide tags
  written by earlier versions still read.

### Fixed

- A duplicated or imported slide kept a reference to tags it did not copy.
- Reading a standard-grouping 3D column chart raised `KeyError`; it now reads as
  `THREE_D_COLUMN`.

## [0.3.1] - 2026-09-27

### Added

- Examples `chart_trendlines_error_bars.py`, `custom_slide_master_walk.py` and
  `picture_effects.py`. Each writes a deck, reopens it and asserts what it wrote.
- `add_chart_secondary_axis.py` and `comments_and_metadata.py` now reopen their output and assert
  the round trip.

## [0.3.0] - 2026-09-26

### Added

- `SlideMaster.text_styles` (`title`, `body`, `other`, indexed by zero-based level) and
  `Presentation.default_text_style`, each level with `alignment`, `indent`, `margin_left`,
  `line_spacing`, `space_before`, `space_after` and `font`.
- `Theme.fill_styles`, `Theme.line_styles` and `Theme.background_fill_styles`, read-only, and
  `MSO_THEME_COLOR.PLACEHOLDER` for the placeholder colour (`phClr`) those styles use.
- `SlideMaster.apply_theme(source)` replaces a master's theme with one from a `Presentation`, a
  `SlideMaster`, or a `.thmx`, `.pptx` or `.potx` file.
- `FreeformBuilder.add_cubic_bezier()`, `add_quadratic_bezier()` and `add_arc()`.
- `LineFormat.cap_style` (`MSO_LINE_CAP_STYLE`), `LineFormat.join_style`
  (`MSO_LINE_JOIN_STYLE`) and `LineFormat.miter_limit`.
- `FillFormat.picture(image)` and `FillFormat.tile()`, for stretched or tiled picture fills.
- `FillFormat.gradient_type` (`MSO_GRADIENT_TYPE`: linear, radial, rectangular, path) and
  `FillFormat.gradient_fill_to_rect`.
- Table `rows.add()`, `columns.add()`, `rows.remove()` and `columns.remove()`, which adjust
  merged cells across the edit, and `_Cell.text_direction` (`MSO_TEXT_VERTICAL_TYPE`).
- `TextFrame.font_scale` and `TextFrame.line_spacing_reduction`, read-only autofit readouts.
- `Presentation.notes_width` and `Presentation.notes_height`.
- `Presentation.custom_shows`, a collection of `CustomShow` objects.
- `Presentation.slide_show_settings`, with `show_type` (`PP_SLIDE_SHOW_TYPE`), loop, narration,
  animation, timings, pen colour and slide range.
- `Presentation.table_styles`, a read-only mapping of table-style id to name, and
  `Presentation.embedded_fonts`, with `remove()` for each font.
- SmartArt: `GraphicFrame.has_smartart` and `GraphicFrame.smartart`, a `SmartArt` with `nodes`
  and `iter_nodes()`. Each `SmartArtNode` has `text` (writable), `level`, `children` and
  `model_id`.
- Chartex (Office 2016) charts: `GraphicFrame.has_chartex` and `GraphicFrame.chartex` read
  them, with new `XL_CHART_TYPE` members `WATERFALL`, `HISTOGRAM`, `PARETO`, `BOX_WHISKER`,
  `TREEMAP`, `SUNBURST`, `FUNNEL` and `REGION_MAP`.
- `add_chart()` creates waterfall, histogram, box and whisker, treemap, sunburst and funnel
  charts. Pareto and region map charts can only be read.
- `Chart.has_data_table` and `Chart.data_table`, a `DataTable` under a classic chart's plot.
- `SlideShapes.add_audio()` adds an audio clip, with MP3, WAV and M4A support.
- `trim_start`, `trim_end`, `fade_in` and `fade_out` on movies and audio.
- `AlternateContentShape`, a read-only shape for 3D models, zooms and equations, with
  `content_kind` and `has_fallback`. `MSO_SHAPE_TYPE.MODEL_3D` is the shape type of a 3D model.
- Example `batch_process.py`, which processes a folder of decks in parallel processes.

### Changed

- Shapes that PowerPoint wraps in `mc:AlternateContent` (chartex charts, 3D models, zooms,
  equations) now appear in `slide.shapes`, so shape counts and indexes change for decks that
  contain them.
- A chartex frame reports `shape_type` `CHART` but `has_chart` `False`; its `.chart` raises
  `ShapeError`.
- A SmartArt frame reports `shape_type` `MSO_SHAPE_TYPE.SMART_ART`. The old name `IGX_GRAPHIC`
  still works.
- Presentation-level parts, SmartArt and chartex charts that the API does not touch are saved
  byte for byte.
- Processing a text-heavy deck is about 39% faster.

### Fixed

- `PP_MEDIA_TYPE.SOUND` is 2. It was an alias of `OTHER`, so audio reported `OTHER`.
- Setting a negative (hanging) paragraph indent raised `ValueError`.
- Reading `theme_color` of a placeholder colour (`phClr`) raised `ValueError`.

## [0.2.0] - 2026-05-16

### Changed

- The README feature list names everything that shipped in 0.1.0, including pattern line fills,
  callouts, movies, z-order, visibility and lock-aspect control, computed slide numbers, custom
  document properties, shadow-colour transparency and the wider set of chart types. This release
  changed documentation only; the package version stayed 0.1.0.

## [0.1.0] - 2026-05-16

### Added

- First alpha release of `pypptx`, a pure-Python library for reading and writing `.pptx` files.
- `MSO_BEVEL_PRESET` for `Bevel.preset`, and `MSO_SHADOW_TYPE` for `ShadowFormat.shadow_type`.
- `XL_DISPLAY_BLANKS_AS` for `Chart.display_blanks_as`.
- Read-only `grouping` on plots (`XL_GROUPING`) and `BarPlot.bar_direction`
  (`XL_BAR_DIRECTION`).

### Changed

- `Bevel.preset`, `ShadowFormat.shadow_type` and `Chart.display_blanks_as` return enum members
  instead of strings. Their setters still accept the old strings.

[Unreleased]: https://github.com/RorySullivan1/openpptx/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/RorySullivan1/openpptx/compare/v0.7.1...v1.0.0
[0.7.1]: https://github.com/RorySullivan1/openpptx/compare/0.7.0...v0.7.1
[0.7.0]: https://github.com/RorySullivan1/openpptx/compare/alpha...0.7.0
[0.6.0]: https://github.com/RorySullivan1/openpptx/pull/134
[0.5.1]: https://github.com/RorySullivan1/openpptx/pull/133
[0.5.0]: https://github.com/RorySullivan1/openpptx/pull/125
[0.4.0]: https://github.com/RorySullivan1/openpptx/pull/122
[0.3.2]: https://github.com/RorySullivan1/openpptx/pull/120
[0.3.1]: https://github.com/RorySullivan1/openpptx/pull/116
[0.3.0]: https://github.com/RorySullivan1/openpptx/pull/111
[0.2.0]: https://github.com/RorySullivan1/openpptx/pull/53
[0.1.0]: https://github.com/RorySullivan1/openpptx/pull/50
