"""Print the GitHub Release notes for a version, taken from CHANGELOG.md.

    python .github/scripts/release_notes.py 1.0.0        # the notes, on stdout
    python .github/scripts/release_notes.py 1.0.0 --check

A final version needs its own dated section (`## [1.0.0] - 2026-10-18`); without one this exits 1,
which `release.yml` runs before publishing, so a release never reaches PyPI without notes. A
pre-release (`1.0.0rc1`, `1.1.0b2`) uses its own section if it has one, else the section of the
version it leads to, else Unreleased, under a line saying what it is.
"""

from __future__ import annotations

import os
import re
import sys

REPO_URL = "https://github.com/RorySullivan1/openpptx"
CHANGELOG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "CHANGELOG.md")

_HEADING = re.compile(r"^## \[([^\]]+)\](?: - (\d{4}-\d{2}-\d{2}))?\s*$", re.MULTILINE)
_PRE_RELEASE = re.compile(r"^(\d+\.\d+\.\d+)(a|b|rc)\d+$")


def sections(text: str) -> dict[str, tuple[str | None, str]]:
    """Map each `## [name]` heading to its (date, body), the body without surrounding blank lines."""
    found: dict[str, tuple[str | None, str]] = {}
    matches = list(_HEADING.finditer(text))
    for i, match in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        body = text[match.end() : end]
        # -- the link definitions at the foot of the file belong to no section --
        body = re.split(r"^\[[^\]]+\]: https?://", body, maxsplit=1, flags=re.MULTILINE)[0]
        found[match.group(1)] = (match.group(2), body.strip("\n"))
    return found


def notes(version: str, text: str) -> str:
    """The release notes for `version`; `SystemExit` if a final version has no dated section."""
    found = sections(text)
    tag = "v" + version
    pre = _PRE_RELEASE.match(version)

    if pre is None:
        date, body = found.get(version, (None, ""))
        if date is None or not body:
            raise SystemExit(
                "CHANGELOG.md has no dated, non-empty `## [%s] - YYYY-MM-DD` section" % version
            )
        lead = ""
    else:
        target = pre.group(1)
        kind = {"a": "An alpha", "b": "A beta", "rc": "A release candidate"}[pre.group(2)]
        for name in (version, target, "Unreleased"):
            body = found.get(name, (None, ""))[1]
            if body:
                break
        lead = (
            "%s for openpptx %s. Install it with `pip install openpptx==%s`; a plain "
            "`pip install openpptx` takes it only while no final release exists.\n\n"
            % (kind, target, version)
        )

    links = "\n\n---\n\n[PyPI](https://pypi.org/project/openpptx/%s/) | [Changelog](%s/blob/%s/CHANGELOG.md)" % (
        version,
        REPO_URL,
        tag,
    )
    return lead + body + links + "\n"


def main(argv: list[str]) -> int:
    if len(argv) not in (2, 3) or (len(argv) == 3 and argv[2] != "--check"):
        print(__doc__, file=sys.stderr)
        return 2
    with open(CHANGELOG, encoding="utf-8") as f:
        text = f.read()
    result = notes(argv[1], text)
    if len(argv) == 2:
        sys.stdout.write(result)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
