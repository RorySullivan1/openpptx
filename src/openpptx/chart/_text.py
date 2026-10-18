"""The parent of a text frame inside a chart: a title, an axis title or a data label."""

from __future__ import annotations

from typing import TYPE_CHECKING, NoReturn

from openpptx.exc import ChartError

if TYPE_CHECKING:
    from openpptx.opc.package import XmlPart


class _ChartTextParent:
    """Stands in for the part of chart text, which these objects cannot reach.

    A text frame asks its parent for the part only to read or write a relationship, which only a
    hyperlink needs. The chart objects that hold text are built from their XML element alone, so
    the chart part is out of reach; a hyperlink in chart text raises |ChartError| rather than an
    `AttributeError`.
    """

    @property
    def part(self) -> XmlPart:
        return self._unreachable()

    @staticmethod
    def _unreachable() -> NoReturn:
        raise ChartError("openpptx cannot read or set a hyperlink in the text of a chart")


CHART_TEXT_PARENT = _ChartTextParent()
