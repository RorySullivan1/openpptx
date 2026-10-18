# MEMORY INDEX  ·  keep ≤ ~80 lines, ≤ ~200 chars per line

## State            (rewrite in place — current truth only, ≤ ~10 lines)
- openpptx (was pypptx/`pptx` until 2026-10-16): pure-Python `.pptx` lib. Dist AND import `openpptx` (`src/openpptx/`),
  repo `RorySullivan1/openpptx`; the local clone dir is still `Projects/pypptx`; conventions `CLAUDE.md`, tooling `.claude/` (`CATALOG.md`), docs `.claude/context/`.
- **1.0.0 SHIPPED 2026-10-18**: on PyPI (`openpptx`, release run 39140694188, tag `v1.0.0` on merge `146dd1c`, PR #138; rc1
  the same day). Docs live on Pages. Nothing planned next: 1.x via `/roadmap-set`; 198 pyright errors + gaps on the card.
- Work-count gate counts TOTAL calls since v0.6.0 (primitive calls hid nested `lazyproperty.__get__`); 3.11 budget 1,073,411.
- **The owner's Windows box has PowerPoint 16.0**, so the `human-gated` verification row is now runnable there.
- Tags: local sessions can push them (pushed `v1.0.0rc1`, `v1.0.0`, as `refs/tags/...`); cloud sessions can't. Older v0.x
  rows in `.meta/release-tags.md` are still untagged; remote also has lightweight `v0.7.1`, `0.7.0`, `alpha`. No GitHub Releases yet.
- CI: `tests.yml` covers 3.9–3.13/Win/macOS; the work-count gate runs on the ubuntu 3.11 cell only.

## Decisions        (append-only; supersede, never delete)
- [2026-09-24..10-09] 19 earlier decisions (claudeBrain adoption, text styles, arcs, element-class keying, SmartArt,
  chartex, AlternateContent, hot-path caches, roadmap renumber, CRLF/LF, POI corpus, test names, perf gate, Sphinx,
  v0.4.0 + v0.5.0 owner decisions) — sessions/ARCHIVE-2026.md
- [2026-10-13] 2 decisions (repair-check via COM `ppAlertsNone` -> `0x80070570`; a passing suite != PowerPoint accepts) — sessions/ARCHIVE-2026.md
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
- [2026-10-15] Owner: lazy blobs for PATH sources only (zip reopened per read, CRC/size checked → `PackageError`; no
  held handle); stream + directory sources stay eager — sessions/2026-10-15-1347-v060-card-expanded.md
- [2026-10-15] Owner: accept save cost of lazy blobs (+5–7% images_100; fixed ~0.4 ms/save zip reopen on small decks);
  work-count gate counts total calls, re-budgeted from main — sessions/2026-10-15-1347-v060-card-expanded.md
- [2026-10-15] Owner: v0.7.0 find/replace is DECK-WIDE too (slide shapes, groups, tables, existing notes; not layouts/
  masters/charts/SmartArt); property test uses hypothesis (already a dev dep) — .meta/roadmap/stages/03-hardening-and-gaps/v0.7.0.md
- [2026-10-16] Owner, v1.0.0: PyPI `pypptx` is an unrelated 2015 project, so the dist becomes **`openpptx`** (import stays
  `pptx`, repo stays `pypptx`). The contract is the DOCUMENTED surface (oxml/opc/parts internal, not renamed;
  snapshot test). Docs on GitHub Pages. LICENSE adds python-pptx's MIT notice — sessions/2026-10-16-1305-v100-card-expanded.md
- [2026-10-16] Owner: COMPLETE rebrand to openpptx, the repo included (supersedes "repo stays pypptx"). History keeps
  the old name: shipped cards, session logs, release-tags. `PyPptxError` → `OpenPptxError` with a deprecated
  module-`__getattr__` alias — sessions/2026-10-16-1305-v100-card-expanded.md
- [2026-10-16] Owner: import renamed too, `pptx` → `openpptx` (no users yet). Supersedes "import stays pptx". With no
  users, nothing renamed before 1.0.0 gets a shim (the `PyPptxError` alias was dropped); the deprecation policy
  starts at 1.0.0 — same log
- [2026-10-16] v1.0.0 step 2: the public modules ARE the `docs/api/*.rst` targets (tests/test_public_api.py parses them);
  internal-layer classes users get (`CorePropertiesPart` etc.) use explicit `:members:`. Regen: `python -m tests.test_public_api`

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
- 2026-10-13..10-15 | 9 sessions (PowerPoint checks #119–#125, v0.5.0/v0.5.1 ship, #126–#132, v0.6.0 build) | sessions/ARCHIVE-2026.md
- 2026-10-16 | 4 entries (v0.7.0 built + merged #135, v0.7.1 built + merged #136) | sessions/ARCHIVE-2026.md
- 2026-10-16..17 | v1.0.0: card filled in (session 1305 log); steps 1–3 done, details in the card | v1.0.0 card
- 2026-10-18 | v1.0.0 SHIPPED: rc1 then 1.0.0 on PyPI; branch/tag name clash needs `refs/tags/` push | v1.0.0 card, release-tags.md
