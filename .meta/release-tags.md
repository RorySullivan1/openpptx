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
| `v0.7.1` | `2627dddae28fdfa2daee0abef05b39b993e8046a` | 2026-10-16 | PR #136 | 0.7.1 | Patch: find/replace review fixes. **Already tagged on the remote** (lightweight). Its shipped status is recorded on the v1.0.0 branch |
| `v1.0.0rc1` | `2042409dfaa7276238bbdd36d13cc0cc964f59ce` | 2026-10-18 | — (on branch `v1.0.0`, before PR #137 merged) | 1.0.0rc1 | **Pushed** (annotated); published to PyPI by release run 39139591806 |
| `v1.0.0` | `146dd1ce6cd3367dfa7d980dbc6d1422b13515d5` | 2026-10-18 | PR #138 | 1.0.0 | **Pushed** (annotated); published to PyPI by release run 39140694188 |

**On the remote as of 2026-10-16** (`git ls-remote --tags origin`), all lightweight: `v0.7.1` → `2627ddd` (matches
the row above); `0.7.0` → `0db7ef1`, the v0.7.0 commit but without the `v`; `alpha` → `100a9c8`, the v0.6.0 merge.
A local-only `v0.1.0` points at `8faa9a5` (PR #48), not the `723ef5a` row above. Tidying these is the owner's call.

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
# v0.7.1 is already on the remote (lightweight, at 2627ddd)
```

A GitHub Release can then be drafted from each tag; the version cards under
`.meta/roadmap/stages/` hold the goals and acceptance for its notes.

## v1.0.0rc1: the first PyPI release

From 1.0.0 on, tags are annotated and `v`-prefixed, and **pushing one publishes it to PyPI**
(`.github/workflows/release.yml`). The workflow checks that the tag matches the version in
`pyproject.toml`, builds and checks the sdist and wheel, runs every example against the built wheel on
Python 3.9 and 3.13, and only then publishes. After publishing it creates the GitHub Release for
the tag. **A final version needs a dated `## [X.Y.Z] - YYYY-MM-DD` section in `CHANGELOG.md`**,
or the build job stops before anything is published (`.github/scripts/release_notes.py --check`). A historical `v0.x` tag above points at a commit from before
`release.yml` existed, so pushing it publishes nothing.

The release candidate is tagged on the `v1.0.0` branch, before it merges, so that a problem found in
the rc can still be fixed in the branch. `1.0.0` itself (step 5) is tagged on `main` after the merge.

Once, before the first release tag:

1. **PyPI**, logged in as `r_sullivan112`: Account settings → Publishing → *Add a new pending
   publisher*: project `openpptx`, owner `RorySullivan1`, repository `openpptx`, workflow
   `release.yml`, environment `pypi`. "Owner" is the GitHub owner, not the PyPI user; the PyPI
   account becomes the project's owner when the first release publishes.
2. **GitHub**: Settings → Environments → *New environment* `pypi`. Adding yourself as a required
   reviewer makes each publish wait for your approval in the Actions run.
3. **GitHub** (for the docs, not the release): Settings → Pages → Source: *GitHub Actions*.

Then:

```bash
git fetch origin v1.0.0
git tag -a v1.0.0rc1 2042409dfaa7276238bbdd36d13cc0cc964f59ce -m "openpptx 1.0.0rc1"
git push origin v1.0.0rc1
```

When the `release` run is green, check it from PyPI in a fresh environment:

```bash
python -m venv rc1 && rc1/bin/python -m pip install openpptx==1.0.0rc1   # rc1\Scripts\python on Windows
rc1/bin/python -c "import openpptx; print(openpptx.__version__)"         # 1.0.0rc1
```

A plain `pip install openpptx` skips a pre-release only once a final release exists. While `1.0.0rc1`
was the only version, pip 26 and uv both installed it without being asked (checked 2026-10-18).

## v1.0.0

Tagged on `main`: the merge commit of the PR that sets the version to `1.0.0`. Once it has merged:

```bash
git fetch origin main
git tag -a v1.0.0 "$(git rev-parse origin/main)" -m "openpptx 1.0.0"   # check it is the merge first
git push origin refs/tags/v1.0.0:refs/tags/v1.0.0
```

**Push a version tag by its full name.** The version's branch has the same name (`v1.0.0`), so
`git push origin v1.0.0` fails with "src refspec v1.0.0 matches more than one". A tag and a branch
can share a name on GitHub, and `release.yml` triggers on tags only.

The `release` run then waits for the `pypi` approval as rc1 did. After it publishes, a plain
`pip install openpptx` gets `1.0.0`, not the rc.

## Keeping this current

When a version ships, add its row once the PR that marks it shipped has merged (its merge
commit is the one to tag). If that PR also carries later work, tag the ship commit itself instead,
as for v0.4.0, so the tag holds only the version. Once the tags exist on the remote, `git ls-remote --tags origin`
is the record and this file can go.
