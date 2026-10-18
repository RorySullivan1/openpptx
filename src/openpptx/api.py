"""Directly exposed API classes, Presentation for now.

Provides some syntactic sugar for interacting with the openpptx.presentation.Package graph and also
provides some insulation so not so many classes in the other modules need to be named as internal
(leading underscore).
"""

from __future__ import annotations

import os
from typing import IO, TYPE_CHECKING

from openpptx.exc import PackageError
from openpptx.opc.constants import CONTENT_TYPE as CT
from openpptx.package import Package

if TYPE_CHECKING:
    from openpptx import presentation
    from openpptx.parts.presentation import PresentationPart


def Presentation(pptx: str | IO[bytes] | None = None) -> presentation.Presentation:
    """
    Return a |Presentation| object loaded from *pptx*, where *pptx* can be
    either a path to a ``.pptx`` file (a string) or a file-like object. If
    *pptx* is missing or ``None``, the built-in default presentation
    "template" is loaded.

    Opened from a path, the file is not held open, but images, media and other
    binary parts are read from it only when they are used, such as when the
    presentation is saved. So the file must not be replaced or deleted while the
    presentation still needs it; reading such a part then raises |PackageError|.
    Saving back over the same file by its path is fine, but opening that file for
    writing yourself, e.g. ``prs.save(open(path, "wb"))``, empties it before its
    parts can be read. A file-like object is read in full when it is opened, so it
    can be closed straight away.
    """
    if pptx is None:
        pptx = _default_pptx_path()

    presentation_part = Package.open(pptx).main_document_part

    if not _is_pptx_package(presentation_part):
        tmpl = "file '%s' is not a PowerPoint file, content type is '%s'"
        raise PackageError(tmpl % (pptx, presentation_part.content_type))

    return presentation_part.presentation


def _default_pptx_path() -> str:
    """Return the path to the built-in default .pptx package."""
    _thisdir = os.path.split(__file__)[0]
    return os.path.join(_thisdir, "templates", "default.pptx")


def _is_pptx_package(prs_part: PresentationPart):
    """Return |True| if *prs_part* is a valid main document part, |False| otherwise."""
    valid_content_types = (CT.PML_PRESENTATION_MAIN, CT.PML_PRES_MACRO_MAIN, CT.PML_TEMPLATE_MAIN)
    return prs_part.content_type in valid_content_types
