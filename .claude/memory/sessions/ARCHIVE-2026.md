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

## Decisions archived 2026-10-09

- [2026-09-29] Tags are one part PER owner, referenced from its `p:custDataLst/p:tags` (`p:nvPr` for a shape,
  `p:cSld` for the slide), related from the slide part; slide tags resolve by that reference, not by reltype
  — sessions/2026-09-29-1211-issue-114-shape-tags.md
- [2026-09-29] 3D chart writers share `_Base3DChartXmlWriter`; only THREE_D_COLUMN/AREA/LINE get a `c:serAx` + perspective
  camera. New chart XML uses POSITIVE axis ids (`unsignedInt`) — sessions/2026-09-29-2205-issue-115-3d-charts.md

## Decisions archived 2026-10-13

- [2026-09-26] Roadmap renumbered: shipped epics = v0.3.0; docs versions v0.2.1/v0.2.2 → v0.3.1/v0.3.2; stage-03 plans
  v0.3.0–v0.6.0 → v0.4.0–v0.7.0 (package versions must increase) — .meta/roadmap/stages/03-hardening-and-gaps/v0.3.0.md
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

## Decisions archived 2026-10-13 (second pass)
- [2026-09-26] Pin `* text=auto eol=lf` repo-wide + explicit `binary` fixtures: the snippet loaders are
  byte-exact (`"rb"`, split on blank lines) so a CRLF tree breaks 51 tests; `osx_dirs_fixture` injects
  `posixpath` rather than skipping on Windows — sessions/2026-09-26-2219-windows-crlf-acceptance.md
- [2026-09-30] v0.4.0 owner decisions: Apache POI corpus files are OK for TESTING ONLY (MANIFEST.in prunes
  them from the sdist); geometry-less `p:sp` → `shape_type` AUTO_SHAPE — stages/03-hardening-and-gaps/v0.4.0.md
- [2026-09-30] pytest collects `and_it_*`/`but_it_*` too (59 silently skipped; 6 more found 2026-10-09, now
  guarded by tests/test_test_names.py). pypptx domain errors keep the builtin they replaced (ShapeError etc.
  are ValueErrors) — sessions/2026-09-30-1642-v040-realworld-hardening.md
- [2026-10-01] #51 perf gate counts WORK (cProfile calls into pptx/ over the corpus), not time; budget pinned
  to py3.11 (skips elsewhere), +2% tolerance; lower it whenever it drops — sessions/2026-10-01-1546-issue-51-perf.md
- [2026-10-09] v0.5.0 owner decisions (all recommendations): +4 POI decks (test only); effect names only for
  entr/exit presetID 1–31 (MsoAnimEffect values); new layout = PowerPoint Insert Layout; no layout shapes yet;
  transitions read as stored — stages/03-hardening-and-gaps/v0.5.0.md

## Log pointers archived 2026-10-13 (second pass)
- 2026-09-26 | Roadmap reconcile + package 0.3.0 | .meta/roadmap/INDEX.md
- 2026-09-26 2219 | Windows/LF acceptance + cross-platform CI (PR #112 merged b64d2b9) | sessions/2026-09-26-2219-windows-crlf-acceptance.md
- 2026-09-27 1829 | v0.3.1 examples (PR #116); #114/#115 filed; Actions billing-blocked | sessions/2026-09-27-1829-v031-examples.md
- 2026-09-28 | v0.3.1 marked shipped, cursor → v0.3.2, package 0.3.1 | .meta/version
- 2026-09-29 1211 | #114 shape tags (`BaseShape.tags`), slide tags keyed by cSld ref | sessions/2026-09-29-1211-issue-114-shape-tags.md
- 2026-09-29 2205 | #115 3D chart authoring: 13 THREE_D_* types via add_chart | sessions/2026-09-29-2205-issue-115-3d-charts.md
- 2026-09-30 0353 | v0.3.2 started: Sphinx scaffold, -W clean, docstring gaps closed | sessions/2026-09-30-0353-v032-docstrings-sphinx.md
- 2026-09-30 | v0.3.2 shipped (PR #120, 33a3e02): package 0.3.2, cursor → v0.4.0 | .meta/version
- 2026-09-30 | Release-tag commits recorded (.meta/release-tags.md); v0.4.0 card expanded from a POI-corpus pilot | stages/03-hardening-and-gaps/v0.4.0.md
- 2026-09-30 1642 | v0.4.0 built: POI corpus, InvalidPackageError, compatible errors, Hypothesis (5 bugs) | sessions/2026-09-30-1642-v040-realworld-hardening.md
- 2026-10-01 | v0.4.0 shipped (PR #122, 2c64b2d): package 0.4.0, cursor → v0.5.0 | .meta/version
- 2026-10-01 1546 | #51: P6 getters, placeholder caching (corpus read −32%), work-count gate | sessions/2026-10-01-1546-issue-51-perf.md
- 2026-10-01 | #51 last item: enum `from_xml` dict lookup; v0.6.0 card records the #51 outcomes | .claude/context/performance.md
- 2026-10-09 | #51 closed (PR #124); v0.5.0 card expanded from a 511-deck pilot | stages/03-hardening-and-gaps/v0.5.0.md
- 2026-10-09 1630 | v0.5.0 built: transitions/animations read, layouts, handout master; import_slide id fix | sessions/2026-10-09-1630-v050-transitions-animations-layouts.md

## Log pointers archived 2026-10-16
- 2026-10-13 2217 | PowerPoint checks for #119–#125 run on Windows; #115/#122/#125 pass; 3 bugs filed #126–#128 | sessions/2026-10-13-2217-powerpoint-verification-pr119-125.md
- 2026-10-13 2228 | Actions unblocked (7/7 green); #125 merged ahead of #126–#128, tag held; local memory merged with origin | sessions/2026-10-13-2228-pr125-merge-order-ci-unblocked.md
- 2026-10-13 | v0.5.0 shipped (PR #125, `b4b1c38`): package 0.5.0, cursor → v0.6.0; tag held for #126–#128 | .meta/version
- 2026-10-13 2253 | Assessed next-on-main: #126–#128 ahead of the cursor, recommended as a v0.5.1 patch; v0.6.0 card found thin | sessions/2026-10-13-2253-main-next-assessment.md
- 2026-10-14 | v0.5.1 fixes written (unlogged sessions): #126 merged via PR #129; #127+#128 in PR #130 | gh pr view 130
- 2026-10-15 | Memory reconciled: PR #130 merged 2026-10-14 (`1c132d7`); version bump + tags are all that's left of v0.5.1 | gh pr view 130
- 2026-10-15 0834 | Filed #131 (shadow colour) + #132 (chartex re-save repair); owner put both in v0.5.1 close-out | sessions/2026-10-15-0834-v051-followups-filed.md
- 2026-10-15 | #131 + #132 fixed and PowerPoint-verified; package 0.5.1; close-out PR opened | sessions/2026-10-15-0834-v051-followups-filed.md
- 2026-10-15 1347 | v0.6.0 built end to end: card, L1/L2, lazy blobs, caching audit (11 fixes), gate metric, 0.6.0; PR #134 ready | sessions/2026-10-15-1347-v060-card-expanded.md

## Log entries folded from INDEX.md on 2026-10-16
- 2026-10-16 0345 | v0.7.0 built end to end (search.py, deck-wide, hypothesis, PowerPoint COM pass, perf flat); PR #135 ready | sessions/2026-10-16-0345-v070-built.md
- 2026-10-16 | v0.7.0 merged (PR #135, `0db7ef1`, 7/7 CI on `f9333f5`); shipped, release-tag row added, cursor → v1.0.0 | .meta/release-tags.md
- 2026-10-16 | v0.7.1 built: 9 review findings → template/count errors up front, TextMatch eq, `\v` → a:br, regex context, rel drops | sessions/2026-10-16-1300-v071-review-fixes.md
- 2026-10-16 | v0.7.1 merged (PR #136, `2627ddd`, 7/7 CI); shipped, release-tag row added, cursor → v1.0.0 | .meta/release-tags.md

## Decisions folded from INDEX.md on 2026-10-16
- [2026-10-13] "Opens without repair" is CHECKABLE on Windows: open via COM with `DisplayAlerts = ppAlertsNone` and
  PowerPoint turns the repair prompt into `0x80070570`. Controls that make it fail: truncated slide XML, and a part deleted
  while its relationship stays. `Presentation.Saved` is NOT a repair signal (True either way) — sessions/2026-10-13-2217-powerpoint-verification-pr119-125.md
- [2026-10-13] A passing suite does NOT mean PowerPoint accepts the output: 3 merged features write decks it refuses
  (#126 glow w/o colour child, #127 orphaned commentAuthors part, #128 chartex w/o chartStyle+chartColorStyle). Each
  shipped behind an "opens in PowerPoint" check nobody ran — same log

## Log entries folded from INDEX.md on 2026-10-16 (v1.0.0)
- 2026-10-16 1305 | v1.0.0 card filled in: `openpptx` dist, documented-surface contract, Pages, LICENSE | sessions/2026-10-16-1305-v100-card-expanded.md
- 2026-10-16 | v1.0.0 step 1 done: LICENSE (both notices), pyproject metadata, setuptools>=77; build+twine OK | v1.0.0 card
- 2026-10-16 | v1.0.0 step 2 done: enum raises, 4 modules documented, helpers underscored, snapshot (3138 names) | v1.0.0 card
