"""Unit-test suite for `openpptx.chart._text`."""

from __future__ import annotations

import pytest

from openpptx import Presentation
from openpptx.chart.data import CategoryChartData
from openpptx.enum.chart import XL_CHART_TYPE
from openpptx.exc import ChartError


class DescribeChartText:
    """Text frames in a chart cannot reach the chart part."""

    @pytest.mark.parametrize("text_frame_of", ["chart_title", "axis_title", "data_label"])
    def it_raises_ChartError_for_a_hyperlink_in_chart_text(self, text_frame_of: str):
        prs = Presentation()
        slide = prs.slides.add_slide(prs.slide_layouts[6])
        data = CategoryChartData()
        data.categories = ["a", "b"]
        data.add_series("s", (1, 2))
        chart = slide.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, 0, 0, 9, 9, data).chart
        text_frame = {
            "chart_title": lambda: chart.chart_title.text_frame,
            "axis_title": lambda: chart.value_axis.axis_title.text_frame,
            "data_label": lambda: chart.plots[0].series[0].points[0].data_label.text_frame,
        }[text_frame_of]()
        text_frame.text = "Title"
        run = text_frame.paragraphs[0].runs[0]

        assert run.hyperlink.address is None
        with pytest.raises(ChartError, match="hyperlink in the text of a chart"):
            run.hyperlink.address = "https://example.com"
