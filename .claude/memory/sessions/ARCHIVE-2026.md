# Memory archive — 2026

Decisions folded out of INDEX.md to keep it in budget. Still in force unless superseded.

## Decisions archived 2026-09-30

- [2026-09-24] Claude assets consolidated: internal_docs → `.claude/context/`, dev_map → `.meta/roadmap/` (hooks read `.meta/`)
  — sessions/2026-09-24-1505-adopt-claudebrain-assets.md
- [2026-09-24] Adopted factory core + roadmap tier + Python/GitHub/docs families. EXCLUDED (not our stacks): VSTO, VBA,
  Power Platform/SharePoint/Power BI, quant, branding→presentation, Outlook/print HTML. Prose tier deferred to v0.3.2 (was v0.2.2) — same log
- [2026-09-24] Keep pypptx's branch-per-version naming `vX.Y.Z` over `/version-set`'s `claude/<label>-<slug>` default (CLAUDE.md § Roadmap) — same log
- [2026-09-24] Text-style levels are zero-based like `_Paragraph.level`; `phClr` → `MSO_THEME_COLOR.PLACEHOLDER` (17)
  — sessions/2026-09-24-1819-epic-87-text-styles-themes.md
- [2026-09-24] Arc angles are visual (DrawingML), converted to parametric for extents; table merge edits promote the next
  continuation cell and copy the orthogonal span — sessions/2026-09-24-1844-epic-79-shape-line-fill-table.md
- [2026-09-25] Element classes are keyed by tag alone: a tag shared across contexts (`p:custShow`, `p:sld`, `a:path`) gets ONE class;
  a test fails on duplicate `register_element_cls` tags — sessions/2026-09-25-1202-epic-56-presentation-parts.md
- [2026-09-25] SmartArt text edits DROP the cached dsp:drawing part (not patch it); `MSO_SHAPE_TYPE.SMART_ART` is canonical,
  `IGX_GRAPHIC` an alias — sessions/2026-09-25-1400-epic-62-smartart.md
- [2026-09-25] Chartex charts are a SIBLING API (`GraphicFrame.chartex`, `has_chart` False, `shape_type` CHART); the
  shape is the `mc:Choice` graphicFrame and `tree_elm()` gives its wrapper — sessions/2026-09-25-1530-epic-66-chartex-dtable.md
- [2026-09-25] Non-chartex `mc:AlternateContent` shapes are one read-only `AlternateContentShape` each, represented by the
  Fallback shape (else Choice) — sessions/2026-09-25-1600-epic-75-media-altcontent.md
- [2026-09-25] Hot-path caching: `qn` is lru_cached; `BaseOxmlElement.xpath` evaluates per-thread cached compiled XPath
  (`xmlchemy.compiled_xpath`) — sessions/2026-09-25-1630-issue-51-perf-caches.md

## Decisions archived 2026-10-13

- [2026-09-26] Roadmap renumbered: shipped epics = v0.3.0; docs versions v0.2.1/v0.2.2 → v0.3.1/v0.3.2; stage-03 plans
  v0.3.0–v0.6.0 → v0.4.0–v0.7.0 (package versions must increase) — .meta/roadmap/stages/03-hardening-and-gaps/v0.3.0.md
- [2026-09-29] Tags are one part PER owner, referenced from its `p:custDataLst/p:tags` (`p:nvPr` for a shape,
  `p:cSld` for the slide), related from the slide part; slide tags resolve by that reference, not by reltype
  — sessions/2026-09-29-1211-issue-114-shape-tags.md
- [2026-09-29] 3D chart writers share `_Base3DChartXmlWriter`; only THREE_D_COLUMN/AREA/LINE get a `c:serAx` + perspective
  camera. New chart XML uses POSITIVE axis ids (`unsignedInt`) — sessions/2026-09-29-2205-issue-115-3d-charts.md
- [2026-09-30] Sphinx `|Name|` substitutions are GENERATED in docs/conf.py from pptx's classes (no hand list); enum `:ref:`
  labels live on docs/api/enum.rst; `-W` is the docs gate — sessions/2026-09-30-0353-v032-docstrings-sphinx.md

## Log pointers archived 2026-10-13

- 2026-09-24 1505 | Consolidate into .claude/ + adopt claudeBrain assets | sessions/2026-09-24-1505-adopt-claudebrain-assets.md
- 2026-09-24 1819 | Close epic #87 (text styles, theme lists, apply_theme) | sessions/2026-09-24-1819-epic-87-text-styles-themes.md
- 2026-09-24 1844 | Close epic #79 (shape/line/fill/table completeness) | sessions/2026-09-24-1844-epic-79-shape-line-fill-table.md
- 2026-09-25 1202 | Close epic #56 (package-level presentation parts) | sessions/2026-09-25-1202-epic-56-presentation-parts.md
- 2026-09-25 1400 | Epic #62 SmartArt read + node text edit (PR #101 merged) | sessions/2026-09-25-1400-epic-62-smartart.md
- 2026-09-25 1530 | Epic #66 chartex + data table (PR #103 merged) | sessions/2026-09-25-1530-epic-66-chartex-dtable.md
- 2026-09-25 1600 | Epic #75 audio, trim/fade, AlternateContent shapes (PR #105 merged) | sessions/2026-09-25-1600-epic-75-media-altcontent.md
- 2026-09-25 1630 | Issue #51: qn/XPath caches (−39%/deck); perf harness PR #109 | sessions/2026-09-25-1630-issue-51-perf-caches.md
