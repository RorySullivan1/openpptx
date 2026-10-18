"""Objects used across sub-package."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from openpptx.opc.package import XmlPart
    from openpptx.types import ProvidesPart


class _Subshape:
    """Provides access to the containing part for drawing elements that occur below a shape.

    Access to the part is required for example to add or drop a relationship. Provides
    `self._parent` attribute to subclasses.
    """

    def __init__(self, parent: ProvidesPart):
        super(_Subshape, self).__init__()
        self._parent = parent

    @property
    def part(self) -> XmlPart:
        """The package part containing this object."""
        return self._parent.part
