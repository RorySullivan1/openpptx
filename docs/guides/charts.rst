Charts
======

A chart is built from a chart-data object and added to a slide's shapes. openpptx writes the chart
XML and an embedded Excel workbook holding the data, so PowerPoint's Edit Data works on the result.

.. code-block:: python

    from openpptx import Presentation
    from openpptx.chart.data import CategoryChartData
    from openpptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION
    from openpptx.util import Inches

    prs = Presentation()
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    data = CategoryChartData()
    data.categories = ["Q1", "Q2", "Q3", "Q4"]
    data.add_series("North", (42, 51, 48, 60))
    data.add_series("South", (35, 39, 44, 41))

    frame = slide.shapes.add_chart(
        XL_CHART_TYPE.COLUMN_CLUSTERED, Inches(1), Inches(1), Inches(8), Inches(5), data
    )
    chart = frame.chart

``add_chart()`` returns the graphic frame holding the chart; the chart itself is ``frame.chart``.
``XL_CHART_TYPE`` lists the bar, column, line, pie, doughnut, area, scatter, bubble, radar, stock and
surface families and their 3D variants. Scatter and bubble charts take ``XyChartData`` and
``BubbleChartData`` instead.

Titles, legends and axes
------------------------

.. code-block:: python

    chart.has_title = True
    chart.chart_title.text_frame.text = "Units sold"

    chart.has_legend = True
    chart.legend.position = XL_LEGEND_POSITION.BOTTOM
    chart.legend.include_in_layout = False

    value_axis = chart.value_axis
    value_axis.maximum_scale = 80
    value_axis.has_major_gridlines = True
    value_axis.tick_labels.number_format = "0"
    value_axis.tick_labels.number_format_is_linked = False

Data labels and series
----------------------

Data labels can be set for a whole plot, a series or a single point. A series also carries its own
fill and line, trendlines and error bars:

.. code-block:: python

    from openpptx.dml.color import RGBColor
    from openpptx.enum.chart import XL_LABEL_POSITION, XL_TRENDLINE_TYPE

    plot = chart.plots[0]
    plot.has_data_labels = True
    plot.data_labels.show_value = True
    plot.data_labels.position = XL_LABEL_POSITION.OUTSIDE_END

    north = plot.series[0]
    north.format.fill.solid()
    north.format.fill.fore_color.rgb = RGBColor(0x1F, 0x77, 0xB4)

    trend = north.trendlines.add(XL_TRENDLINE_TYPE.LINEAR)
    trend.display_r_squared = True

Combining chart types
---------------------

``add_plot()`` adds an empty line, bar, area or scatter plot to the chart, on a secondary axis by
default, to make a combo chart:

.. code-block:: python

    line_plot = chart.add_plot("line", use_secondary_axis=True)
    print([p.__class__.__name__ for p in chart.plots])

openpptx has no call yet that moves a series from one plot to another.
``add_chart_secondary_axis.py`` in ``examples/`` shows how to do it by moving the series' XML.

Changing the data
-----------------

``replace_data()`` swaps the categories and series for new ones, keeping the chart's formatting
where the series still exist:

.. code-block:: python

    data = CategoryChartData()
    data.categories = ["Q1", "Q2", "Q3", "Q4"]
    data.add_series("North", (44, 50, 52, 63))
    data.add_series("South", (36, 40, 43, 47))
    chart.replace_data(data)
    print(chart.plots[0].series[0].values)

Office 2016 charts
------------------

Waterfall, histogram, box and whisker, treemap, sunburst and funnel charts use a newer chart format
("chartex"). They are added the same way, from ``CategoryChartData``. Their data is read-only once
the chart exists, and their styling is not supported:

.. code-block:: python

    cash = CategoryChartData()
    cash.categories = ["Opening", "Sales", "Costs", "Closing"]
    cash.add_series("Cash flow", (120, 85, -95, 110))

    slide = prs.slides.add_slide(prs.slide_layouts[6])
    waterfall = slide.shapes.add_chart(
        XL_CHART_TYPE.WATERFALL, Inches(1), Inches(1), Inches(8), Inches(5), cash
    )
    print(waterfall.has_chart, waterfall.chartex.chart_type)
    print(waterfall.chartex.series[0].values)

    prs.save("charts.pptx")

A chartex chart is reached through ``chartex`` rather than ``chart``. Any chartex chart in a file
you open can be read this way, Pareto and region-map charts included.

See ``add_chart.py``, ``add_chart_secondary_axis.py``, ``chart_trendlines_error_bars.py``,
``chart_3d_view.py`` and ``modern_charts.py`` in ``examples/`` for complete scripts.
