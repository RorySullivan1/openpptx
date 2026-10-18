Shapes
======

Everything on a slide is a shape in ``slide.shapes``: autoshapes and text boxes, pictures, tables,
charts, connectors, groups and freeforms. Positions and sizes are lengths in EMUs; pass
``Inches()``, ``Cm()`` or ``Pt()`` rather than raw numbers.

.. code-block:: python

    from openpptx import Presentation
    from openpptx.util import Inches, Pt

    prs = Presentation()
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # Blank
    shapes = slide.shapes

Autoshapes and text boxes
-------------------------

``add_shape()`` takes one of the 180-odd preset geometries in ``MSO_SHAPE``. Some presets have
adjustment handles, which ``adjustments`` exposes as fractions:

.. code-block:: python

    from openpptx.enum.shapes import MSO_SHAPE

    box = shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1), Inches(1), Inches(3), Inches(1.5))
    box.text = "Rounded box"
    box.adjustments[0] = 0.25
    box.name = "Callout box"

    note = shapes.add_textbox(Inches(5), Inches(1), Inches(3), Inches(1))
    note.text_frame.text = "A plain text box"

Every shape has a position, size, rotation and name, and the accessibility text PowerPoint reads
aloud:

.. code-block:: python

    box.left = Inches(0.5)
    box.rotation = 10
    box.alternative_text = "A rounded box with a short label"
    print(box.shape_id, box.name, box.width.inches)

Pictures
--------

A picture is added from a path or a file-like object. Give one of width and height to scale it,
keeping its aspect ratio, or neither for its native size. Cropping is a fraction of each edge:

.. code-block:: python

    picture = shapes.add_picture("logo.png", Inches(1), Inches(3), width=Inches(2))
    picture.crop_right = 0.1
    print(picture.image.content_type, picture.image.size)

Tables
------

``add_table()`` returns a graphic frame; the table is its ``table``. Cells merge and split, and
rows and columns can be added and removed after the table exists:

.. code-block:: python

    frame = shapes.add_table(3, 3, Inches(4), Inches(3), Inches(5), Inches(1.5))
    table = frame.table
    table.cell(0, 0).text = "Region"
    table.cell(0, 1).text = "Q3"
    table.cell(0, 2).text = "Q4"
    table.cell(1, 0).text = "North"

    table.cell(2, 0).merge(table.cell(2, 2))
    table.cell(2, 0).text = "Merged across the row"

    new_row = table.rows.add()
    table.columns.remove(table.columns[2])

Connectors and groups
---------------------

A connector can be attached to a shape's connection points, so it follows the shape when it moves
in PowerPoint. Grouping takes existing shapes into a new group:

.. code-block:: python

    from openpptx.enum.shapes import MSO_CONNECTOR

    a = shapes.add_shape(MSO_SHAPE.OVAL, Inches(1), Inches(5), Inches(1), Inches(1))
    b = shapes.add_shape(MSO_SHAPE.OVAL, Inches(4), Inches(5.5), Inches(1), Inches(1))
    line = shapes.add_connector(MSO_CONNECTOR.ELBOW, 0, 0, 0, 0)
    line.begin_connect(a, 3)
    line.end_connect(b, 1)

    group = shapes.add_group_shape([a, b, line])
    print(len(group.shapes))

Freeforms
---------

A freeform is drawn with a builder, in local coordinates scaled to the slide:

.. code-block:: python

    builder = shapes.build_freeform(0, 0, scale=Inches(1) / 100)
    builder.add_line_segments([(100, 0), (50, 80)], close=True)
    triangle = builder.convert_to_shape(Inches(6), Inches(5))

Stacking order and many shapes at once
--------------------------------------

The order of ``slide.shapes`` is the stacking order, back to front. A shape range applies one
change to several shapes, such as aligning them:

.. code-block:: python

    shapes.move_shape_to_front(box)
    shapes.move_shape_to_back(note)

    shapes.shape_range([box, note, picture]).align_left()
    print(box.left == note.left == picture.left)

    prs.save("shapes.pptx")

Placeholders
------------

A slide made from a layout has placeholders that inherit position and formatting from the layout.
``slide.placeholders`` reaches them by their ``idx``, and a picture, chart or table placeholder can
be filled in place:

.. code-block:: python

    slide = prs.slides.add_slide(prs.slide_layouts[8])  # Picture with Caption
    for placeholder in slide.placeholders:
        print(placeholder.placeholder_format.idx, placeholder.placeholder_format.type)
    slide.placeholders[1].insert_picture("photo.jpg")

See ``add_picture.py``, ``add_table.py``, ``shapes_and_fills.py`` and
``connectors_and_groups.py`` in ``examples/`` for complete scripts.
