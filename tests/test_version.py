"""The package version is written in two places; they must agree.

`pyproject.toml` gives the version PyPI publishes, and the release workflow checks the tag against
it. `openpptx.__version__` is what users and the docs see.
"""

from __future__ import annotations

import os
import re

import openpptx

PYPROJECT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "pyproject.toml")


class DescribeTheVersion:
    def it_is_the_same_in_pyproject_and_the_package(self):
        with open(PYPROJECT, encoding="utf-8") as f:
            match = re.search(r'^version = "([^"]+)"', f.read(), re.MULTILINE)
        assert match is not None
        assert openpptx.__version__ == match.group(1)

    def and_it_is_a_valid_PEP_440_release_or_pre_release(self):
        assert re.fullmatch(r"\d+\.\d+\.\d+((a|b|rc)\d+)?", openpptx.__version__)
