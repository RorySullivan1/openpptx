Coming from python-pptx
=======================

openpptx is derived from `python-pptx <https://github.com/scanny/python-pptx>`_ and keeps its
object model, so most python-pptx code runs once the imports change. This page lists what is
different: the names, the exceptions, a few behaviours, and what openpptx adds.

Installing and importing
------------------------

The distribution and the import package are both ``openpptx``. It does not use the name ``pptx``,
so the two libraries can be installed side by side while you move code across::

    pip install openpptx

The public modules keep python-pptx's layout under the new name. Code like this:

.. code-block:: python
   :class: no-test

    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.enum.shapes import MSO_SHAPE

becomes:

.. code-block:: python

    from openpptx import Presentation
    from openpptx.enum.shapes import MSO_SHAPE
    from openpptx.util import Inches, Pt

    prs = Presentation()
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    box = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1), Inches(1), Inches(2), Inches(1))
    box.text_frame.text = "Same API, new name"

Renamed and internal names
--------------------------

========================================  ==============================================
python-pptx                               openpptx
========================================  ==============================================
``pptx.exc.PythonPptxError``              ``openpptx.exc.OpenPptxError``
``pptx.exceptions`` (alias of ``exc``)    ``openpptx.exc``; there is no alias
``pptx.util.lazyproperty``                internal; not part of the API
``pptx.shapes.Subshape``                  internal
``pptx.shapes.shapetree.*ShapeFactory``   internal
``pptx.chart.plot.PlotFactory``,          internal
``pptx.chart.plot.PlotTypeInspector``
========================================  ==============================================

openpptx also states which modules are public. ``openpptx.oxml``, ``openpptx.opc`` and
``openpptx.parts`` are internal, as are a few implementation modules in the API layer; see
:doc:`stability`. Code that reaches into the XML through ``shape._element`` still works, but is
not covered by the stability promise.

Exceptions
----------

python-pptx mostly raised ``ValueError``, ``TypeError`` and ``KeyError``. openpptx raises its own
exception classes, all derived from ``OpenPptxError``, and each one that replaces a builtin also
derives from that builtin. An existing ``except ValueError`` still catches it:

.. code-block:: python

    from openpptx.exc import InvalidTypeError, InvalidValueError, OpenPptxError

    try:
        box.line.dash_style = "dashed"  # -- not an MSO_LINE_DASH_STYLE member
    except ValueError as error:
        print(type(error).__name__, isinstance(error, OpenPptxError))

    try:
        box.rotation = "45"  # -- a number is expected
    except TypeError as error:
        print(type(error).__name__, isinstance(error, InvalidTypeError))

Lookups follow Python's protocols, as in python-pptx: an index out of range raises ``IndexError``
(``prs.slides[99]``) and a missing key raises ``KeyError`` (``slide.placeholders[99]``).

Opening a deck from a path
--------------------------

python-pptx reads the whole file into memory when it opens it. openpptx leaves images, media and
other binary parts in the file until they are used, so a deck full of pictures opens quickly and
uses little memory. Keep the file where it is while you work on the presentation. Saving back over
the same path is fine; opening that path for writing yourself first empties it before those parts
can be read. A file-like object is still read in full when it is opened.

What openpptx adds
------------------

Everything python-pptx does carries over. On top of it, among other things:

- **Slides**: delete, duplicate, move, import from another deck and merge whole decks; custom
  layouts; sections and custom shows; classic and modern comments; tags; slide-show settings.
  See :doc:`guides/slides`.
- **Text**: find and replace across runs, in a frame, a slide or the whole deck, with regular
  expressions; run traversal and merging; tab stops; more font and paragraph properties.
  See :doc:`guides/text`.
- **Charts**: waterfall, histogram, box and whisker, treemap, sunburst and funnel charts; more 3D
  charts; trendlines, error bars and data tables; combo charts. See :doc:`guides/charts`.
- **Formatting**: shadow, glow, reflection, soft edges and 3D on shapes; gradient, pattern and
  picture fills; picture brightness, contrast and grayscale. See :doc:`guides/effects`.
- **Themes**: read colour, font and effect schemes, apply another deck's theme, and edit master text
  styles. See :doc:`guides/theme`.
- **Read-only access** to transitions, animations, SmartArt (with editable node text) and the
  shapes PowerPoint wraps in ``mc:AlternateContent``, such as 3D models and zooms.
- **Audio** shapes, embedded fonts, and many more enumeration members.
- **Type annotations** on the public API, shipped with ``py.typed``.

The :doc:`API reference <api/presentation>` documents all of it, and the ``CHANGELOG.md`` in the
repository records when each feature arrived.
