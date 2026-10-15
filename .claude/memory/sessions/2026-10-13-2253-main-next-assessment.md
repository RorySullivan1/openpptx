# 2026-10-13 22:53 · main-next-assessment

**Goal:** Assess what is next on main after v0.5.0

## What happened
- Read-only status pass (`/roadmap-status`): main is clean and in sync with origin at `445ac30`;
  package 0.5.0; no `v0.6.0` branch exists and nothing is in flight.
- Confirmed #126/#127/#128 are the only open issues and that they are the real next work,
  ahead of the v0.6.0 cursor: each makes PowerPoint refuse the deck (`0x80070570`), each sits in an
  already-merged feature with a defective `examples/` script, and together they hold the v0.5.0 tag.
- **Recommended shape of the fix: a `v0.5.1` PATCH, not part of v0.6.0.** They are corrections to
  released behaviour (the definition of a patch), the tag can go out the moment they land, and the
  three fixes touch disjoint code so they parallelize.
- Put one question to the owner, unanswered at session end: should the regression tests assert on the
  XML, open the deck via PowerPoint COM, or both? (Recommended both — XML assertions as the portable
  CI gate plus an opt-in `pytest -m powerpoint` suite, since only the COM check would have caught these.)

## Gotchas & dead ends
- The `github` MCP server fails to connect in this session ("Authorization header is badly formatted").
  `gh` CLI works fine — use it for issue/PR reads rather than concluding GitHub access is missing.

## State at end
- Nothing changed in `src/` or `.meta/`. This was assessment only; no branch opened.

## Open threads
- **The v0.6.0 card is mostly already struck through** — 4 of 6 goals landed early (#51/#107/#109/#123:
  perf harness, lookup indexes, `ShapeRange`, work-count gate). Only lazy blob loading, streaming save,
  and the caching audit itself remain, which is thin for a version. Re-slice it (or pull v0.7.0's
  cross-run text work forward) when its branch opens, rather than implementing the card as written.
- `.meta/version` still records v0.5.0 `shipped` while INDEX marks v0.6.0 as cursor; `/version-set`
  reconciles them when the next version actually starts.
