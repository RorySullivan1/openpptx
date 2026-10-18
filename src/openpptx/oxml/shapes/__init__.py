"""Base shape-related objects such as BaseShape."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing_extensions import TypeAlias

    from openpptx.oxml.shapes.autoshape import CT_Shape
    from openpptx.oxml.shapes.connector import CT_Connector
    from openpptx.oxml.shapes.graphfrm import CT_GraphicalObjectFrame
    from openpptx.oxml.shapes.groupshape import CT_GroupShape
    from openpptx.oxml.shapes.picture import CT_Picture


ShapeElement: TypeAlias = (
    "CT_Connector | CT_GraphicalObjectFrame |  CT_GroupShape | CT_Picture | CT_Shape"
)
