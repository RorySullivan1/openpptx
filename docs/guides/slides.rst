Presentations and slides
========================

A |Presentation| holds the slides, the slide masters and layouts they are built on, and the
document's properties. Everything else in openpptx is reached from one.

Opening and saving
------------------

``Presentation()`` with no argument starts from the built-in blank template. Pass a path or a
file-like object to open an existing ``.pptx``, ``.pptm`` or ``.potx`` file:

.. code-block:: python

    from openpptx import Presentation
    from openpptx.util import Inches

    prs = Presentation()
    prs.save("blank.pptx")

    prs = Presentation("blank.pptx")

A deck opened from a path leaves its images and media in the file until they are used, so keep
the file in place while you work on it. Saving back over the same path is fine. A file-like
object is read in full when it is opened.

The slide size is in EMUs, like every length in openpptx. ``Inches``, ``Cm``, ``Mm`` and ``Pt``
convert for you:

.. code-block:: python

    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    print(prs.slide_width.inches)

Adding slides
-------------

A slide is added from one of the layouts of a slide master. The default template's layouts are,
in order: Title Slide, Title and Content, Section Header, Two Content, Comparison, Title Only,
Blank, Content with Caption and Picture with Caption.

.. code-block:: python

    title_layout = prs.slide_layouts[0]
    slide = prs.slides.add_slide(title_layout)
    slide.shapes.title.text = "Quarterly review"
    slide.placeholders[1].text = "October 2026"

    content = prs.slides.add_slide(prs.slide_layouts.get_by_name("Title and Content"))
    content.shapes.title.text = "Agenda"

Each slide has a notes page, created when you first ask for it:

.. code-block:: python

    content.notes_slide.notes_text_frame.text = "Keep this to five minutes."

Rearranging slides
------------------

``Slides`` can duplicate, move and delete. Duplicating copies the slide's images, charts and
media relationships too:

.. code-block:: python

    copy = prs.slides.duplicate(content)
    copy.shapes.title.text = "Agenda (continued)"

    prs.slides.move(prs.slides.index(copy), 1)
    prs.slides.delete(copy)
    print(len(prs.slides))

Slides can also come from another deck. ``import_slide()`` copies one slide, bringing its layout
across when this deck has no matching one, and ``merge()`` appends every slide of a deck:

.. code-block:: python

    other = Presentation()
    extra = other.slides.add_slide(other.slide_layouts[5])
    extra.shapes.title.text = "Appendix"

    imported = prs.slides.import_slide(extra)
    appended = prs.slides.merge(other)

Layouts
-------

A layout can be added to a master the way PowerPoint's Insert Layout does it, with title, date,
footer and slide-number placeholders placed by the master, and then given placeholders of its own:

.. code-block:: python

    from openpptx.enum.shapes import PP_PLACEHOLDER

    layout = prs.slide_layouts.add_slide_layout("Title and Chart")
    layout.shapes.add_placeholder(PP_PLACEHOLDER.CHART)
    chart_slide = prs.slides.add_slide(layout)

Sections and custom shows
-------------------------

Sections group slides in PowerPoint's slide sorter. A custom show is a named subset of slides to
present on its own:

.. code-block:: python

    intro = prs.sections.add("Introduction")
    print(intro.name, len(prs.sections))

    short = prs.custom_shows.add("Short version", [slide, content])
    print([s.slide_id for s in short.slides])

Document properties, tags and comments
--------------------------------------

The core properties are the ones PowerPoint shows under File > Info. Custom properties take
``str``, ``int``, ``float`` and ``bool`` values:

.. code-block:: python

    prs.core_properties.title = "Quarterly review"
    prs.core_properties.author = "Finance team"
    prs.custom_properties["Client"] = "Acme"
    prs.custom_properties["Revision"] = 3

Tags are name-value strings stored with a slide or a shape, invisible in the slide show. Comments
are the classic slide comments; ``slide.threaded_comments`` reads and writes the modern ones:

.. code-block:: python

    slide.tags["review-status"] = "draft"
    print("review-status" in slide.tags)

    comment = slide.comments.add("Pat Lee", "PL", "Check the date.")
    print(comment.author, comment.text)

    prs.save("review.pptx")

The ``examples/`` directory has complete scripts for these areas, among them
``slide_operations.py``, ``merge_presentations.py``, ``custom_layouts.py`` and
``comments_and_metadata.py``.
