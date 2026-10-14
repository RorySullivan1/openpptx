# 2026-10-13 22:17 · powerpoint-verification-pr119-125

**Goal:** run the pending PowerPoint human-gated checks for PRs #119-#125 on a machine with PowerPoint

## What happened

- First session on a box with **PowerPoint 16.0 (build 20430)**, so the `human-gated` row of
  `verification-surface.md` ("output opens and renders correctly") was finally executable.
- Verified on a worktree of PR #125's branch (`1a840e3`), which contains `main` (`7535b1d`), so one
  tree covered #119, #122 and #125.
- **Agent-runnable:** `pytest -q` 4367 passed / 1 skipped (the work-count gate skips off 3.11);
  all 21 runnable examples exit 0; `sphinx-build -W -E` exit 0.
- **Built a COM harness** (`pp_open.ps1`, `pp_one.ps1`, `pp_authorex.ps1` — kept in the session
  scratchpad, not the repo): opens each deck with `DisplayAlerts = ppAlertsNone`, dumps PowerPoint's
  own object model (layout gallery, `SlideShowTransition`, `TimeLine.MainSequence`) and exports
  slide PNGs.
- **Closed human checks:** #119 3-D charts render with depth axis + coloured floor/back wall;
  #122 round-tripped corpus decks render **pixel-identical** to the originals (0 differing px) and
  the API-set table/chart shadows render; #125 layout gallery, placeholders and `1_Quote` naming.
- **Found 3 defects** that make PowerPoint refuse decks the library writes while every test and
  example passes — see Decisions in INDEX.md and the table below.

## Gotchas & dead ends

- **`pytest ... | tail` returns the PIPE's exit status.** An earlier run reported exit 0 while
  pytest had aborted at collection. Tee to a file and read pytest's own summary line.
- **A worktree does not get its own `import pptx`.** `pip install -e` binds one fixed `src/`, so a
  PR's tests silently run against `main` unless `PYTHONPATH=<worktree>/src` is set. Verified by
  printing `pptx.__file__` both ways.
- `hypothesis` (dev dep since #122) was missing locally → collection error. `pip install -e ".[dev,docs]"`.
- **How to make "opens without repair" a real check:** with alerts suppressed PowerPoint turns the
  repair prompt into `0x80070570`. Controls: truncated slide XML → error; **missing part with a live
  relationship → error** (the canonical repair case); known-good → opens. `Presentation.Saved` is
  **not** a discriminator (reads True for good files *and* for a file with an unknown child element
  that PowerPoint silently ignores).
- Dead end: `AddChart2` fails with `E_FAIL` unless the Presentation is created **with a window**
  (`Presentations.Add(-1)` + `Visible`).
- Dead end: chartex blamed on the chart XML. Grafting pypptx's `chartEx1.xml` into PowerPoint's own
  deck **opens fine**; an earlier contrary result (v5) was contaminated — PowerPoint's chart part was
  left with pypptx's rels. Also ruled out: `mc:AlternateContent` wrapper, the `xmlns:r` on `cx:chart`
  (the slide root already declares it), content types, dangling rels.
- Two of my own analysis errors, both corrected: `MsoAnimTriggerType` is **0-based**
  (None=0, OnPageClick=1, WithPrevious=2, AfterPrevious=3) — a 1-based table invented 44 fake
  mismatches; and `slide.transition` **always returns an object** (`type == NONE` when absent), so
  `is not None` is never a useful predicate.

## State at end

- Repo untouched (`main` clean at `7535b1d`). Nothing committed.
- **Filed #126 (glow), #127 (legacy comments), #128 (chartex)** — all `bug`, each with repro, evidence and
  acceptance incl. a regression test that must fail against today's code. All three reproduce on `main` 7535b1d.
- The three defects are diagnosed and each fix was **proved** by rebuilding the real example deck
  with that one change and watching PowerPoint open it. No library code was changed.

| Deck | Root cause | Proved fix |
|---|---|---|
| `shape_effects.pptx` | `<a:glow rad=".."/>` written with **no `EG_ColorChoice` child** (schema requires one) | add any colour child |
| `comments_and_metadata.pptx` | `ppt/commentAuthors.xml` is an **orphan part** — no `commentAuthors` relationship from `presentation.xml`, so `authorId` can't resolve | add that relationship |
| `modern_charts.pptx` (all 6 chartex types) | missing the **`chartStyle` + `chartColorStyle`** parts (`style1.xml`/`colors1.xml`) PowerPoint requires for chartex | add both — **neither alone suffices** |

- Controls that passed and bound each cause: shadow / soft edge / bevel / extrusion; threaded
  comments / slide tags / shape tags / sections / custom properties; classic chart + data table.

## Open threads

- Fix #126/#127/#128 (regression test each: assert the colour child, the relationship, the two parts).
  They belong to epics #66 (chartex), #79/#75 (effects) and the comments work — all three had an
  un-run "opens in PowerPoint" check, which is exactly how they shipped broken.
- `verification-surface.md`: the "Output opens and renders correctly" row can become
  `agent-runnable` **on a Windows+PowerPoint box** (command + the controls that make it fail are in
  Gotchas). Keep it `human-gated` elsewhere.
- Transition inheritance **is real**: stripping every slide's own `p:transition` left PowerPoint
  reporting the identical effect (3073) while a deck with none anywhere reports 0. So
  `slide.transition` under-reports what PowerPoint plays — consider an `effective_transition`.
- `thruBlk` ("fade through black") is not exposed: plain `<p:fade/>` and `<p:fade thruBlk="1"/>`
  both read as `FADE` though PowerPoint distinguishes them (entry effect 3849 vs 1793).
- Still unchecked by a human: the older epic #87/#56/#62 items (master text styles, custom shows,
  SmartArt text edits) — the harness now exists to do them cheaply.
