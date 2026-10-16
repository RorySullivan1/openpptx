"""Unit-test suite for the `pptx.oxml.text` module."""

from __future__ import annotations

from typing import cast

import pytest

from pptx.oxml.text import CT_RegularTextRun, CT_TextCharacterProperties, CT_TextParagraph

from ..unitutil.cxml import element, xml


class DescribeCT_TextParagraph:
    """Unit-test suite for `pptx.oxml.text.CT_TextParagraph` objects."""

    @pytest.mark.parametrize(
        ("p_cxml", "expected_value"),
        [
            ("a:p", []),
            ("a:p/(a:pPr,a:endParaRPr)", []),
            ('a:p/a:r/a:t"foo"', [(0, ["foo"])]),
            ('a:p/(a:r/a:t"foo",a:r/a:t"bar")', [(0, ["foo", "bar"])]),
            ('a:p/(a:r/a:t"foo",a:br,a:r/a:t"bar")', [(0, ["foo"]), (4, ["bar"])]),
            ('a:p/(a:fld/a:t"12",a:r/a:t"ab",a:r/a:t"c")', [(2, ["ab", "c"])]),
            ('a:p/(a:r/a:t"a",a:fld/a:t"xyz",a:br,a:r/a:t"b")', [(0, ["a"]), (5, ["b"])]),
            ("a:p/(a:pPr,a:r/a:t,a:endParaRPr)", [(0, [""])]),
        ],
    )
    def it_splits_its_runs_into_segments(self, p_cxml: str, expected_value: list):
        p = cast(CT_TextParagraph, element(p_cxml))

        segments = p.run_segments()

        assert [(start, [r.text for r in rs]) for start, rs in segments] == expected_value

    def it_offsets_each_segment_into_the_paragraph_text(self):
        p = cast(
            CT_TextParagraph,
            element('a:p/(a:r/a:t"ab",a:br,a:fld/a:t"7",a:r/a:t"cd",a:r/a:t"e",a:br,a:r/a:t"f")'),
        )
        text = p.text

        for start, rs in p.run_segments():
            seg_text = "".join(r.text for r in rs)
            assert text[start : start + len(seg_text)] == seg_text


class DescribeCT_TextCharacterProperties:
    """Unit-test suite for `pptx.oxml.text.CT_TextCharacterProperties` objects."""

    @pytest.mark.parametrize(
        ("rPr_cxml", "other_cxml"),
        [
            ("a:rPr", "a:rPr"),
            ("a:rPr{dirty=0}", "a:rPr"),
            ("a:rPr{lang=en-US,err=1}", "a:rPr{lang=en-US}"),
            ("a:rPr{b=1,smtClean=0}", "a:rPr{b=1,dirty=0}"),
            ("a:rPr{smtId=4}", "a:rPr{err=1,dirty=0,smtClean=0}"),
            ("a:rPr{b=1,i=0}", "a:rPr{i=0,b=1}"),
            (
                "a:rPr{sz=1200,err=1}/a:solidFill/a:srgbClr{val=FF0000}",
                "a:rPr{sz=1200}/a:solidFill/a:srgbClr{val=FF0000}",
            ),
        ],
    )
    def it_has_a_formatting_key_that_ignores_proofing_state(self, rPr_cxml: str, other_cxml: str):
        rPr = cast(CT_TextCharacterProperties, element(rPr_cxml))
        other = cast(CT_TextCharacterProperties, element(other_cxml))
        assert rPr.formatting_key() == other.formatting_key()

    @pytest.mark.parametrize(
        ("rPr_cxml", "other_cxml"),
        [
            ("a:rPr{b=1}", "a:rPr"),
            ("a:rPr{b=1}", "a:rPr{b=0}"),
            ("a:rPr{i=1}", "a:rPr"),
            ("a:rPr{sz=1200}", "a:rPr{sz=1400}"),
            ("a:rPr{baseline=30000}", "a:rPr"),
            ("a:rPr{lang=en-US}", "a:rPr{lang=fr-FR}"),
            (
                "a:rPr/a:solidFill/a:srgbClr{val=FF0000}",
                "a:rPr/a:solidFill/a:srgbClr{val=00FF00}",
            ),
            ("a:rPr/a:latin{typeface=Arial}", "a:rPr"),
            ("a:rPr/a:hlinkClick{r:id=rId1}", "a:rPr/a:hlinkClick{r:id=rId2}"),
        ],
    )
    def but_it_gives_a_different_key_when_the_formatting_differs(
        self, rPr_cxml: str, other_cxml: str
    ):
        rPr = cast(CT_TextCharacterProperties, element(rPr_cxml))
        other = cast(CT_TextCharacterProperties, element(other_cxml))
        assert rPr.formatting_key() != other.formatting_key()

    @pytest.mark.parametrize("rPr_cxml", ["a:rPr", "a:rPr{dirty=0,err=1,smtClean=0,smtId=7}"])
    def and_it_gives_the_empty_key_to_an_rPr_without_formatting(self, rPr_cxml: str):
        rPr = cast(CT_TextCharacterProperties, element(rPr_cxml))
        assert rPr.formatting_key() == ()

    def and_it_makes_the_key_hashable(self):
        rPr = cast(CT_TextCharacterProperties, element("a:rPr{b=1}/a:latin{typeface=Arial}"))
        assert hash(rPr.formatting_key()) == hash(rPr.formatting_key())


class DescribeCT_RegularTextRun:
    """Unit-test suite for `pptx.oxml.text.CT_RegularTextRun` objects."""

    @pytest.mark.parametrize(
        ("p_cxml", "lines", "expected_cxml"),
        [
            ('a:p/a:r/a:t"a"', [], 'a:p/a:r/a:t"a"'),
            ('a:p/a:r/a:t"a"', ["b"], 'a:p/(a:r/a:t"a",a:br,a:r/a:t"b")'),
            (
                'a:p/(a:r/(a:rPr{b=1},a:t"a"),a:r/a:t"z")',
                ["b", "", "c"],
                'a:p/(a:r/(a:rPr{b=1},a:t"a"),a:br/a:rPr{b=1},a:r/(a:rPr{b=1},a:t"b"),'
                'a:br/a:rPr{b=1},a:br/a:rPr{b=1},a:r/(a:rPr{b=1},a:t"c"),a:r/a:t"z")',
            ),
        ],
    )
    def it_can_insert_lines_after_itself(self, p_cxml: str, lines: list[str], expected_cxml: str):
        p = cast(CT_TextParagraph, element(p_cxml))

        p.r_lst[0].insert_lines_after(lines)

        assert p.xml == xml(expected_cxml)

    def and_it_gives_each_new_line_its_own_copy_of_the_formatting(self):
        p = cast(CT_TextParagraph, element('a:p/a:r/(a:rPr{b=1},a:t"a")'))
        r = p.r_lst[0]

        r.insert_lines_after(["b"])

        br, new_r = p.content_children[1:]
        assert br.rPr is not r.rPr and new_r.rPr is not r.rPr
        assert br.rPr is not None and new_r.rPr is not None

    @pytest.mark.parametrize(
        ("r_cxml", "expected_value"),
        [
            ('a:r/a:t"a"', []),
            ('a:r/(a:rPr/a:hlinkClick{r:id=rId2},a:t"a")', ["rId2"]),
            (
                'a:r/(a:rPr/(a:hlinkClick{r:id=rId2},a:hlinkMouseOver{r:id=rId2}),a:t"a")',
                ["rId2", "rId2"],
            ),
            ('a:r/(a:rPr/a:blipFill/a:blip{r:embed=rId4},a:t"a")', ["rId4"]),
        ],
    )
    def it_knows_the_relationships_it_refers_to(self, r_cxml: str, expected_value: list[str]):
        r = cast(CT_RegularTextRun, element(r_cxml))
        assert r.rel_ids == expected_value
