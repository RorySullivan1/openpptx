"""Every Python sample in the narrative docs runs, so the guides stay true to the API.

Each page's `.. code-block:: python` blocks run in order in one namespace, in a scratch directory
holding the files the samples open (see `FIXTURES`). A block marked `:class: no-test` is not run;
the migration guide uses that for the python-pptx code it starts from.
"""

from __future__ import annotations

import os
import re
import shutil
import textwrap

import pytest

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
DOCS_DIR = os.path.join(os.path.dirname(TESTS_DIR), "docs")
TEST_FILES = os.path.join(TESTS_DIR, "test_files")

FIXTURES = {"logo.png": "python-powered.png", "photo.jpg": "python-icon.jpeg"}
"""Files the samples open by name -> the test file each is copied from."""

_BLOCK = re.compile(r"^\.\. code-block:: python\n((?:   :[\w-]+:.*\n)*)\n((?:(?:   .*)?\n)+)", re.M)


def _pages() -> list[str]:
    pages = [os.path.join("guides", name) for name in os.listdir(os.path.join(DOCS_DIR, "guides"))]
    pages.append("migration.rst")
    return sorted(page for page in pages if page.endswith(".rst"))


def _samples(page: str) -> list[str]:
    with open(os.path.join(DOCS_DIR, page), encoding="utf-8") as f:
        text = f.read()
    return [
        textwrap.dedent(body)
        for options, body in _BLOCK.findall(text)
        if ":class: no-test" not in options
    ]


class DescribeTheGuides:
    @pytest.mark.parametrize("page", _pages())
    def it_runs_every_sample_on_the_page(self, page: str, tmp_path, monkeypatch):
        samples = _samples(page)
        assert samples, "no runnable samples found in %s" % page
        for name, source in FIXTURES.items():
            shutil.copy(os.path.join(TEST_FILES, source), str(tmp_path / name))
        monkeypatch.chdir(tmp_path)

        namespace: dict[str, object] = {"__name__": "__guide__"}
        for number, sample in enumerate(samples, 1):
            code = compile(sample, "%s, sample %d" % (page, number), "exec")
            exec(code, namespace)
