# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Identity

- Distribution name: **`openpptx`** (PyPI, from 1.0.0; the project was called `pypptx` until then, a PyPI name an unrelated project owns). Repo: `RorySullivan1/openpptx`. Import name: **`openpptx`** too (it was `pptx`, python-pptx's name, until the 2026-10-16 rebrand). Sources live at `src/openpptx/`. Test code and user code both `from openpptx import ...`.
- Pure-Python library for reading/writing PowerPoint `.pptx` (OOXML / ECMA-376) files. No PowerPoint, no rendering engine, no runtime dependency — every feature must be expressible as an edit to XML parts inside the package's ZIP container.
- Python `>= 3.9`. Hard deps: `lxml`, `Pillow`, `XlsxWriter`, `typing_extensions`.

## Common Commands

```bash
# Install in editable mode with dev extras
pip install -e ".[dev]"

# Run the full test suite (configured in pyproject.toml -> [tool.pytest.ini_options])
pytest

# Run a single test file / class / function
pytest tests/test_slide.py
pytest tests/test_slide.py::DescribeSlide
pytest tests/test_slide.py::DescribeSlide::it_provides_access_to_its_shapes

# Coverage
pytest --cov=openpptx --cov-report=term-missing

# API docs (needs the docs extra: pip install -e ".[docs]"); -W makes any warning fatal
sphinx-build -W -b html docs docs/_build/html
```

Test discovery is non-default: classes match `Describe*`, functions match `it_*`, `and_it_*`, `but_it_*` or `test_*` (BDD style). Keep new tests in that shape or pytest will silently skip them.

## Architecture

Four layers, low to high. Each layer only depends on the ones below it.

| Layer | Where | Responsibility |
|---|---|---|
| **OPC** | `openpptx/opc/` | Open Packaging Convention — ZIP I/O, content-types, part relationships, `PackURI`. |
| **OXML** | `openpptx/oxml/` | lxml custom element classes mapped to ECMA-376 schema types. Element classes carry attribute/child accessors; the parser inflates them automatically when their tag is encountered. |
| **Parts** | `openpptx/parts/` | One class per content-type — `SlidePart`, `ChartPart`, `ImagePart`, etc. A part owns one XML element tree (or a blob) plus its outbound relationships. |
| **API** | `openpptx/api.py`, `openpptx/presentation.py`, `openpptx/slide.py`, `openpptx/shapes/`, `openpptx/text/`, `openpptx/chart/`, `openpptx/dml/`, `openpptx/table.py`, `openpptx/action.py` | User-facing Pythonic proxies. Modeled loosely on the VBA PowerPoint object model. |

Entry point is `openpptx.api.Presentation(pptx=None)` (a path or a file-like object). With no argument it loads `src/openpptx/templates/default.pptx`. The returned `Presentation` is a proxy whose `.part` is a `PresentationPart`, which owns the package graph through `openpptx.package.Package` (`OpcPackage` subclass).

### How content-types resolve to part classes

`openpptx/__init__.py` builds a `content_type → Part class` map and registers it onto `PartFactory.part_type_for`. When the package reader walks the ZIP it consults this map to instantiate the right Part subclass. **New part types must be registered here** — adding the class alone is not enough.

### Element proxy hierarchy (`openpptx/shared.py`)

- `ElementProxy` — wraps one lxml element. Equality is "same underlying element".
- `ParentedElementProxy` — adds `._parent` (and `.part` via the parent) for objects that need ancestor context (most shapes).
- `PartElementProxy` — wraps the root element of a part (e.g. a slide). Owns its `.part` directly.

Most API objects subclass one of these. Keep them as value objects — no mutable Python-side state; mutate XML instead.

### oxml / xmlchemy

`openpptx/oxml/xmlchemy.py` provides a declarative meta-system for defining custom lxml element classes (child accessors, attribute typing via `simpletypes`, choice groups). Classes are registered with `register_element_cls("ns:tag", Cls)` so the lxml parser auto-promotes elements to the right Python class on load. When adding XML support, add the element class in `openpptx/oxml/...`, register it, then build the API proxy on top — do not parse XML directly from API code.

### Units

`openpptx/util.py` defines `Length` (int subclass storing EMUs) with subclasses `Emu`, `Inches`, `Cm`, `Mm`, `Pt`, `Centipoints`. All public APIs that accept measurements take `Length` — pass `Inches(1)`, not `914400`. PowerPoint stores font sizes in centipoints internally, which is why that subclass exists.

`@lazyproperty` (in `openpptx/_util.py`, internal, so every layer can import it) is the standard cache decorator — used pervasively for derived collections (`slides`, `slide_layouts`, etc.). Prefer it over manual `_cache` attributes.

## Testing Conventions

- `tests/unitutil/mock.py` — wrappers over `unittest.mock` (`class_mock`, `instance_mock`, `method_mock`, `property_mock`). Use these rather than raw `patch()`; they auto-register teardown.
- `tests/unitutil/cxml.py` — a homegrown **C**ompact **XML** **E**xpression **L**anguage. `cxml.element("p:sp/p:nvSpPr/p:cNvPr{id=1,name=foo}")` produces a parsed lxml element. Used everywhere to build fixture XML compactly. Read the module's docstring before writing complex test XML by hand.
- Tests are organized to mirror `src/openpptx/` (e.g. `tests/oxml/`, `tests/shapes/`, `tests/parts/`).
- Round-trip tests live in `tests/test_roundtrip.py` and exercise real `.pptx` save/load cycles.

## Project Conventions

- `from __future__ import annotations` is at the top of every source file; `TYPE_CHECKING` blocks are used for proxy-class imports to avoid cycles between layers.
- `py.typed` ships with the package — keep annotations accurate; downstream users rely on them.
- The exception hierarchy in `openpptx/exc.py` (`ShapeError`, `SlideError`, `ChartError`, `TableError`, `PackageError`, etc.) is the preferred raise target inside the API layer. Avoid bare `ValueError`/`TypeError` in user-facing code paths.
- `*.pptx` is gitignored — example scripts write to the working directory and outputs are not checked in.

## Capabilities (`.claude/`)

Task-scoped **skills** (`.claude/skills/`) and isolated **agents** (`.claude/agents/`) auto-load
by their `description:` — the Python family (`python-development` / `-review` / `-maintenance` /
`-deployment`), the GitHub family, roadmap planning, and the memory / knowledge / token-economy
helpers. `@agent-python-developer` is the executor for `src/openpptx/` work. For the full inventory
of skills, agents, commands, and workflows read **`.claude/CATALOG.md`** (regenerate with
`/reindex`) — don't enumerate assets here. These assets were adopted from the claudeBrain
factory; `.claude/README.md` explains the layers.

## Reference Docs (`.claude/context/`)

- **`feature-manifest.md`** — authoritative scope/feature inventory and explicit out-of-scope
  items. Consult before proposing a feature that "PowerPoint can do" — many such features
  (rendering, slideshow, print, macro execution) are deliberately excluded.
- **`feature-gaps.md`** — granular feature-gap log with each item's OOXML schema location.
  Strategy: **bottom-up, types-first** — complete the OXML layer (element classes, simple
  types, enums) before building API wrappers on top.
- **`verification-surface.md`** — what the agent can verify itself (`pytest`, examples) vs.
  what needs a human (opening output in PowerPoint). Read before claiming work is confirmed.
- `examples/` — runnable scripts demonstrating each feature area; useful as informal smoke
  tests when changing public APIs.

## Roadmap & versioning (`.meta/`)

- **Roadmap** (`.meta/roadmap/`) — `INDEX.md` dashboard (auto-surfaced at session start)
  plus `stages/NN-<theme>/` with one card per version (Objective / Goals / Dependencies /
  Out of scope / Objectives-acceptance). Re-plan with `/roadmap-set`, reconcile with
  `/roadmap-status`. Shipped cards are history — don't edit them.
- **Version** (`.meta/version`) — the single unit of work in flight (the cursor). Start a
  version with `/version-set`, ship it with `/version-ship`; `advance-roadmap-step` drives a
  card end to end.
- **Branch per version, named `release/vX.Y.Z`** (this overrides the `claude/<label>-<slug>`
  default in `/version-set`). Not plain `vX.Y.Z`: that is the version's tag, and a branch of the
  same name makes `git push origin vX.Y.Z` ambiguous (versions up to v1.0.0 used it). Expand a
  card with implementation detail when its branch opens; don't implement a version whose card is
  still an overview.

## Memory

Decisions and state carry across sessions via the `session-memory` skill:
`.claude/memory/INDEX.md` (auto-loaded) plus append-only `.claude/memory/sessions/*.md` logs.

## Compact Instructions

On compaction, preserve: the `openpptx` name (dist and import; formerly `pypptx`/`pptx`), the four-layer
architecture and bottom-up/types-first rule, the `Describe*`/`it_*` test naming, the current
`.meta/version` cursor, and that features must be pure XML edits (no rendering engine).
