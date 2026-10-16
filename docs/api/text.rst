Text
====

``pptx.text.text``
------------------

.. automodule:: pptx.text.text

``pptx.text.search``
--------------------

Find and replace across runs. The methods are on |TextFrame|, ``_Paragraph``,
|Slide| and |Presentation| (``find_all()``/``replace()`` on a text frame or
paragraph, ``find_text()``/``replace_text()`` on a slide or the presentation);
this module holds the objects they return and the machinery behind them.

.. automodule:: pptx.text.search

``pptx.text.styles``
--------------------

.. automodule:: pptx.text.styles

Objects the API returns from private classes
--------------------------------------------

These classes have private names but are handed to callers, e.g. by
``text_frame.paragraphs`` or ``table.cell()``.

.. autoclass:: pptx.text.text._Paragraph

.. autoclass:: pptx.text.text._Run

.. autoclass:: pptx.text.text._Hyperlink

