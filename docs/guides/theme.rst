Themes and masters
==================

A slide master carries the theme: twelve colour slots, a heading and a body font, and the fill,
line and effect styles PowerPoint offers in its style galleries. Layouts take their look from the
master, and slides from their layout.

.. code-block:: python

    from openpptx import Presentation

    prs = Presentation()
    master = prs.slide_masters[0]
    theme = master.theme
    print(theme.name)

Colours and fonts
-----------------

The colour scheme gives each slot as an RGB hex string. The font scheme has a major (headings) and a
minor (body) font, each with Latin, East Asian and complex-script typefaces:

.. code-block:: python

    colors = theme.color_scheme
    print(colors.accent_1, colors["dk1"])
    for slot, rgb in colors:
        print(slot, rgb)

    fonts = theme.font_scheme
    print(fonts.major_font.latin, fonts.minor_font.latin)

Shapes that use a theme colour (``MSO_THEME_COLOR.ACCENT_1``, say) or a theme font (``"+mj-lt"`` for
the heading font) change with the theme.

Effect and format styles
------------------------

The effect scheme holds the subtle, moderate and intense effect styles. The fill, line and
background-fill style lists are read-only:

.. code-block:: python

    effects = theme.effect_scheme
    print(len(effects), effects.subtle.has_effect_list)
    print(len(theme.fill_styles), len(theme.line_styles))

Applying another theme
----------------------

``apply_theme()`` replaces a master's theme with a copy of another one: from a presentation, a
slide master, a ``.thmx`` theme file or a ``.pptx`` / ``.potx`` file. Only the theme is copied, not
the source's layouts. Slides keep their theme references, which now resolve against the new theme:

.. code-block:: python

    source = Presentation()
    source.slide_masters[0].theme.color_scheme.name = "Corporate"
    source.save("corporate.pptx")

    master.apply_theme("corporate.pptx")
    print(master.theme.color_scheme.name)

Master text styles
------------------

The master also defines the default formatting of title, body and other text, level by level:

.. code-block:: python

    from openpptx.util import Pt

    styles = master.text_styles
    styles.title[0].font.size = Pt(40)
    styles.body[0].font.size = Pt(24)
    print(styles.body[1].font.size.pt if styles.body[1].font.size else None)

    prs.save("themed.pptx")

Every slide, layout and master also has ``header_footer`` for the date, footer and slide-number
placeholders. See ``custom_slide_master_walk.py`` and ``custom_layouts.py`` in ``examples/`` for
complete scripts.
