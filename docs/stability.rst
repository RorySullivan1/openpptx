Stability and deprecation
=========================

From 1.0.0, openpptx follows `Semantic Versioning <https://semver.org/>`_. A release that
breaks the public surface described here is a new major version. Minor releases add to it, and
patch releases fix bugs in it.

The public surface
------------------

These are public:

- ``openpptx.Presentation`` and ``openpptx.__version__``.
- Every module the :doc:`API reference <api/presentation>` documents, and ``openpptx.exc``. A
  module's public names are the ones it defines without a leading underscore. A name it only
  imports from somewhere else is public where it is defined, not where it is imported.
- The members of each public class, including those it inherits from a private base class in a
  public module. ``Shape.name`` is public, for example, although ``_BaseShape`` defines it.
- The classes the reference lists as returned "from private classes" or "from internal
  modules", such as ``_Paragraph`` and ``CorePropertiesPart``, and the members it shows for them.
- The members of every enumeration.

These are internal and can change in any release:

- The ``openpptx.oxml``, ``openpptx.opc`` and ``openpptx.parts`` packages. The exceptions are
  the classes the reference lists as returned "from internal modules", and only the members it
  shows for them.
- These modules, which serve the implementation:

  - ``openpptx.chart.chartexwriter``
  - ``openpptx.chart.xlsx``
  - ``openpptx.chart.xmlwriter``
  - ``openpptx.enum.base``
  - ``openpptx.media``
  - ``openpptx.package``
  - ``openpptx.shared``
  - ``openpptx.spec``
  - ``openpptx.text.fonts``
  - ``openpptx.text.layout``
  - ``openpptx.types``

- Any name with a leading underscore, other than the private classes the reference documents.
- The objects that ``part``, ``chart_part`` and ``chartex_part`` return. Those attributes are
  public, but what they return belongs to the internal ``openpptx.parts`` layer.

Not covered by the contract at all: the exact XML written (only that PowerPoint opens it and it
means the same thing), the text of error messages, ``repr()`` output, the content of the default
template, and performance.

What counts as a breaking change
--------------------------------

Any of these, made to the public surface:

- Removing or renaming a public name.
- Changing a signature in a way that breaks an existing call: removing a parameter, adding a
  required one, reordering positional ones, or narrowing the types a parameter accepts.
- Changing what a property or method returns in a way that breaks existing use of the result.
- Changing the exception contract below. Raising a subclass of the exception documented before
  is not a break, because ``except`` still catches it.

The exception contract
----------------------

Every exception openpptx raises deliberately derives from ``openpptx.exc.OpenPptxError``, so
``except OpenPptxError`` catches them all. Several also derive from a builtin, so code that
catches the builtin keeps working: ``InvalidValueError``, ``ShapeError``, ``SlideError``,
``ChartError`` and ``TableError`` are ``ValueError`` subclasses, and ``InvalidTypeError`` is a
``TypeError`` subclass.

The API also raises a few builtins where Python's own protocols expect them:

- ``IndexError`` when an index into a sequence (slides, shapes, rows, comments...) is out of
  range.
- ``KeyError`` when a lookup by key or name finds nothing.
- ``AttributeError`` when a property does not apply to the object's current state, so that
  ``hasattr()`` reports it correctly. ``ColorFormat.rgb`` of a theme colour is an example.
- ``NotImplementedError`` for a feature openpptx does not support yet, such as writing a chart
  type it has no XML writer for.

Deprecation
-----------

A public name is never removed or renamed within a major version:

1. The minor release that deprecates a name keeps it working and makes it emit a
   ``DeprecationWarning`` that names the replacement. The changelog lists the deprecation.
2. The name keeps working, and warning, for the rest of that major version.
3. It is removed no earlier than the next major release.

Nothing renamed before 1.0.0 has a deprecated alias. There were no users to keep working, so
the policy starts at 1.0.0.

Keeping the contract
--------------------

``tests/test_public_api.py`` records every public name in ``tests/test_files/public_api.txt``.
It fails when a change adds or removes one, and when a module in the API layer is neither
documented in the reference nor listed above as internal. A contributor who changes the surface
on purpose regenerates the record with ``python -m tests.test_public_api`` from the repository
root, and commits it with the change, so the diff shows reviewers exactly what moved.
