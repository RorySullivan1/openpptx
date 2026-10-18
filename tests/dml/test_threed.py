"""Unit-test suite for `openpptx.dml.threed` module."""

from __future__ import annotations

import pytest

from openpptx.dml.threed import Bevel, Camera
from openpptx.enum.dml import MSO_BEVEL_PRESET

from ..unitutil.cxml import element, xml


class DescribeBevel:
    """Unit-test suite for `openpptx.dml.threed.Bevel`."""

    def it_returns_None_for_preset_when_not_set(self):
        bevel = Bevel(element("a:bevelT"))
        assert bevel.preset is None

    @pytest.mark.parametrize(
        ("bevel_cxml", "expected_value"),
        [
            ("a:bevelT{prst=circle}", MSO_BEVEL_PRESET.CIRCLE),
            ("a:bevelT{prst=relaxedInset}", MSO_BEVEL_PRESET.RELAXED_INSET),
            ("a:bevelT{prst=artDeco}", MSO_BEVEL_PRESET.ART_DECO),
        ],
    )
    def it_returns_the_preset_as_an_enum_member(
        self, bevel_cxml: str, expected_value: MSO_BEVEL_PRESET
    ):
        bevel = Bevel(element(bevel_cxml))
        assert bevel.preset == expected_value

    def it_can_set_the_preset_with_an_enum_member(self):
        bevel = Bevel(element("a:bevelT"))
        bevel.preset = MSO_BEVEL_PRESET.CIRCLE
        assert bevel._bevel.xml == xml("a:bevelT{prst=circle}")

    def it_can_set_the_preset_with_a_legacy_string(self):
        bevel = Bevel(element("a:bevelT"))
        bevel.preset = "convex"
        assert bevel._bevel.xml == xml("a:bevelT{prst=convex}")

    def it_can_clear_the_preset_with_None(self):
        bevel = Bevel(element("a:bevelT{prst=circle}"))
        bevel.preset = None
        assert bevel._bevel.xml == xml("a:bevelT")


class DescribeCamera:
    """Unit-test suite for `openpptx.dml.threed.Camera` objects."""

    @pytest.mark.parametrize(
        ("camera_cxml", "expected_value"),
        [
            ("a:camera{prst=perspectiveFront,fov=2700000}", 45.0),
            ("a:camera{prst=perspectiveFront,fov=5400000}", 90.0),
            ("a:camera{prst=orthographicFront}", None),
        ],
    )
    def it_knows_its_field_of_view_in_degrees(self, camera_cxml: str, expected_value):
        assert Camera(element(camera_cxml)).field_of_view == expected_value

    @pytest.mark.parametrize(
        ("value", "expected_cxml"),
        [
            (45, "a:camera{prst=perspectiveFront,fov=2700000}"),
            (30.5, "a:camera{prst=perspectiveFront,fov=1830000}"),
            (None, "a:camera{prst=perspectiveFront}"),
        ],
    )
    def it_can_change_its_field_of_view(self, value, expected_cxml: str):
        camera = Camera(element("a:camera{prst=perspectiveFront,fov=600000}"))
        camera.field_of_view = value
        assert camera._camera.xml == xml(expected_cxml)
