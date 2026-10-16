"""API for reading/writing serialized Open Packaging Convention (OPC) package."""

from __future__ import annotations

import contextlib
import os
import posixpath
import zipfile
import zlib
from typing import IO, TYPE_CHECKING, Any, Container, Iterator, Sequence

from openpptx.exc import InvalidPackageError, PackageError, PackageNotFoundError
from openpptx.opc.constants import CONTENT_TYPE as CT
from openpptx.opc.oxml import CT_Types, serialize_part_xml
from openpptx.opc.packuri import CONTENT_TYPES_URI, PACKAGE_URI, PackURI
from openpptx.opc.shared import CaseInsensitiveDict
from openpptx.opc.spec import default_content_types
from openpptx.util import lazyproperty

if TYPE_CHECKING:
    from openpptx.opc.package import Part, _Relationships  # pyright: ignore[reportPrivateUsage]


class PackageReader(Container[bytes]):
    """Provides access to package-parts of an OPC package with dict semantics.

    The package may be in zip-format (a .pptx file) or expanded into a directory structure,
    perhaps by unzipping a .pptx file.
    """

    def __init__(self, pkg_file: str | IO[bytes]):
        self._pkg_file = pkg_file

    def __contains__(self, pack_uri: object) -> bool:
        """Return True when part identified by `pack_uri` is present in package."""
        return pack_uri in self._blob_reader

    def __getitem__(self, pack_uri: PackURI) -> bytes:
        """Return bytes for part corresponding to `pack_uri`."""
        return self._blob_reader[pack_uri]

    def blob_source_for(self, pack_uri: PackURI) -> bytes | ZipMember:
        """Return the bytes of `pack_uri`, or a |ZipMember| that reads them when asked.

        Only a package opened from a path to a zip file defers the read. A stream may be closed
        by its caller once loading ends, and an expanded directory is rare, so both give bytes.
        """
        return self._blob_reader.blob_source_for(pack_uri)

    def close(self) -> None:
        """Release the open package file; deferred reads reopen it when they need it."""
        self._blob_reader.close()

    def rels_xml_for(self, partname: PackURI) -> bytes | None:
        """Return optional rels item XML for `partname`.

        Returns `None` if no rels item is present for `partname`. `partname` is a |PackURI|
        instance.
        """
        blob_reader, uri = self._blob_reader, partname.rels_uri
        return blob_reader[uri] if uri in blob_reader else None

    @lazyproperty
    def _blob_reader(self) -> _PhysPkgReader:
        """|_PhysPkgReader| subtype providing read access to the package file."""
        return _PhysPkgReader.factory(self._pkg_file)


class PackageWriter:
    """Writes a zip-format OPC package to `pkg_file`.

    `pkg_file` can be either a path to a zip file (a string) or a file-like object. `pkg_rels` is
    the |_Relationships| object containing relationships for the package. `parts` is a sequence of
    |Part| subtype instance to be written to the package.

    Its single API classmethod is :meth:`write`. This class is not intended to be instantiated.
    """

    def __init__(self, pkg_file: str | IO[bytes], pkg_rels: _Relationships, parts: Sequence[Part]):
        self._pkg_file = pkg_file
        self._pkg_rels = pkg_rels
        self._parts = parts

    @classmethod
    def write(
        cls, pkg_file: str | IO[bytes], pkg_rels: _Relationships, parts: Sequence[Part]
    ) -> None:
        """Write a physical package (.pptx file) to `pkg_file`.

        The serialized package contains `pkg_rels` and `parts`, a content-types stream based on
        the content type of each part, and a .rels file for each part that has relationships.
        """
        cls(pkg_file, pkg_rels, parts)._write()

    def _write(self) -> None:
        """Write physical package (.pptx file)."""
        with _PhysPkgWriter.factory(self._pkg_file) as phys_writer:
            self._write_content_types_stream(phys_writer)
            self._write_pkg_rels(phys_writer)
            self._write_parts(phys_writer)

    def _write_content_types_stream(self, phys_writer: _PhysPkgWriter) -> None:
        """Write `[Content_Types].xml` part to the physical package.

        This part must contain an appropriate content type lookup target for each part in the
        package.
        """
        phys_writer.write(
            CONTENT_TYPES_URI,
            serialize_part_xml(_ContentTypesItem.xml_for(self._parts)),
        )

    def _write_parts(self, phys_writer: _PhysPkgWriter) -> None:
        """Write blob of each part in `parts` to the package.

        A rels item for each part is also written when the part has relationships.
        """
        for part in self._parts:
            phys_writer.write(part.partname, part.blob)
            if part._rels:  # pyright: ignore[reportPrivateUsage]
                phys_writer.write(part.partname.rels_uri, part.rels.xml)

    def _write_pkg_rels(self, phys_writer: _PhysPkgWriter) -> None:
        """Write the XML rels item for `pkg_rels` ('/_rels/.rels') to the package."""
        phys_writer.write(PACKAGE_URI.rels_uri, self._pkg_rels.xml)


class _PhysPkgReader(Container[PackURI]):
    """Base class for physical package reader objects."""

    def __contains__(self, item: object) -> bool:
        """Must be implemented by each subclass."""
        raise NotImplementedError(  # pragma: no cover
            "`%s` must implement `.__contains__()`" % type(self).__name__
        )

    def __getitem__(self, pack_uri: PackURI) -> bytes:
        """Blob for part corresponding to `pack_uri`."""
        raise NotImplementedError(  # pragma: no cover
            f"`{type(self).__name__}` must implement `.__contains__()`"
        )

    def blob_source_for(self, pack_uri: PackURI) -> bytes | ZipMember:
        """Bytes for part `pack_uri`; a subclass able to defer the read returns a |ZipMember|."""
        return self[pack_uri]

    def close(self) -> None:
        """Release any open file; the base implementation holds none."""

    @classmethod
    def factory(cls, pkg_file: str | IO[bytes]) -> _PhysPkgReader:
        """Return |_PhysPkgReader| subtype instance appropriage for `pkg_file`."""
        # --- for pkg_file other than str, assume it's a stream and pass it to Zip
        # --- reader to sort out
        if not isinstance(pkg_file, str):
            return _ZipPkgReader(pkg_file)

        # --- otherwise we treat `pkg_file` as a path ---
        if os.path.isdir(pkg_file):
            return _DirPkgReader(pkg_file)

        if not os.path.exists(pkg_file):
            raise PackageNotFoundError("Package not found at '%s'" % pkg_file)

        # --- an existing file that is not a readable zip raises InvalidPackageError ---
        return _ZipPkgReader(pkg_file)


class _DirPkgReader(_PhysPkgReader):
    """Implements |PhysPkgReader| interface for OPC package extracted into directory.

    `path` is the path to a directory containing an expanded package.
    """

    def __init__(self, path: str):
        self._path = os.path.abspath(path)

    def __contains__(self, pack_uri: object) -> bool:
        """Return True when part identified by `pack_uri` is present in zip archive."""
        if not isinstance(pack_uri, PackURI):
            return False
        return os.path.exists(posixpath.join(self._path, pack_uri.membername))

    def __getitem__(self, pack_uri: PackURI) -> bytes:
        """Return bytes of file corresponding to `pack_uri` in package directory."""
        path = os.path.join(self._path, pack_uri.membername)
        try:
            with open(path, "rb") as f:
                return f.read()
        except IOError:
            raise KeyError("no member '%s' in package" % pack_uri)


class _ZipPkgReader(_PhysPkgReader):
    """Implements |PhysPkgReader| interface for a zip-file OPC package.

    Blobs are read on demand from the zip archive rather than all at once,
    reducing peak memory usage for large packages. The zip file stays open while the package
    loads, until `close()`. When `pkg_file` is a path, `blob_source_for()` returns a |ZipMember|
    that reopens the file to read its bytes later.
    """

    def __init__(self, pkg_file: str | IO[bytes]):
        try:
            self._zipf = zipfile.ZipFile(pkg_file, "r")
        except (zipfile.BadZipFile, EOFError) as e:
            raise InvalidPackageError(
                "%s is not a valid .pptx package: not a readable zip archive (%s)"
                % (_describe(pkg_file), e)
            ) from e
        self._archive = ZipArchive(os.path.abspath(pkg_file)) if isinstance(pkg_file, str) else None

    def __del__(self) -> None:
        """Close the zip file when this reader is garbage-collected."""
        # -- `_zipf` is absent when opening the archive raised in `__init__()` --
        zipf = getattr(self, "_zipf", None)
        if zipf is not None:
            zipf.close()

    def __contains__(self, pack_uri: object) -> bool:
        """Return True when part identified by `pack_uri` is present in zip archive."""
        return pack_uri in self._member_names

    def __getitem__(self, pack_uri: PackURI) -> bytes:
        """Return bytes for part corresponding to `pack_uri`.

        Reads the member from the zip archive on demand.
        Raises |KeyError| if no matching member is present in zip archive.
        """
        membername = self._member_names.get(pack_uri)
        if membername is None:
            raise KeyError("no member '%s' in package" % pack_uri)
        try:
            return self._zipf.read(membername)
        except (zipfile.BadZipFile, zlib.error, EOFError, NotImplementedError) as e:
            raise InvalidPackageError(
                "part '%s' of the package cannot be read: the archive is corrupt (%s)"
                % (pack_uri, e)
            ) from e

    def blob_source_for(self, pack_uri: PackURI) -> bytes | ZipMember:
        """A |ZipMember| for `pack_uri` when this archive was opened from a path, else its bytes."""
        if self._archive is None:
            return self[pack_uri]
        membername = self._member_names.get(pack_uri)
        if membername is None:
            raise KeyError("no member '%s' in package" % pack_uri)
        info = self._zipf.getinfo(membername)
        return ZipMember(self._archive, membername, info.CRC, info.file_size)

    def close(self) -> None:
        """Close the zip file. Reading through this reader afterwards fails."""
        self._zipf.close()

    @lazyproperty
    def _member_names(self) -> dict[PackURI, str]:
        """dict mapping PackURI to zip member name (str).

        Only the member names are loaded eagerly — the actual blob bytes are
        read on demand in ``__getitem__``.
        """
        return {PackURI("/%s" % name): name for name in self._zipf.namelist()}


class ZipArchive:
    """A `.pptx` file on disk that |ZipMember| objects read from after the package has loaded.

    The file is open only while a read, or a `batch()` of reads, needs it. Holding no handle in
    between leaves the file free to be moved or deleted, which Windows forbids while it is open.
    """

    def __init__(self, path: str):
        self.path = path
        self._zipf: zipfile.ZipFile | None = None
        self._depth = 0

    @contextlib.contextmanager
    def batch(self) -> Iterator[None]:
        """Keep the file open for every read made inside the `with` block.

        Reopening the zip parses its central directory each time, about half a millisecond for a
        few hundred parts, so a save reads all its parts inside one batch. Batches nest.
        """
        if self._depth == 0:
            self._zipf = self._open()
        self._depth += 1
        try:
            yield
        finally:
            self._depth -= 1
            if self._depth == 0 and self._zipf is not None:
                self._zipf.close()
                self._zipf = None

    def read(self, membername: str, crc: int, size: int) -> bytes:
        """Bytes of `membername`, which held `crc` and `size` bytes when the package loaded.

        Raises |PackageError| when the file is gone or its member no longer matches: the file was
        replaced or rewritten after the presentation was opened.
        """
        with self.batch():
            assert self._zipf is not None
            try:
                info = self._zipf.getinfo(membername)
            except KeyError:
                info = None
            if info is None or (info.CRC, info.file_size) != (crc, size):
                raise self._changed_error(membername)
            try:
                return self._zipf.read(info)
            except (zipfile.BadZipFile, zlib.error, EOFError, NotImplementedError) as e:
                raise InvalidPackageError(
                    "part '/%s' of the package cannot be read: the archive is corrupt (%s)"
                    % (membername, e)
                ) from e

    def _changed_error(self, membername: str | None = None) -> PackageError:
        parts = "its parts" if membername is None else "its part '/%s'" % membername
        return PackageError(
            "'%s' changed or was removed after the presentation was opened, so %s can no longer "
            "be read" % (self.path, parts)
        )

    def _open(self) -> zipfile.ZipFile:
        try:
            return zipfile.ZipFile(self.path, "r")
        except (OSError, zipfile.BadZipFile, EOFError) as e:
            raise self._changed_error() from e


class ZipMember:
    """The bytes of one zip member, left in a |ZipArchive| on disk until `read()`."""

    def __init__(self, archive: ZipArchive, membername: str, crc: int, size: int):
        self.archive = archive
        self._membername = membername
        self._crc = crc
        self.size = size

    def read(self) -> bytes:
        """Read the member's bytes from the archive; nothing is cached."""
        return self.archive.read(self._membername, self._crc, self.size)


def _describe(pkg_file: str | IO[bytes]) -> str:
    """Name `pkg_file` for an error message: its path, or "the stream" for a file-like object."""
    return "'%s'" % pkg_file if isinstance(pkg_file, str) else "the stream"


class _PhysPkgWriter:
    """Base class for physical package writer objects."""

    @classmethod
    def factory(cls, pkg_file: str | IO[bytes]) -> _ZipPkgWriter:
        """Return |_PhysPkgWriter| subtype instance appropriage for `pkg_file`.

        Currently the only subtype is `_ZipPkgWriter`, but a `_DirPkgWriter` could be implemented
        or even a `_StreamPkgWriter`.
        """
        return _ZipPkgWriter(pkg_file)

    def write(self, pack_uri: PackURI, blob: bytes) -> None:
        """Write `blob` to package with membername corresponding to `pack_uri`."""
        raise NotImplementedError(  # pragma: no cover
            f"`{type(self).__name__}` must implement `.write()`"
        )


class _ZipPkgWriter(_PhysPkgWriter):
    """Implements |PhysPkgWriter| interface for a zip-file (.pptx file) OPC package."""

    def __init__(self, pkg_file: str | IO[bytes]):
        self._pkg_file = pkg_file

    def __enter__(self) -> _ZipPkgWriter:
        """Enable use as a context-manager. Opening zip for writing happens here."""
        return self

    def __exit__(self, *exc: list[Any]) -> None:
        """Close the zip archive on exit from context.

        Closing flushes any pending physical writes and releasing any resources it's using.
        """
        self._zipf.close()

    def write(self, pack_uri: PackURI, blob: bytes) -> None:
        """Write `blob` to zip package with membername corresponding to `pack_uri`."""
        self._zipf.writestr(pack_uri.membername, blob)

    @lazyproperty
    def _zipf(self) -> zipfile.ZipFile:
        """`ZipFile` instance open for writing."""
        return zipfile.ZipFile(
            self._pkg_file, "w", compression=zipfile.ZIP_DEFLATED, strict_timestamps=False
        )


class _ContentTypesItem:
    """Composes content-types "part" ([Content_Types].xml) for a collection of parts."""

    def __init__(self, parts: Sequence[Part]):
        self._parts = parts

    @classmethod
    def xml_for(cls, parts: Sequence[Part]) -> CT_Types:
        """Return content-types XML mapping each part in `parts` to a content-type.

        The resulting XML is suitable for storage as `[Content_Types].xml` in an OPC package.
        """
        return cls(parts)._xml

    @lazyproperty
    def _xml(self) -> CT_Types:
        """lxml.etree._Element containing the content-types item.

        This XML object is suitable for serialization to the `[Content_Types].xml` item for an OPC
        package. Although the sequence of elements is not strictly significant, as an aid to
        testing and readability Default elements are sorted by extension and Override elements are
        sorted by partname.
        """
        defaults, overrides = self._defaults_and_overrides
        _types_elm = CT_Types.new()

        for ext, content_type in sorted(defaults.items()):
            _types_elm.add_default(ext, content_type)
        for partname, content_type in sorted(overrides.items()):
            _types_elm.add_override(partname, content_type)

        return _types_elm

    @lazyproperty
    def _defaults_and_overrides(self) -> tuple[dict[str, str], dict[PackURI, str]]:
        """pair of dict (defaults, overrides) accounting for all parts.

        `defaults` is {ext: content_type} and overrides is {partname: content_type}.
        """
        defaults = CaseInsensitiveDict(rels=CT.OPC_RELATIONSHIPS, xml=CT.XML)
        overrides: dict[PackURI, str] = {}

        for part in self._parts:
            partname, content_type = part.partname, part.content_type
            ext = partname.ext
            if (ext.lower(), content_type) in default_content_types:
                defaults[ext] = content_type
            else:
                overrides[partname] = content_type

        return defaults, overrides
