# MEMORY INDEX  ·  keep ≤ ~80 lines, ≤ ~200 chars per line

## State            (rewrite in place — current truth only, ≤ ~10 lines)
- pypptx: pure-Python `.pptx` lib (dist `pypptx`, import `pptx`); conventions `CLAUDE.md`, tooling `.claude/` (`CATALOG.md`), docs `.claude/context/`.
- Package 0.5.1 SHIPPED (PR #133 merged `51a8cd1`); v0.5.1 tag row recorded; owner tags v0.5.0 + v0.5.1 by hand.
  **In flight: v0.6.0 on branch `v0.6.0`** — perf remainder only: lazy binary blobs + caching audit (`.meta/version`).
  Next step: expand the v0.6.0 card with implementation detail before code lands.
- **The owner's Windows box has PowerPoint 16.0**, so the `human-gated` verification row is now runnable there.
- No git tags or Releases yet: sessions can't push tags. Owner tags by hand from `.meta/release-tags.md` (v0.1.0–v0.4.0 ready; v0.5.0's row is recorded but HELD).
- Sessions push only to their assigned branch, not `vX.Y.Z`; `.meta/version` records the real branch.
- Actions RUNS again (2026-10-14 01:48Z, #125 ran 7/7 green); LF pinned; `tests.yml` covers 3.9–3.13/Win/macOS.
- API reference: `sphinx-build -W -b html docs docs/_build/html` (docs extra).

## Decisions        (append-only; supersede, never delete)
- [2026-09-24..10-09] 19 earlier decisions (claudeBrain adoption, text styles, arcs, element-class keying, SmartArt,
  chartex, AlternateContent, hot-path caches, roadmap renumber, CRLF/LF, POI corpus, test names, perf gate, Sphinx,
  v0.4.0 + v0.5.0 owner decisions) — sessions/ARCHIVE-2026.md
- [2026-10-13] "Opens without repair" is CHECKABLE on Windows: open via COM with `DisplayAlerts = ppAlertsNone` and
  PowerPoint turns the repair prompt into `0x80070570`. Controls that make it fail: truncated slide XML, and a part deleted
  while its relationship stays. `Presentation.Saved` is NOT a repair signal (True either way) — sessions/2026-10-13-2217-powerpoint-verification-pr119-125.md
- [2026-10-13] A passing suite does NOT mean PowerPoint accepts the output: 3 merged features write decks it refuses
  (#126 glow w/o colour child, #127 orphaned commentAuthors part, #128 chartex w/o chartStyle+chartColorStyle). Each
  shipped behind an "opens in PowerPoint" check nobody ran — same log
- [2026-10-13] Merge order: **merge #125 BEFORE fixing #126–#128**. The bugs live in already-merged features, so holding
  #125 contained nothing; overlap with the fixes is two TEST files only (test_chartexwriter, test_comments) — zero `src/`.
  Hold the **tag**, not the merge: merging publishes nothing (owner tags by hand) — sessions/2026-10-13-2228-pr125-merge-order-ci-unblocked.md
- [2026-10-15] Owner: #131 (shadow) and #132 (chartex re-save repair) ship IN v0.5.1, one close-out PR with the version
  bump — not deferred to v0.6.0 — sessions/2026-10-15-0834-v051-followups-filed.md
- [2026-10-15] Owner: default shadow colour = `prstClr black` @ 40% (PowerPoint "Outer Offset"); chartex style repair runs
  ON LOAD. Templateless types (Pareto/region map/None) get the histogram style — same log
- [2026-10-15] Load-time repairs live in `OpcPackage._repair_loaded_parts(parts)` (Package overrides), scanning the
  loader's part dict: an `iter_parts()` walk cost +1.7% work count, near the 2% gate — same log

- [2026-10-15] Owner: v0.6.0 = perf remainder only (lazy blobs + caching audit); streaming save dropped unless measured;
  cross-run text stays v0.7.0 — .meta/version

## Threads          (open items; remove when closed)
- Optional, unfiled (PR #130 notes): package check flagging a part with a content type but no inbound relationship.
  Would NOT have caught #127 (the part was related, from the wrong source).
- The `github` MCP server may fail to connect ("Authorization header is badly formatted"); `gh` CLI works — use it.
- v0.3.2 docstring audit: consider adopting the factory's prose tier (`prose_budget.py`, `prose-auditor`, `/prose-review`).
- Legacy getters write on read (from python-pptx): `Font.color` makes fill solid, `_Paragraph.alignment` adds a:pPr.
  Candidate fix; until then use deckwalk.walk_timing (not walk) for read-then-save checks.
- PowerPoint human checks for epics #56 #62 #66 #75 #79 #87 and issues #114 #115 — .claude/context/verification-surface.md
  § Pending human checks. RUN 2026-10-13: #115/#122/#125 pass; epic #66 chartex FAILED → #128 (its data table renders
  fine); #115 3D charts render but still have no `series_axis` API.
- `unverified` surfaces (verification-surface.md): type checker. The "opens and renders" row can move to
  `agent-runnable` **on Windows+PowerPoint** (method + controls in the 2026-10-13 decision); keep it human-gated elsewhere.
- `slide.transition` under-reports: PowerPoint DOES apply a layout/master transition to a slide with none of its own
  (proved by stripping every slide's `p:transition` — same rendered effect). Consider `effective_transition`.
- `thruBlk` ("fade through black") is not exposed: `<p:fade/>` and `<p:fade thruBlk="1"/>` both read as FADE.
- A Windows clone predating `b64d2b9` needs `git add --renormalize .` once after pulling, else git calls every text file modified.
- `tests.yml` caveats: `paths-ignore` (md/.claude/.meta) must go if `tests` ever becomes a REQUIRED check, or
  docs-only PRs wait forever; ~17 billable min/run, 10 of them the single macOS cell (x10 multiplier).
- #114 human check: shape-tagged deck opens in PowerPoint without repair. Follow-up idea: `has_tags` (reading creates a part).

## Log              (append-only pointers)
- 2026-09-24..10-09 | 22 earlier sessions (claudeBrain adoption; epics #87/#79/#56/#62/#66/#75; #51 perf; v0.3.x docs
  and examples; #114 tags; #115 3D charts; v0.4.0 hardening; v0.5.0 build) | sessions/ARCHIVE-2026.md
- 2026-10-13 2217 | PowerPoint checks for #119–#125 run on Windows; #115/#122/#125 pass; 3 bugs filed #126–#128 | sessions/2026-10-13-2217-powerpoint-verification-pr119-125.md
- 2026-10-13 2228 | Actions unblocked (7/7 green); #125 merged ahead of #126–#128, tag held; local memory merged with origin | sessions/2026-10-13-2228-pr125-merge-order-ci-unblocked.md
- 2026-10-13 | v0.5.0 shipped (PR #125, `b4b1c38`): package 0.5.0, cursor → v0.6.0; tag held for #126–#128 | .meta/version
- 2026-10-13 2253 | Assessed next-on-main: #126–#128 ahead of the cursor, recommended as a v0.5.1 patch; v0.6.0 card found thin | sessions/2026-10-13-2253-main-next-assessment.md
- 2026-10-14 | v0.5.1 fixes written (unlogged sessions): #126 merged via PR #129; #127+#128 in PR #130 | gh pr view 130
- 2026-10-15 | Memory reconciled: PR #130 merged 2026-10-14 (`1c132d7`); version bump + tags are all that's left of v0.5.1 | gh pr view 130
- 2026-10-15 0834 | Filed #131 (shadow colour) + #132 (chartex re-save repair); owner put both in v0.5.1 close-out | sessions/2026-10-15-0834-v051-followups-filed.md
- 2026-10-15 | #131 + #132 fixed and PowerPoint-verified; package 0.5.1; close-out PR opened | sessions/2026-10-15-0834-v051-followups-filed.md
