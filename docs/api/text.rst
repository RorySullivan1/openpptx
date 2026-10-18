Text
====

``openpptx.text.text``
----------------------

.. automodule:: openpptx.text.text

``openpptx.text.search``
------------------------

Find and replace across runs. The methods are on |TextFrame|, ``_Paragraph``,
|Slide| and |Presentation| (``find_all()``/``replace()`` on a text frame or
paragraph, ``find_text()``/``replace_text()`` on a slide or the presentation);
this module holds the objects they return and the machinery behind them.

.. automodule:: openpptx.text.search

``openpptx.text.styles``
------------------------

.. automodule:: openpptx.text.styles

Objects the API returns from private classes
--------------------------------------------

These classes have private names but are handed to callers, e.g. by
``text_frame.paragraphs`` or ``table.cell()``.

.. autoclass:: openpptx.text.text._Paragraph

.. autoclass:: openpptx.text.text._Run

.. autoclass:: openpptx.text.text._Hyperlink

