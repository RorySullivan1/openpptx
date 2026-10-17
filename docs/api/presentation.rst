Presentation and slides
=======================

``openpptx.api``
----------------

.. automodule:: openpptx.api

``openpptx.presentation``
-------------------------

.. automodule:: openpptx.presentation

``openpptx.slide``
------------------

.. automodule:: openpptx.slide

``openpptx.transition``
-----------------------

.. automodule:: openpptx.transition

``openpptx.animation``
----------------------

.. automodule:: openpptx.animation

``openpptx.custom_show``
------------------------

.. automodule:: openpptx.custom_show

``openpptx.theme``
------------------

.. automodule:: openpptx.theme

``openpptx.fonts``
------------------

.. automodule:: openpptx.fonts

Objects the API returns from private classes
--------------------------------------------

These classes have private names but are handed to callers, e.g. by
``text_frame.paragraphs`` or ``table.cell()``.

.. autoclass:: openpptx.slide._Background

Objects the API returns from internal modules
---------------------------------------------

These classes are defined in the internal ``openpptx.parts`` layer but are handed to callers,
e.g. by ``prs.core_properties``, ``shape.tags`` or ``picture.image``. Only the members shown
here are public (see :doc:`../stability`). The properties and tags objects also work as
mappings: ``custom_properties["Client"]``, ``"Client" in tags``, ``len(tags)``.

.. autoclass:: openpptx.parts.coreprops.CorePropertiesPart
   :members: author, category, comments, content_status, created, identifier, keywords,
      language, last_modified_by, last_printed, modified, revision, subject, title, version

.. autoclass:: openpptx.parts.custprops.CustomPropertiesPart
   :members: get, items

.. autoclass:: openpptx.parts.tags.TagsPart
   :members: get, items

.. autoclass:: openpptx.parts.image.Image
   :members: blob, content_type, dpi, ext, filename, sha1, size
