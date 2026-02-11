"""Unit enumerations for length, speed, temperature, pressure, and speed type."""

from enum import StrEnum


class LengthUnit(StrEnum):
    FT = "ft"
    M = "m"
    KM = "km"
    SM = "sm"  # statute miles
    NM = "nm"  # nautical miles


class PressureUnit(StrEnum):
    HPA = "hPa"
    INHG = "inHg"


class SpeedUnit(StrEnum):
    KTS = "kts"
    FPS = "fps"
    MPH = "mph"
    MPS = "mps"
    KMH = "kmh"


class TemperatureUnit(StrEnum):
    C = "C"
    F = "F"
    K = "K"
    R = "R"


class SpeedType(StrEnum):
    CAS = "cas"
    EAS = "eas"
    TAS = "tas"
    MACH = "mach"
