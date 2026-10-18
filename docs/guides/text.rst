Text
====

Text lives in a shape's text frame. A frame holds paragraphs, and a paragraph holds runs: stretches
of text that share one set of character formatting.

.. code-block:: python

    from openpptx import Presentation
    from openpptx.dml.color import RGBColor
    from openpptx.util import Inches, Pt

    prs = Presentation()
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    box = slide.shapes.add_textbox(Inches(1), Inches(1), Inches(8), Inches(3))
    frame = box.text_frame

Paragraphs and runs
-------------------

Setting ``text`` replaces everything in the frame; a ``"\n"`` starts a new paragraph and a
``"\v"`` a line break within one. For mixed formatting, build the runs yourself:

.. code-block:: python

    frame.text = "Results"
    heading = frame.paragraphs[0]
    heading.font.size = Pt(28)
    heading.font.bold = True

    body = frame.add_paragraph()
    body.level = 1
    run = body.add_run()
    run.text = "Revenue grew "
    highlight = body.add_run()
    highlight.text = "12%"
    highlight.font.bold = True
    highlight.font.color.rgb = RGBColor(0x1F, 0x77, 0xB4)

    print([p.text for p in frame.paragraphs])

Paragraph and frame formatting
------------------------------

Alignment, spacing and indents belong to the paragraph. Margins, wrapping, anchoring, columns and
auto-fit belong to the frame:

.. code-block:: python

    from openpptx.enum.text import MSO_ANCHOR, MSO_AUTO_SIZE, PP_ALIGN

    heading.alignment = PP_ALIGN.CENTER
    body.space_before = Pt(6)
    body.line_spacing = 1.2

    frame.word_wrap = True
    frame.vertical_anchor = MSO_ANCHOR.TOP
    frame.margin_left = Inches(0.2)
    frame.auto_size = MSO_AUTO_SIZE.SHAPE_TO_FIT_TEXT

A run can carry a hyperlink:

.. code-block:: python

    link = frame.add_paragraph().add_run()
    link.text = "Full report"
    link.hyperlink.address = "https://example.com/report"

Finding and replacing text
--------------------------

PowerPoint often splits one visible word across several runs, recording spelling state or an edit.
Find and replace work on the text as you see it, across runs. The new text takes the formatting of
the first run a match touches:

.. code-block:: python

    frame.text = "ACME results for Q3 2026"
    frame.paragraphs[0].add_run().text = " and ACME's outlook"

    for match in frame.find_all("ACME"):
        print(match.paragraph_index, match.start, match.text)

    replaced = frame.replace("ACME", "Acme Corp")
    print(replaced, frame.text)

``slide.find_text()`` / ``slide.replace_text()`` search every shape on a slide, group members and
table cells included, plus its notes. ``prs.find_text()`` / ``prs.replace_text()`` do the same for
every slide. Pass ``regex=True`` for a regular expression; the replacement can then use groups, and
``count`` limits how many are replaced:

.. code-block:: python

    for match in prs.find_text(r"Q[1-4] (\d{4})", regex=True):
        print(match.shape.name, match.text)

    prs.replace_text(r"Q([1-4]) (\d{4})", r"\2-Q\1", regex=True)
    print(frame.text)

Layouts, masters, charts, SmartArt and comments are not searched, and a match never crosses a
paragraph, a line break or a field.

Walking and tidying runs
------------------------

``iter_runs()`` yields every run in a frame, and ``iter_chars()`` every character with the run it is
in. ``merge_runs()`` joins neighbouring runs whose formatting is the same, ignoring proofing state,
and returns how many it removed:

.. code-block:: python

    print(sum(1 for _ in frame.iter_runs()))
    first = next(frame.iter_chars())
    print(first.char, first.paragraph_index, first.offset)
    print(frame.merge_runs())

    prs.save("text.pptx")

``fit_text()`` sizes the text to fill its shape. It needs a TrueType font file to measure the text
with, because openpptx does not render. See ``add_textbox.py`` and ``bullet_lists.py`` in
``examples/`` for complete scripts.
