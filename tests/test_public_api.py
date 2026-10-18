"""The public API contract: every public name, recorded so a change to the surface is deliberate.

`docs/stability.rst` defines the surface. The public modules are the ones the API reference
documents, so the reference and this test cannot disagree about what is public. Regenerate the
record after an intended change with ``python -m tests.test_public_api`` from the repository root
(run as a script, ``tests/enum`` would shadow the standard library's ``enum``).
"""

from __future__ import annotations

import ast
import enum
import importlib
import inspect
import os
import pkgutil
import re
import sys
from types import ModuleType

import openpptx

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(TESTS_DIR)
DOCS_DIR = os.path.join(ROOT_DIR, "docs")
SNAPSHOT_PATH = os.path.join(TESTS_DIR, "test_files", "public_api.txt")

INTERNAL_PACKAGES = ("openpptx.oxml", "openpptx.opc", "openpptx.parts")
"""Packages that are internal as a whole; `docs/stability.rst` says so."""

INTERNAL_MODULES = (
    "openpptx.chart.chartexwriter",
    "openpptx.chart.xlsx",
    "openpptx.chart.xmlwriter",
    "openpptx.enum.base",
    "openpptx.media",
    "openpptx.package",
    "openpptx.shared",
    "openpptx.spec",
    "openpptx.text.fonts",
    "openpptx.text.layout",
    "openpptx.types",
)
"""API-layer modules that serve the implementation; `docs/stability.rst` lists them."""


class DescribePublicApi:
    """The public names and the modules that hold them."""

    def it_records_every_public_name(self):
        expected = _read_snapshot()
        actual = _public_names()

        added = sorted(set(actual) - set(expected))
        removed = sorted(set(expected) - set(actual))
        assert not (added or removed), (
            "the public API changed; if that is intended, run `python -m tests.test_public_api` "
            "and commit tests/test_files/public_api.txt with the change\n"
            + "".join("  + %s\n" % name for name in added)
            + "".join("  - %s\n" % name for name in removed)
        )

    def it_documents_or_declares_internal_every_api_module(self):
        documented = _documented_modules()
        undecided = [
            name
            for name in _api_layer_modules()
            # -- the package itself: its two public names are recorded explicitly --
            if name != "openpptx"
            and name not in documented
            and not _is_internal_module(name)
            and _module_level_names(importlib.import_module(name))
        ]
        assert not undecided, (
            "each module needs an entry in docs/api/ or a place in INTERNAL_MODULES and the "
            "internal list in docs/stability.rst: %s" % ", ".join(undecided)
        )

    def and_it_matches_the_internal_list_on_the_stability_page(self):
        with open(os.path.join(DOCS_DIR, "stability.rst"), encoding="utf-8") as f:
            page = f.read()
        listed = set(re.findall(r"^\s+- ``(openpptx\.[\w.]+)``$", page, re.MULTILINE))
        assert listed == set(INTERNAL_MODULES)
        for package in INTERNAL_PACKAGES:
            assert "``%s``" % package in page

    def and_it_lists_only_real_members_for_a_class_whose_members_it_names(self):
        for target, members in _explicit_members().items():
            module_name, class_name = target.rsplit(".", 1)
            cls = getattr(importlib.import_module(module_name), class_name)
            assert [m for m in members if not hasattr(cls, m)] == [], target

    def but_it_documents_no_internal_module(self):
        documented = _documented_modules()
        assert not [name for name in documented if _is_internal_module(name)]


# -- the surface ---------------------------------------------------------------------------------


def _public_names() -> list[str]:
    """Sorted dotted name of everything public: module-level names, class members, enum members."""
    names: set[str] = {"openpptx.Presentation", "openpptx.__version__"}

    for module_name in sorted(_documented_modules() | {"openpptx.exc"}):
        module = importlib.import_module(module_name)
        for name in _module_level_names(module):
            names.add("%s.%s" % (module_name, name))
            obj = getattr(module, name)
            # -- an alias such as `MSO_FILL = MSO_FILL_TYPE` adds its own name, not its members --
            if inspect.isclass(obj) and obj.__name__ == name and obj.__module__ == module_name:
                names.update("%s.%s.%s" % (module_name, name, m) for m in _class_members(obj))

    explicit = _explicit_members()
    for cls in _documented_classes():
        qualname = "%s.%s" % (cls.__module__, cls.__name__)
        names.add(qualname)
        members = explicit.get(qualname)
        names.update("%s.%s" % (qualname, m) for m in members or _class_members(cls))

    return sorted(names)


def _module_level_names(module: ModuleType) -> list[str]:
    """Public names `module` defines itself (not imports), plus any listed in its `__all__`."""
    if module.__file__ is None or not module.__file__.endswith(".py"):
        return []
    with open(module.__file__, encoding="utf-8") as f:
        tree = ast.parse(f.read())

    defined: set[str] = set()

    def visit(body: list[ast.stmt]) -> None:
        for node in body:
            if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
                defined.add(node.name)
            elif isinstance(node, ast.Assign):
                for target in node.targets:
                    for leaf in ast.walk(target):
                        if isinstance(leaf, ast.Name):
                            defined.add(leaf.id)
            elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
                defined.add(node.target.id)
            elif isinstance(node, ast.If):
                visit(node.body)
                visit(node.orelse)
            elif isinstance(node, ast.Try):
                visit(node.body)
                for handler in node.handlers:
                    visit(handler.body)
                visit(node.orelse)

    visit(tree.body)
    defined.update(getattr(module, "__all__", ()))
    return sorted(
        name for name in defined if not name.startswith("_") and hasattr(module, name)
    )


def _class_members(cls: type) -> list[str]:
    """Public members of `cls`: its own, and those inherited from openpptx classes not internal.

    Members inherited from the standard library, a dependency or an internal module (the package
    machinery behind a `Part`, say) are not part of the contract.
    """
    documented = set(_documented_classes())
    members: set[str] = set()
    for name in dir(cls):
        if name.startswith("_"):
            continue
        owner = next((base for base in cls.__mro__ if name in vars(base)), None)
        if owner is None:
            continue
        if owner is cls or owner in documented or _is_public_owner(owner):
            members.add(name)
    if issubclass(cls, enum.Enum):
        members.update(name for name in cls.__members__ if not name.startswith("_"))
    return sorted(members)


def _is_public_owner(owner: type) -> bool:
    module = owner.__module__
    return module.startswith("openpptx.") and not _is_internal_module(module)


# -- modules -------------------------------------------------------------------------------------


def _api_layer_modules() -> list[str]:
    """Every module in the package outside the internal oxml/opc/parts layers."""
    return sorted(
        name
        for name in ["openpptx"]
        + [info.name for info in pkgutil.walk_packages(openpptx.__path__, prefix="openpptx.")]
        if not any(name == p or name.startswith(p + ".") for p in INTERNAL_PACKAGES)
    )


def _is_internal_module(name: str) -> bool:
    """True for a module internal by policy: listed, in an internal package, or underscored."""
    return (
        name in INTERNAL_MODULES
        or any(name == p or name.startswith(p + ".") for p in INTERNAL_PACKAGES)
        or any(part.startswith("_") for part in name.split("."))
    )


def _reference_text() -> str:
    api_dir = os.path.join(DOCS_DIR, "api")
    text = ""
    for filename in sorted(os.listdir(api_dir)):
        if filename.endswith(".rst"):
            with open(os.path.join(api_dir, filename), encoding="utf-8") as f:
                text += f.read() + "\n"
    return text


def _directive_targets(directive: str) -> list[str]:
    """Targets of every `.. <directive>::` in the API reference pages."""
    return re.findall(r"^\.\. %s:: (\S+)$" % directive, _reference_text(), re.MULTILINE)


def _explicit_members() -> dict[str, list[str]]:
    """`autoclass` target -> the members its `:members:` option names, where it names them.

    A class from an internal module lists the members the contract covers this way, so its
    package machinery stays out of both the reference and the record.
    """
    found: dict[str, list[str]] = {}
    pattern = r"^\.\. autoclass:: (\S+)\n   :members: (.+(?:\n      .+)*)"
    for target, members in re.findall(pattern, _reference_text(), re.MULTILINE):
        found[target] = [m.strip() for m in members.replace("\n", " ").split(",")]
    return found


def _documented_modules() -> set[str]:
    """Modules the reference documents: by `automodule`, or by `autoclass` of a class in them."""
    modules = set(_directive_targets("automodule"))
    for target in _directive_targets("autoclass"):
        module_name = target.rsplit(".", 1)[0]
        if not _is_internal_module(module_name):
            modules.add(module_name)
    return modules


def _documented_classes() -> list[type]:
    """Classes the reference documents with `autoclass`: private, internal-module or enum ones."""
    classes: list[type] = []
    for target in _directive_targets("autoclass"):
        module_name, class_name = target.rsplit(".", 1)
        classes.append(getattr(importlib.import_module(module_name), class_name))
    return classes


# -- the record ----------------------------------------------------------------------------------


def _read_snapshot() -> list[str]:
    with open(SNAPSHOT_PATH, encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip() and not line.startswith("#")]


def _write_snapshot() -> int:
    names = _public_names()
    with open(SNAPSHOT_PATH, "w", encoding="utf-8", newline="\n") as f:
        f.write("# The public API of openpptx, one dotted name per line. Generated by\n")
        f.write("# `python -m tests.test_public_api`; see docs/stability.rst.\n")
        f.writelines(name + "\n" for name in names)
    return len(names)


if __name__ == "__main__":
    print("wrote %d names to %s" % (_write_snapshot(), os.path.relpath(SNAPSHOT_PATH, ROOT_DIR)))
    sys.exit(0)
