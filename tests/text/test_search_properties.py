# pyright: reportPrivateUsage=false

"""Property-based tests (Hypothesis) for find/replace across runs.

A paragraph's text is split into random runs with random formatting, then a random sequence of
replacements is applied both to the paragraph and to a plain Python string (`str.replace`, or
`re.sub` in regex mode, with the same `count`). After each step:

- the paragraph's text equals the string;
- every character outside a match keeps the formatting of the run it was in, and the new text
  takes the formatting of the run holding the first character of its match;
- no run the replacement empties is left behind.

`find_all()` must report the matches `re.finditer` does, and `merge_runs()` must change neither
the text nor its formatting.

Runs are derandomized so a failure reproduces, and use no example database.
"""

from __future__ import annotations

import re
from typing import cast
from xml.sax.saxutils import escape

from hypothesis import given, settings
from hypothesis import strategies as st

from pptx.oxml import parse_xml
from pptx.oxml.ns import nsdecls
from pptx.oxml.text import CT_TextParagraph
from pptx.text.text import _Paragraph

PROPERTY_SETTINGS = settings(max_examples=300, derandomize=True, database=None, deadline=None)

ALPHABET = "ab c."
# -- `None` is a run without `a:rPr`; `dirty="0"` alone formats like no `a:rPr` at all --
FORMATS = [None, 'b="1"', 'i="1"', 'dirty="0"', 'b="1" err="1"']
# -- regex patterns that cannot match the empty string, so `re.sub` counts what we count --
REGEXES = ["a+", "b.", "[ab]c", r"\.", "c|ab", "(a)(b)", " +"]

texts = st.text(alphabet=ALPHABET, max_size=24)


@st.composite
def paragraphs(draw: st.DrawFn) -> list[tuple[str, str | None]]:
    """Some text cut into runs (empty ones included), each with a random format."""
    text = draw(texts)
    cuts = sorted(draw(st.lists(st.integers(0, len(text)), max_size=6)))
    bounds = [0, *cuts, len(text)]
    return [
        (text[start:end], draw(st.sampled_from(FORMATS))) for start, end in zip(bounds, bounds[1:])
    ]


literal_ops = st.tuples(
    st.text(alphabet=ALPHABET, min_size=1, max_size=3),
    texts.map(lambda t: t[:4]),
    st.one_of(st.none(), st.integers(0, 4)),
    st.just(False),
)
regex_ops = st.tuples(
    st.sampled_from(REGEXES),
    st.sampled_from(["", "x", "yy z", r"\g<0>\g<0>", "-"]),
    st.one_of(st.none(), st.integers(0, 4)),
    st.just(True),
)
ops = st.lists(st.one_of(literal_ops, regex_ops), min_size=1, max_size=5)


def _paragraph(runs: list[tuple[str, str | None]]) -> _Paragraph:
    r_xml = "".join(
        f"<a:r>{f'<a:rPr {fmt}/>' if fmt else ''}<a:t>{escape(text)}</a:t></a:r>"
        for text, fmt in runs
    )
    p = cast(CT_TextParagraph, parse_xml(f"<a:p {nsdecls('a')}>{r_xml}</a:p>"))
    return _Paragraph(p, None)  # pyright: ignore[reportArgumentType]


def _char_formats(paragraph: _Paragraph) -> list[object]:
    return [c.run._r.formatting_key() for c in paragraph.iter_chars() if c.run is not None]


class DescribeFindReplaceProperties:
    """Find/replace across runs behaves as the same operations on a Python string."""

    @PROPERTY_SETTINGS
    @given(runs=paragraphs(), steps=ops)
    def it_replaces_as_a_string_would_and_keeps_formatting_outside_matches(
        self, runs: list[tuple[str, str | None]], steps: list[tuple[str, str, int | None, bool]]
    ):
        paragraph = _paragraph(runs)
        text = paragraph.text

        for old, new, count, regex in steps:
            compiled = re.compile(old if regex else re.escape(old))
            formats = _char_formats(paragraph)
            empty_runs = sum(not r.text for r in paragraph.runs)
            matches = list(compiled.finditer(text))[: count if count is not None else None]

            # -- the formatting each character of the result should have --
            expected_formats: list[object] = []
            pos = 0
            for m in matches:
                expected_formats += formats[pos : m.start()]
                new_text = m.expand(new) if regex else new
                expected_formats += [formats[m.start()]] * len(new_text)
                pos = m.end()
            expected_formats += formats[pos:]

            n = paragraph.replace(old, new, count=count, regex=regex)

            if regex:
                text = compiled.sub(new, text, count=count or 0) if count != 0 else text
            else:
                text = text.replace(old, new, -1 if count is None else count)
            assert paragraph.text == text
            assert n == len(matches)
            assert _char_formats(paragraph) == expected_formats
            # -- a run the replacement empties is removed; runs outside the matches are kept --
            assert sum(not r.text for r in paragraph.runs) <= empty_runs

    @PROPERTY_SETTINGS
    @given(runs=paragraphs(), pattern=st.sampled_from(REGEXES))
    def it_finds_what_re_finditer_finds(self, runs: list[tuple[str, str | None]], pattern: str):
        paragraph = _paragraph(runs)
        text = paragraph.text

        matches = paragraph.find_all(pattern, regex=True)

        assert [(m.start, m.end, m.text) for m in matches] == [
            (m.start(), m.end(), m.group()) for m in re.finditer(pattern, text)
        ]
        for m in matches:
            assert "".join(r.text for r in m.runs).find(m.text) != -1
            assert all(r.text for r in m.runs)

    @PROPERTY_SETTINGS
    @given(runs=paragraphs())
    def it_merges_runs_without_changing_the_text_or_its_formatting(
        self, runs: list[tuple[str, str | None]]
    ):
        paragraph = _paragraph(runs)
        text, formats = paragraph.text, _char_formats(paragraph)

        paragraph.merge_runs()

        assert paragraph.text == text
        assert _char_formats(paragraph) == formats
        keys = [r._r.formatting_key() for r in paragraph.runs]
        assert all(a != b for a, b in zip(keys, keys[1:]))
