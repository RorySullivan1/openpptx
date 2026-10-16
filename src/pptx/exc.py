"""Exceptions used with openpptx.

The base exception class is |OpenPptxError|; every exception openpptx raises deliberately derives
from it, so ``except OpenPptxError`` catches them all.

Several classes also derive from a builtin exception. The API used to raise plain
``ValueError`` / ``TypeError`` in these cases, and callers written against that keep working:
``except ValueError`` still catches a |ShapeError|, |SlideError|, |ChartError|, |TableError|
or |InvalidValueError|, and ``except TypeError`` still catches an |InvalidTypeError|.

``PyPptxError``, the base class's name before the project became openpptx, is a deprecated
alias of |OpenPptxError|: it is the same class, and importing it emits a ``DeprecationWarning``.
"""

from __future__ import annotations

import warnings
from typing import TYPE_CHECKING


class OpenPptxError(Exception):
    """Generic error class."""


if TYPE_CHECKING:
    PyPptxError = OpenPptxError


def __getattr__(name: str) -> type[OpenPptxError]:
    """Resolve the deprecated alias `PyPptxError`, warning the caller to use the new name."""
    if name == "PyPptxError":
        warnings.warn(
            "PyPptxError is deprecated; use OpenPptxError (the same class)",
            DeprecationWarning,
            stacklevel=2,
        )
        return OpenPptxError
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


class PackageNotFoundError(OpenPptxError):
    """Raised when a package cannot be found at the specified path."""


class InvalidXmlError(OpenPptxError):
    """Raised when invalid XML is encountered according to the OOXML schema."""


class InvalidValueError(OpenPptxError, ValueError):
    """Raised when a value is of an acceptable type but out of range or otherwise invalid.

    Also a ``ValueError``, which is what the API raised for these cases before.
    """


class InvalidTypeError(OpenPptxError, TypeError):
    """Raised when a value is of the wrong type for the property or parameter it is given to.

    Also a ``TypeError``, which is what the API raised for these cases before.
    """


class ShapeError(OpenPptxError, ValueError):
    """Raised for shape operation failures (type mismatch, invalid state).

    Also a ``ValueError``, which is what the API raised for these cases before.
    """


class SlideError(OpenPptxError, ValueError):
    """Raised for slide collection and management failures.

    Also a ``ValueError``, which is what the API raised for these cases before.
    """


class ChartError(OpenPptxError, ValueError):
    """Raised for chart-specific operation failures.

    Also a ``ValueError``, which is what the API raised for these cases before.
    """


class UnsupportedEffectError(ShapeError, NotImplementedError, AttributeError):
    """Raised when a shape has nowhere to hold a visual effect or 3D formatting.

    For example a group's `three_d`, or the shadow of a graphic frame holding SmartArt. Also a
    ``NotImplementedError`` and an ``AttributeError``, which these properties raised before, so
    ``hasattr(shape, "three_d")`` is still False for such a shape.
    """


class TableError(OpenPptxError, ValueError):
    """Raised for table operation failures (cell access, merge).

    Also a ``ValueError``, which is what the API raised for these cases before.
    """


class PackageError(OpenPptxError):
    """Raised for OPC package, relationship, or content-type errors."""


class InvalidPackageError(PackageError):
    """Raised when a file or stream exists but is not a readable `.pptx` package.

    For example, it is not a zip archive, the archive is truncated or corrupt, or it lacks the
    `[Content_Types].xml` every package must have. A path that does not exist raises
    |PackageNotFoundError| instead.
    """
