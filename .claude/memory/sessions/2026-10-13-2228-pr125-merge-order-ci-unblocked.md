# 2026-10-13 22:28 · pr125-merge-order-ci-unblocked

**Goal:** Decide merge order for PR #125 vs bugs #126/#127/#128; correct the stale Actions-billing memory item

## What happened
- **GitHub Actions is no longer billing-blocked.** PR #125's `tests` workflow ran all 7 cells
  (ubuntu 3.9–3.13, windows 3.13, macos 3.13) to SUCCESS at 2026-10-14 01:48Z, run `38497540055`.
  The State line claiming "all evidence is local (since 2026-09-27)" was stale and is rewritten;
  the matching Threads item ("Actions billing blocks every job") is removed as resolved.
- **Merge-order call: merge #125 first, fix the three bugs after.** Evidence: `mergeable: MERGEABLE`,
  `mergeStateStatus: CLEAN`, not a draft, no required review, CI green, and PowerPoint-verified in the
  preceding session. #126/#127/#128 are defects in features ALREADY on `main`, so holding #125 contained
  nothing. Overlap with the coming fixes is two TEST files only — `tests/chart/test_chartexwriter.py` and
  `tests/test_comments.py`, exactly where the regression tests land — and ZERO `src/` overlap
  (#125 touches animation/transition/slide/presentation/placeholder/shapetree; the fixes touch
  dml-effect, the comments part, and the chartex writer).
- **Owner merged #125** at 2026-10-14 02:26:58Z, merge commit `b4b1c38`.
- Distinguished merging from releasing: nothing is on PyPI/Releases and tags are hand-cut from
  `.meta/release-tags.md`, so the merge publishes nothing. The thing to withhold is the **v0.5.0 tag**,
  not the merge, until the three PowerPoint-fatal bugs are fixed and re-verified.

## Gotchas & dead ends
- **The local memory files diverge from `origin/main` and a naive `git pull` will conflict.** The working
  tree's `.claude/memory/INDEX.md` + `sessions/ARCHIVE-2026.md` carry UNCOMMITTED edits from the
  2026-10-13 2217 session (plus this one), while `origin/main` advanced them independently in commits
  `1a840e3` ("Memory: v0.5.0 PR #125 opened") and the #125 merge. The working tree is the NEWER content
  and must win on conflict; commit the local memory edits before merging `origin/main`, do not pull first.
- `.meta/version` on `origin/main` was already updated for #125 (commit `8dc6982`) but the local clone is
  behind — don't re-derive the cursor from the local file until main is pulled.
- Deliberately did NOT merge, pull, or commit anything: the question asked was advisory, and the
  memory-file divergence above makes an unattended pull destructive.

## State at end
- `main` on the remote is `b4b1c38` (#125 merged); local `main` still at `7535b1d`, memory edits uncommitted.
- Three bugs open and unfixed: #126 (glow without colour child), #127 (orphaned `commentAuthors.xml`),
  #128 (chartex without `chartStyle` + `chartColorStyle`). Each diagnosed with a proved fix, no code written.
- CI can verify PRs again, so the "all evidence is local" constraint on every open thread is lifted.

## Open threads
- Pull `origin/main` locally, resolving the memory conflicts in favour of the working tree.
- v0.5.0 close-out still owed: `.meta/version` → shipped, package 0.5.0, cursor → v0.6.0, release-tags row.
- Fix #126/#127/#128, each with a regression test that fails against today's code, plus the COM
  "opens without repair" check (`DisplayAlerts = ppAlertsNone` → `0x80070570`) from the 2217 session.
- Hold the v0.5.0 tag until those three are fixed and re-verified in PowerPoint.
- `tests.yml` cost caveat still stands now that runs actually bill: ~17 billable min/run, ~10 of them the
  single macOS cell (x10 multiplier).
