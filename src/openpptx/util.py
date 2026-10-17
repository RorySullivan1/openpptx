"""Length units: |Length| and its subclasses |Emu|, |Inches|, |Cm|, |Mm|, |Pt| and |Centipoints|."""

from __future__ import annotations


class Length(int):
    """Base class for length classes Inches, Emu, Cm, Mm, and Pt.

    Provides properties for converting length values to convenient units.
    """

    _EMUS_PER_INCH = 914400
    _EMUS_PER_CENTIPOINT = 127
    _EMUS_PER_CM = 360000
    _EMUS_PER_MM = 36000
    _EMUS_PER_PT = 12700

    def __new__(cls, emu: int):
        return int.__new__(cls, emu)

    @property
    def inches(self) -> float:
        """Floating point length in inches."""
        return self / float(self._EMUS_PER_INCH)

    @property
    def centipoints(self) -> int:
        """Integer length in hundredths of a point (1/7200 inch).

        Used internally because PowerPoint stores font size in centipoints.
        """
        return self // self._EMUS_PER_CENTIPOINT

    @property
    def cm(self) -> float:
        """Floating point length in centimeters."""
        return self / float(self._EMUS_PER_CM)

    @property
    def emu(self) -> int:
        """Integer length in English Metric Units."""
        return self

    @property
    def mm(self) -> float:
        """Floating point length in millimeters."""
        return self / float(self._EMUS_PER_MM)

    @property
    def pt(self) -> float:
        """Floating point length in points."""
        return self / float(self._EMUS_PER_PT)


class Inches(Length):
    """Convenience constructor for length in inches."""

    def __new__(cls, inches: float):
        emu = int(inches * Length._EMUS_PER_INCH)
        return Length.__new__(cls, emu)


class Centipoints(Length):
    """Convenience constructor for length in hundredths of a point."""

    def __new__(cls, centipoints: int):
        emu = int(centipoints * Length._EMUS_PER_CENTIPOINT)
        return Length.__new__(cls, emu)


class Cm(Length):
    """Convenience constructor for length in centimeters."""

    def __new__(cls, cm: float):
        emu = int(cm * Length._EMUS_PER_CM)
        return Length.__new__(cls, emu)


class Emu(Length):
    """Convenience constructor for length in english metric units."""

    def __new__(cls, emu: int):
        return Length.__new__(cls, int(emu))


class Mm(Length):
    """Convenience constructor for length in millimeters."""

    def __new__(cls, mm: float):
        emu = int(mm * Length._EMUS_PER_MM)
        return Length.__new__(cls, emu)


class Pt(Length):
    """Convenience value class for specifying a length in points."""

    def __new__(cls, points: float):
        emu = int(points * Length._EMUS_PER_PT)
        return Length.__new__(cls, emu)
