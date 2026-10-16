"""Chartex part: an Office 2016+ chart (waterfall, histogram, treemap, ...) and its workbook."""

from __future__ import annotations

from typing import TYPE_CHECKING, cast

from openpptx.chart.chartex import ChartEx
from openpptx.enum.chart import XL_CHART_TYPE
from openpptx.opc.constants import CONTENT_TYPE as CT
from openpptx.opc.constants import RELATIONSHIP_TYPE as RT
from openpptx.opc.package import LazyXmlPart, XmlPart
from openpptx.oxml import parse_from_template, parse_xml
from openpptx.oxml.ns import qn
from openpptx.parts.embeddedpackage import EmbeddedXlsxPart

if TYPE_CHECKING:
    from openpptx.chart.data import CategoryChartData
    from openpptx.oxml.chart.chartex import CT_ChartExSpace
    from openpptx.package import Package


class ChartExPart(LazyXmlPart):
    """A chartex part, e.g. ``/ppt/charts/chartEx1.xml``, holding a `cx:chartSpace`.

    Loaded lazily (see |LazyXmlPart|), so a chartex chart that is opened and re-saved without
    being read writes its bytes back unchanged.
    """

    partname_template = "/ppt/charts/chartEx%d.xml"

    @classmethod
    def new(
        cls, chart_type: XL_CHART_TYPE, chart_data: CategoryChartData, package: Package
    ) -> ChartExPart:
        """Return a new |ChartExPart| depicting `chart_data` as a chart of `chart_type`.

        The chart's data is also written to a new embedded workbook related to the part, so the
        chart can be edited in PowerPoint. The part also gets the chart-style and color-style
        parts PowerPoint requires of every chartex chart; it refuses a deck lacking either.
        """
        from openpptx.chart.chartexwriter import ChartExWorkbookWriter, ChartExXmlWriter

        chart_part = cls.load(
            package.next_partname(cls.partname_template),
            CT.OFC_CHART_EX,
            package,
            ChartExXmlWriter(chart_type, chart_data).xml.encode("utf-8"),
        )
        xlsx_part = EmbeddedXlsxPart.new(ChartExWorkbookWriter(chart_data).xlsx_blob, package)
        rId = chart_part.relate_to(xlsx_part, RT.PACKAGE)
        chartData = chart_part.chartSpace.get_or_add_chartData()
        externalData = chartData.get_or_add_externalData()
        externalData.rId = rId
        externalData.set(qn("cx:autoUpdate"), "0")
        chart_part._add_style_part(chart_type)
        chart_part._add_colors_part()
        return chart_part

    def ensure_style_parts(self) -> None:
        """Add the chart-style and color-style parts PowerPoint requires, where either is missing.

        PowerPoint refuses a deck whose chartex chart lacks either part, and openpptx 0.5.0 and
        earlier wrote neither. Only relationships change: the chart type is read from a throwaway
        parse of the blob, so a chart that was never read still saves its original bytes.
        """
        reltypes = {rel.reltype for rel in self.rels.values()}
        if RT.CHART_STYLE not in reltypes:
            chartSpace = cast("CT_ChartExSpace", parse_xml(self.blob))
            self._add_style_part(ChartEx(chartSpace, self).chart_type)
        if RT.CHART_COLOR_STYLE not in reltypes:
            self._add_colors_part()

    @property
    def chartex(self) -> ChartEx:
        """|ChartEx| object giving read access to the chart in this part."""
        return ChartEx(self.chartSpace, self)

    @property
    def chartSpace(self) -> CT_ChartExSpace:
        """The `cx:chartSpace` root element of this part (parsed on first access)."""
        return cast("CT_ChartExSpace", self._element)

    def _add_colors_part(self) -> None:
        """Relate a new color-style part to this chart: the one PowerPoint writes for every type."""
        package = self.package
        colors_part = XmlPart(
            package.next_partname("/ppt/charts/colors%d.xml"),
            CT.OFC_CHART_COLORS,
            package,
            parse_from_template("chartex_colors"),
        )
        self.relate_to(colors_part, RT.CHART_COLOR_STYLE)

    def _add_style_part(self, chart_type: XL_CHART_TYPE | None) -> None:
        """Relate a new chart-style part to this chart, chosen for a chart of `chart_type`."""
        package = self.package
        style_part = XmlPart(
            package.next_partname("/ppt/charts/style%d.xml"),
            CT.OFC_CHART_STYLE,
            package,
            parse_from_template(_style_template_name(chart_type)),
        )
        self.relate_to(style_part, RT.CHART_STYLE)

    @property
    def xlsx_part(self) -> EmbeddedXlsxPart | None:
        """The embedded workbook holding this chart's data, or |None| if it has none."""
        rId = self.chartSpace.xlsx_part_rId
        return None if rId is None else cast(EmbeddedXlsxPart, self.related_part(rId))


# -- chart types with a style template captured from PowerPoint 16 --
_STYLED_CHART_TYPES = frozenset(
    (
        XL_CHART_TYPE.BOX_WHISKER,
        XL_CHART_TYPE.FUNNEL,
        XL_CHART_TYPE.HISTOGRAM,
        XL_CHART_TYPE.SUNBURST,
        XL_CHART_TYPE.TREEMAP,
        XL_CHART_TYPE.WATERFALL,
    )
)


def _style_template_name(chart_type: XL_CHART_TYPE | None) -> str:
    """Return the name of the chart-style template for a chartex chart of `chart_type`.

    `src/openpptx/templates/` holds the style PowerPoint 16 writes for a new chart of each type
    openpptx can create: `chartex_style_<type>` for waterfall, histogram, box_whisker, treemap,
    sunburst and funnel. A chart loaded from a deck may be another type (`PARETO`, `REGION_MAP`)
    or unrecognized (|None|), and it still needs a style, or PowerPoint refuses the deck.
    """
    if chart_type in _STYLED_CHART_TYPES:
        return "chartex_style_%s" % chart_type.name.lower()
    # -- a Pareto chart is a histogram series plus a line, so the histogram style fits it; it is
    # -- also the plainest style, so any other chart falls back to it too --
    return "chartex_style_histogram"
