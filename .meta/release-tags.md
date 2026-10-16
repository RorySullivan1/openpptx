# Release tags — commits that mark each version's completion

Sessions cannot push git tags, so versions are tagged by hand. Each row is the **merge commit
on `main`** where the version was complete: for versions that bumped the package, the merge
that first carries the new `version =` in `pyproject.toml`; for v0.2.0, which changed docs
only, the merge of its PR. Found by walking `main`'s first-parent history
(`git rev-list --first-parent main`) and reading `pyproject.toml` at each commit.

| Tag | Commit | Date | Merge | Package version at the commit | Notes |
|---|---|---|---|---|---|
| `v0.1.0` | `723ef5aa0d1973844a6a1975df7648db577174cf` | 2026-05-16 | PR #50 | 0.1.0 | First commit carrying 0.1.0 |
| `v0.2.0` | `49108ffc2cbbd6d523e4dd18a093ac8a086a8a03` | 2026-05-16 | PR #53 | 0.1.0 | Docs-only version; the package was never set to 0.2.0 (it went 0.1.0 → 0.3.0) |
| `v0.3.0` | `0658fa51370950394501dc251d4b92a3fe841d7c` | 2026-09-26 | PR #111 | 0.3.0 | Roadmap reconcile + package 0.3.0; the epic work it records merged in earlier PRs |
| `v0.3.1` | `99e2ef72a9fb3d4b29faa4138b9750244e207d23` | 2026-09-27 | PR #117 | 0.3.1 | Marks v0.3.1 shipped and bumps the package; the examples themselves merged in PR #116 (`1657988`) |
| `v0.3.2` | `cb8a179c3346cf75f1759c445df31f1ef244dd51` | 2026-09-30 | PR #121 | 0.3.2 | Marks v0.3.2 shipped and bumps the package; docs work merged in PR #120 (`33a3e02`). Also carries #114 and #115 |
| `v0.4.0` | `aceb359ebfd89df5f51e903b8eabde501554037c` | 2026-10-01 | PR #123 | 0.4.0 | **The ship commit itself, not a merge:** PR #123 also carries #51's P6 (`iterchildren` getters), which is not part of v0.4.0. This commit's parent is the v0.4.0 merge (`2c64b2d`, PR #122), so its tree is exactly v0.4.0 plus the ship bookkeeping |
| `v0.5.0` | `070704d2656a3298ec0b9a3cc4dd3e2096fffe3b` | 2026-10-13 | — (direct to `main`) | 0.5.0 | **Known defects, fixed in v0.5.1:** glow, legacy comments, every chartex type and shadow-without-colour write decks PowerPoint refuses (#126/#127/#128/#131). Tag it anyway as the historical v0.5.0; the hold lifted when v0.5.1 shipped the fixes. **The ship commit itself, not a merge:** v0.5.0's work merged as `b4b1c38` (PR #125) and this commit adds only the ship bookkeeping |
| `v0.5.1` | `51a8cd1d242256cb5032761188ab909aedc528ef` | 2026-10-15 | PR #133 | 0.5.1 | Patch: decks PowerPoint refused. Carries #131/#132 and the ship bookkeeping; #126 merged in PR #129, #127/#128 in PR #130 |
| `v0.6.0` | `100a9c84a2586a634057facec1ae76f07b6a4481` | 2026-10-16 | PR #134 | 0.6.0 | Lazy binary blobs and the caching audit (11 stale caches fixed, plus L1/L2). Its shipped status is recorded on the v0.7.0 branch |
| `v0.7.0` | `0db7ef1718a49c97e41fbabbf3ba096854135ba8` | 2026-10-16 | PR #135 | 0.7.0 | Cross-run text find/replace on frames, paragraphs, slides and the deck. Its shipped status is recorded on the v1.0.0 branch |

## Commands

Annotated tags, then one push:

```bash
git fetch origin main
git tag -a v0.1.0 723ef5aa0d1973844a6a1975df7648db577174cf -m "v0.1.0"
git tag -a v0.2.0 49108ffc2cbbd6d523e4dd18a093ac8a086a8a03 -m "v0.2.0 (docs only; package 0.1.0)"
git tag -a v0.3.0 0658fa51370950394501dc251d4b92a3fe841d7c -m "v0.3.0"
git tag -a v0.3.1 99e2ef72a9fb3d4b29faa4138b9750244e207d23 -m "v0.3.1"
git tag -a v0.3.2 cb8a179c3346cf75f1759c445df31f1ef244dd51 -m "v0.3.2"
git tag -a v0.4.0 aceb359ebfd89df5f51e903b8eabde501554037c -m "v0.4.0"
git tag -a v0.5.0 070704d2656a3298ec0b9a3cc4dd3e2096fffe3b -m "v0.5.0 (known PowerPoint-refusal defects; fixed in v0.5.1)"
git tag -a v0.5.1 51a8cd1d242256cb5032761188ab909aedc528ef -m "v0.5.1"
git tag -a v0.6.0 100a9c84a2586a634057facec1ae76f07b6a4481 -m "v0.6.0"
git tag -a v0.7.0 0db7ef1718a49c97e41fbabbf3ba096854135ba8 -m "v0.7.0"
git push origin v0.1.0 v0.2.0 v0.3.0 v0.3.1 v0.3.2 v0.4.0 v0.5.0 v0.5.1 v0.6.0 v0.7.0
```

A GitHub Release can then be drafted from each tag; the version cards under
`.meta/roadmap/stages/` hold the goals and acceptance for its notes.

## Keeping this current

When a version ships, add its row once the PR that marks it shipped has merged (its merge
commit is the one to tag). If that PR also carries later work, tag the ship commit itself instead,
as for v0.4.0, so the tag holds only the version. Once the tags exist on the remote, `git ls-remote --tags origin`
is the record and this file can go.
