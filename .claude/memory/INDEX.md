# MEMORY INDEX  ·  keep ≤ ~80 lines, ≤ ~200 chars per line

## State            (rewrite in place — current truth only, ≤ ~10 lines)
- pypptx: pure-Python `.pptx` lib (dist `pypptx`, import `pptx`); conventions `CLAUDE.md`, tooling `.claude/` (`CATALOG.md`), docs `.claude/context/`.
- Package 0.4.0; v0.3.0–v0.4.0 shipped (v0.4.0 = PR #122: real-world corpus, InvalidPackageError, compatible errors).
- **v0.5.0 PR #125 MERGED 2026-10-14 02:26Z (`b4b1c38`)** — transitions/animations read, custom layouts, handout
  master. Still owed: `.meta/version` → shipped, package 0.5.0, cursor → v0.6.0, release-tags row. **Hold the v0.5.0
  tag until #126/#127/#128 are fixed** (they write decks PowerPoint refuses). Then v0.6.0 … v0.7.0.
- API reference: `sphinx-build -W -b html docs docs/_build/html` (docs extra). #51 closed by PR #124.
- **The owner's Windows box has PowerPoint 16.0**, so the `human-gated` verification row is now runnable there.
- **Open bugs #126/#127/#128: glow, legacy comments and all 6 chartex types write decks PowerPoint REFUSES to open** —
  diagnosed, each fix proved, no code changed yet — sessions/2026-10-13-2217-powerpoint-verification-pr119-125.md
- No git tags or Releases yet: sessions can't push tags. Owner tags by hand from `.meta/release-tags.md` (v0.1.0–v0.4.0).
- Sessions push only to their assigned branch, not `vX.Y.Z`; `.meta/version` records the real branch.
- **Actions RUNS again as of 2026-10-14 01:48Z** (PR #125 ran all 7 cells green) — the 2026-09-27 billing block is cleared; PRs can be CI-verified. LF pinned; `tests.yml` covers 3.9–3.13/Win/macOS.

## Decisions        (append-only; supersede, never delete)
- [2026-09-24..30] 14 earlier decisions (claudeBrain adoption, text styles, arcs, element-class keying, SmartArt,
  chartex, AlternateContent, hot-path caches, roadmap renumber, tags, 3D writers, Sphinx) — sessions/ARCHIVE-2026.md
- [2026-09-26] Pin `* text=auto eol=lf` repo-wide + explicit `binary` fixtures: the snippet loaders are
  byte-exact (`"rb"`, split on `"

"`) so a CRLF tree breaks 51 tests; `osx_dirs_fixture` injects `posixpath`
  rather than skipping on Windows — sessions/2026-09-26-2219-windows-crlf-acceptance.md
- [2026-09-30] v0.4.0 owner decisions: Apache POI corpus files are OK for TESTING ONLY (MANIFEST.in prunes them from the sdist);
  geometry-less `p:sp` → `shape_type` AUTO_SHAPE — .meta/roadmap/stages/03-hardening-and-gaps/v0.4.0.md
- [2026-09-30] pytest collects `and_it_*`/`but_it_*` too (59 were silently skipped). pypptx domain errors keep the
  builtin they replaced (ShapeError etc. are ValueErrors) — sessions/2026-09-30-1642-v040-realworld-hardening.md
- [2026-10-01] #51 perf gate counts WORK (cProfile calls into pptx/ over the corpus), not time; budget pinned to
  py3.11 (skips elsewhere), +2% tolerance; lower it whenever it drops — sessions/2026-10-01-1546-issue-51-perf.md
- [2026-10-13] "Opens without repair" is CHECKABLE on Windows: open via COM with `DisplayAlerts = ppAlertsNone` and
  PowerPoint turns the repair prompt into `0x80070570`. Controls that make it fail: truncated slide XML, and a part
  deleted while its relationship stays. `Presentation.Saved` is NOT a repair signal (True either way)
  — sessions/2026-10-13-2217-powerpoint-verification-pr119-125.md
- [2026-10-13] A passing suite does NOT mean PowerPoint accepts the output: 3 merged features write decks it refuses
  (#126 glow w/o colour child, #127 orphaned commentAuthors part, #128 chartex w/o chartStyle+chartColorStyle). Each
  shipped behind an "opens in PowerPoint" check nobody ran — same log
- [2026-10-13] Merge order: **merge #125 BEFORE fixing #126/#127/#128**. The bugs live in already-merged features, so
  holding #125 contains nothing; its only overlap with the fixes is two TEST files (`tests/chart/test_chartexwriter.py`,
  `tests/test_comments.py`) where the regression tests will land — zero `src/` overlap. Hold the **v0.5.0 tag**, not the
  merge, until the three are fixed and re-verified in PowerPoint (merging publishes nothing; owner tags by hand)

## Threads          (open items; remove when closed)
- Epic #87 human checks: master text styles rendering in PowerPoint; `apply_theme` with a real PowerPoint .thmx.
- Epic #79 human checks: picture/tiled fill, radial gradient, elliptical arc, table insert inside a merge.
- Epic #56 human checks: custom show plays the right slides; loop/kiosk take effect; last-embedded-font removal opens cleanly.
- v0.3.2 docstring audit: consider adopting the factory's prose tier (`prose_budget.py`, `prose-auditor`, `/prose-review`).
- Epic #62 human check: edited SmartArt node text shows in PowerPoint (use a PowerPoint-authored deck).
- Epic #66 chartex: human check RUN and FAILED → #128. Data table renders fine.
- Epic #75 human checks: added audio plays; trim/fade take effect; 3D model/zoom deck matches the selection pane.
- `unverified` surfaces (verification-surface.md): type checker. The "opens and renders" row can move to
  `agent-runnable` **on Windows+PowerPoint** (method + controls in the 2026-10-13 decision); keep it human-gated elsewhere.
- Fix #126/#127/#128, each with a regression test that fails against today's code.
- `slide.transition` under-reports: PowerPoint DOES apply a layout/master transition to a slide with none of its own
  (proved by stripping every slide's `p:transition` — same rendered effect). Consider `effective_transition`.
- `thruBlk` ("fade through black") is not exposed: `<p:fade/>` and `<p:fade thruBlk="1"/>` both read as FADE.
- Anyone with a Windows clone predating `b64d2b9` needs `git add --renormalize .` once after pulling, or git
  reports every text file modified (its dirty check compares the size recorded in the index, not content).
- `tests.yml` caveats: `paths-ignore` (md/.claude/.meta) must go if `tests` ever becomes a REQUIRED check, or
  docs-only PRs wait forever; ~17 billable min/run, 10 of them the single macOS cell (x10 multiplier).
- #115 human check DONE 2026-10-13: 3D charts open, camera/floor/walls render. Still no `series_axis` API.
- #114 human check: shape-tagged deck opens in PowerPoint without repair. Follow-up idea: `has_tags` (reading creates a part).

## Log              (append-only pointers)
- 2026-09-24..25 | 8 earlier sessions (claudeBrain adoption; epics #87/#79/#56/#62/#66/#75; #51 caches) | sessions/ARCHIVE-2026.md
- 2026-09-26 | Roadmap reconcile + package 0.3.0 | .meta/roadmap/INDEX.md
- 2026-09-26 2219 | Windows/LF acceptance + cross-platform CI (PR #112 merged b64d2b9) | sessions/2026-09-26-2219-windows-crlf-acceptance.md
- 2026-09-27 1829 | v0.3.1 examples (PR #116); #114/#115 filed; Actions billing-blocked | sessions/2026-09-27-1829-v031-examples.md
- 2026-09-28 | v0.3.1 marked shipped, cursor → v0.3.2, package 0.3.1 | .meta/version
- 2026-09-29 1211 | #114 shape tags (`BaseShape.tags`), slide tags keyed by cSld ref | sessions/2026-09-29-1211-issue-114-shape-tags.md
- 2026-09-29 2205 | #115 3D chart authoring: 13 THREE_D_* types via add_chart | sessions/2026-09-29-2205-issue-115-3d-charts.md
- 2026-09-30 0353 | v0.3.2 started: Sphinx scaffold, -W clean, docstring gaps closed | sessions/2026-09-30-0353-v032-docstrings-sphinx.md
- 2026-09-30 | v0.3.2 shipped (PR #120, 33a3e02): package 0.3.2, cursor → v0.4.0 | .meta/version
- 2026-09-30 | Release-tag commits recorded (.meta/release-tags.md); v0.4.0 card expanded from a POI-corpus pilot | .meta/roadmap/stages/03-hardening-and-gaps/v0.4.0.md
- 2026-09-30 1642 | v0.4.0 built: POI corpus, InvalidPackageError, compatible errors, Hypothesis (5 bugs) | sessions/2026-09-30-1642-v040-realworld-hardening.md
- 2026-10-01 | v0.4.0 shipped (PR #122, 2c64b2d): package 0.4.0, cursor → v0.5.0 | .meta/version
- 2026-10-01 1546 | #51: P6 getters, placeholder caching (corpus read −32%), work-count gate | sessions/2026-10-01-1546-issue-51-perf.md
- 2026-10-01 | #51 last item: enum `from_xml` dict lookup; v0.6.0 card records the #51 outcomes | .claude/context/performance.md
- 2026-10-13 2217 | PowerPoint checks for #119–#125 run on Windows; #115/#122/#125 pass; 3 bugs filed #126–#128 | sessions/2026-10-13-2217-powerpoint-verification-pr119-125.md
- 2026-10-13 2228 | Actions unblocked (7/7 green); #125 merged first (`b4b1c38`), tag held for #126–#128; local memory diverges from origin — commit before pulling | sessions/2026-10-13-2228-pr125-merge-order-ci-unblocked.md
