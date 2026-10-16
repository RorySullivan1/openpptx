# pyright: reportPrivateUsage=false

"""Behavior tests for lazy binary parts, read from a real `.pptx` on disk.

A deck opened from a path keeps each binary part's bytes in the zip until they are used, and holds
no file handle between reads. A deck opened from a stream is read in full.
"""

from __future__ import annotations

import io
import os
import shutil
import zipfile
from pathlib import Path

import pytest

from openpptx import Presentation
from openpptx.exc import PackageError
from openpptx.opc.package import Part, XmlPart
from openpptx.opc.serialized import ZipArchive
from openpptx.util import Inches

from ..unitutil.file import absjoin, test_file_dir

IMAGE_PATHS = (
    absjoin(test_file_dir, "python-icon.jpeg"),
    absjoin(test_file_dir, "monty-truth.png"),
)


def _binary_parts(prs) -> list[Part]:
    return [p for p in prs.part.package.iter_parts() if not isinstance(p, XmlPart)]


def _picture_parts(prs) -> list[Part]:
    """The parts of the pictures added to the deck; the template's thumbnail is an image too."""
    return [p for p in _binary_parts(prs) if p.partname.startswith("/ppt/media/")]


def _spy_on_reads(monkeypatch: pytest.MonkeyPatch) -> list[tuple[str, str]]:
    """Record each (archive path, member name) a lazy part reads from from now on."""
    reads: list[tuple[str, str]] = []
    real_read = ZipArchive.read

    def spy(self: ZipArchive, membername: str, crc: int, size: int) -> bytes:
        reads.append((self.path, membername))
        return real_read(self, membername, crc, size)

    monkeypatch.setattr(ZipArchive, "read", spy)
    return reads


def _member_bytes(path: Path) -> dict[str, bytes]:
    with zipfile.ZipFile(path) as zipf:
        return {name: zipf.read(name) for name in zipf.namelist()}


class DescribeLazyBlobs:
    """A binary part loaded from a path reads its bytes from the source zip when used."""

    def it_leaves_binary_bytes_in_the_source_file_until_used(self, deck_path: Path):
        prs = Presentation(str(deck_path))

        parts = _binary_parts(prs)
        assert len(_picture_parts(prs)) == 2
        assert all(p._blob_source is not None and p._blob_bytes is None for p in parts)

        members = _member_bytes(deck_path)
        for part in parts:
            assert part.blob == members[part.partname.membername]
        # -- reading does not keep the bytes --
        assert all(p._blob_bytes is None for p in parts)

    def it_reads_a_stream_source_in_full(self, deck_path: Path, tmp_path: Path):
        with open(deck_path, "rb") as stream:
            prs = Presentation(stream)

        assert all(p._blob_source is None for p in _binary_parts(prs))
        out = tmp_path / "from-stream.pptx"
        prs.save(str(out))
        assert _member_bytes(out).keys() >= {
            p.partname.membername for p in _binary_parts(prs)
        }

    def it_writes_untouched_binary_parts_unchanged(self, deck_path: Path, tmp_path: Path):
        prs = Presentation(str(deck_path))
        out = tmp_path / "resaved.pptx"

        prs.save(str(out))

        before, after = _member_bytes(deck_path), _member_bytes(out)
        for part in _binary_parts(prs):
            name = part.partname.membername
            assert after[name] == before[name]

    def it_can_save_over_its_source_file(self, deck_path: Path):
        before = _member_bytes(deck_path)
        prs = Presentation(str(deck_path))
        names = [p.partname.membername for p in _binary_parts(prs)]

        prs.save(str(deck_path))

        after = _member_bytes(deck_path)
        for name in names:
            assert after[name] == before[name]
        # -- and the deck still works from bytes now held in memory --
        prs.save(io.BytesIO())

    def it_raises_when_the_source_file_is_replaced_after_open(
        self, deck_path: Path, other_deck_path: Path
    ):
        prs = Presentation(str(deck_path))
        shutil.copyfile(other_deck_path, deck_path)

        with pytest.raises(PackageError, match="changed or was removed"):
            _picture_parts(prs)[0].blob

    def it_raises_when_the_source_file_is_removed_after_open(self, deck_path: Path):
        prs = Presentation(str(deck_path))

        # -- removing it succeeds on Windows too: no handle is held between reads --
        os.remove(deck_path)

        with pytest.raises(PackageError, match="changed or was removed"):
            _binary_parts(prs)[0].blob

    def it_opens_the_source_zip_once_per_save(
        self, deck_path: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ):
        prs = Presentation(str(deck_path))
        opened: list[str] = []
        real_zipfile = zipfile.ZipFile

        def spy(file, mode="r", *args, **kwargs):
            if mode == "r" and isinstance(file, str):
                opened.append(file)
            return real_zipfile(file, mode, *args, **kwargs)

        monkeypatch.setattr(zipfile, "ZipFile", spy)

        prs.save(str(tmp_path / "out.pptx"))

        assert opened == [str(deck_path.resolve())]

    def it_reads_only_same_size_pictures_when_adding_one(
        self, deck_path: Path, monkeypatch: pytest.MonkeyPatch
    ):
        prs = Presentation(str(deck_path))
        reads = _spy_on_reads(monkeypatch)
        shapes = prs.slides[0].shapes

        shapes.add_picture(absjoin(test_file_dir, "python-powered.png"), 0, 0)
        assert reads == []

        # -- an image already in the deck is found by reading only the part of its size --
        picture = shapes.add_picture(IMAGE_PATHS[1], 0, 0)
        assert picture.image.blob == open(IMAGE_PATHS[1], "rb").read()
        assert set(reads) == {(str(deck_path), "ppt/media/image2.png")}
        assert len(_picture_parts(prs)) == 3

    def it_reads_no_target_picture_when_importing_one_of_another_size(
        self, deck_path: Path, other_deck_path: Path, monkeypatch: pytest.MonkeyPatch
    ):
        target = Presentation(str(deck_path))
        source = Presentation(str(other_deck_path))
        reads = _spy_on_reads(monkeypatch)

        target.slides.import_slide(source.slides[0])

        assert [read for read in reads if read[0] == str(deck_path)] == []

    # fixtures -------------------------------------------------------

    @pytest.fixture
    def deck_path(self, tmp_path: Path) -> Path:
        """A deck with two distinct images, saved to its own file."""
        prs = Presentation()
        for image_path in IMAGE_PATHS:
            slide = prs.slides.add_slide(prs.slide_layouts[6])
            slide.shapes.add_picture(image_path, Inches(1), Inches(1))
        path = tmp_path / "deck.pptx"
        prs.save(str(path))
        return path

    @pytest.fixture
    def other_deck_path(self, tmp_path: Path) -> Path:
        """A different deck with one image, to overwrite the source with."""
        prs = Presentation()
        slide = prs.slides.add_slide(prs.slide_layouts[6])
        slide.shapes.add_picture(absjoin(test_file_dir, "python-powered.png"), 0, 0)
        path = tmp_path / "other.pptx"
        prs.save(str(path))
        return path
