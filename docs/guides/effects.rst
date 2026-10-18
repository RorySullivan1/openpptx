Fills, lines and effects
========================

A shape's appearance is its fill, its outline and any visual effects: shadow, glow, reflection,
soft edges and 3D. Each is a property object on the shape; setting a value writes the XML for it.

.. code-block:: python

    from openpptx import Presentation
    from openpptx.dml.color import RGBColor
    from openpptx.enum.shapes import MSO_SHAPE
    from openpptx.util import Inches, Pt

    prs = Presentation()
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    def add_box(left, top):
        return slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(2.5), Inches(1.5)
        )

Colour
------

A colour is either an RGB value or a theme colour. A theme colour follows the deck's theme, so it
changes when the theme does; ``brightness`` lightens or darkens it, from -1.0 to 1.0:

.. code-block:: python

    from openpptx.enum.dml import MSO_THEME_COLOR

    solid = add_box(0.5, 0.5)
    solid.fill.solid()
    solid.fill.fore_color.rgb = RGBColor(0x2E, 0x86, 0xC1)

    themed = add_box(3.5, 0.5)
    themed.fill.solid()
    themed.fill.fore_color.theme_color = MSO_THEME_COLOR.ACCENT_2
    themed.fill.fore_color.brightness = 0.4

Fills
-----

Besides solid, a fill can be a gradient, a pattern, a picture, or nothing:

.. code-block:: python

    from openpptx.enum.dml import MSO_PATTERN

    gradient = add_box(6.5, 0.5)
    gradient.fill.gradient()
    gradient.fill.gradient_angle = 90
    stops = gradient.fill.gradient_stops
    stops[0].color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
    stops[1].color.rgb = RGBColor(0x2E, 0x86, 0xC1)

    patterned = add_box(0.5, 2.5)
    patterned.fill.patterned()
    patterned.fill.pattern = MSO_PATTERN.WIDE_UPWARD_DIAGONAL
    patterned.fill.fore_color.rgb = RGBColor(0x2E, 0x86, 0xC1)

    pictured = add_box(3.5, 2.5)
    pictured.fill.picture("logo.png")

    empty = add_box(6.5, 2.5)
    empty.fill.background()

Lines
-----

The outline has a width, colour and dash style, and a connector or line shape can have arrowheads:

.. code-block:: python

    from openpptx.enum.dml import MSO_LINE_DASH_STYLE

    empty.line.width = Pt(2.5)
    empty.line.color.rgb = RGBColor(0x2E, 0x86, 0xC1)
    empty.line.dash_style = MSO_LINE_DASH_STYLE.DASH

Effects
-------

Shadow, glow, reflection and soft edges each have their own format object:

.. code-block:: python

    shadowed = add_box(0.5, 4.5)
    shadow = shadowed.shadow
    shadow.blur_radius = Pt(8)
    shadow.distance = Pt(5)
    shadow.direction = 315
    shadow.color.rgb = RGBColor(0x00, 0x00, 0x00)

    glowing = add_box(3.5, 4.5)
    glowing.glow.radius = Pt(10)
    glowing.glow.color.rgb = RGBColor(0xF1, 0xC4, 0x0F)

    soft = add_box(6.5, 4.5)
    soft.soft_edge.radius = Pt(12)

    print(shadow.blur_radius.pt, glowing.glow.radius.pt)

``shadow.inherit`` tells you whether a shape still takes its effects from the theme. Setting it to
``False`` on a shape that inherits them turns the theme's shadow off; setting it to ``True`` removes
every effect set on the shape, glow and reflection included, and inherits again.

3D
--

``three_d`` gives a shape depth, a bevel and a material; its ``scene`` holds the camera and the
lighting:

.. code-block:: python

    from openpptx.enum.dml import MSO_BEVEL_PRESET

    raised = add_box(0.5, 6)
    bevel = raised.three_d.get_or_add_bevel_top()
    bevel.preset = MSO_BEVEL_PRESET.CIRCLE
    bevel.width = Pt(8)
    bevel.height = Pt(4)
    raised.three_d.extrusion_height = Pt(6)

Pictures
--------

A picture has its own adjustments, as PowerPoint's Picture Format tab sets them:

.. code-block:: python

    picture = slide.shapes.add_picture("photo.jpg", Inches(6.5), Inches(6), height=Inches(1.2))
    picture.brightness = 0.2
    picture.contrast = -0.1
    picture.is_grayscale = True

    prs.save("effects.pptx")

See ``shapes_and_fills.py``, ``shape_effects.py`` and ``picture_effects.py`` in ``examples/`` for
complete scripts.
