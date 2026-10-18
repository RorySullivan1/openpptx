openpptx
========

A pure-Python library for reading and writing PowerPoint ``.pptx`` files (Office Open XML,
ECMA-376). Install and import it as ``openpptx``::

    from openpptx import Presentation

    prs = Presentation()

The guides below walk through each area of the library. Every code sample in them runs as part of
the test suite. Complete scripts for each area live in the repository's
`examples/ <https://github.com/RorySullivan1/openpptx/tree/main/examples>`_ directory. Coming from
python-pptx? Start with :doc:`migration`.

.. toctree::
   :maxdepth: 1
   :caption: Guides

   guides/slides
   guides/shapes
   guides/text
   guides/charts
   guides/effects
   guides/theme

.. toctree::
   :maxdepth: 1
   :caption: Using openpptx

   migration
   stability

.. toctree::
   :maxdepth: 2
   :caption: API reference

   api/presentation
   api/shapes
   api/text
   api/chart
   api/dml
   api/table
   api/enum
   api/util
