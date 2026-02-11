"""Unit conversion functions for length and speed. All functions accept scalars or numpy arrays."""

import numpy as np

from .units import LengthUnit, SpeedUnit

# Length conversion constants
_METERS_PER_FOOT = 0.3048
_FEET_PER_STATUTE_MILE = 5280.0
_FEET_PER_NAUTICAL_MILE = 6076.11549

# Speed conversion constants (from knots)
_KTS_TO_FPS = 1.6878
_KTS_TO_MPS = 0.51444
_KTS_TO_KMH = 1.8520
_KTS_TO_MPH = 1.1508


def length_to_feet(value, from_unit):
    """Convert a length value to feet."""
    from_unit = LengthUnit(from_unit)
    if from_unit == LengthUnit.FT:
        return value
    if from_unit == LengthUnit.M:
        return value / _METERS_PER_FOOT
    if from_unit == LengthUnit.KM:
        return value * 1000.0 / _METERS_PER_FOOT
    if from_unit == LengthUnit.SM:
        return value * _FEET_PER_STATUTE_MILE
    if from_unit == LengthUnit.NM:
        return value * _FEET_PER_NAUTICAL_MILE


def length_convert(value, from_unit, to_unit):
    """Convert a length value between any two units."""
    to_unit = LengthUnit(to_unit)
    feet = length_to_feet(value, from_unit)
    if to_unit == LengthUnit.FT:
        return feet
    if to_unit == LengthUnit.M:
        return feet * _METERS_PER_FOOT
    if to_unit == LengthUnit.KM:
        return feet * _METERS_PER_FOOT / 1000.0
    if to_unit == LengthUnit.SM:
        return feet / _FEET_PER_STATUTE_MILE
    if to_unit == LengthUnit.NM:
        return feet / _FEET_PER_NAUTICAL_MILE


def speed_to_knots(value, from_unit):
    """Convert a speed value to knots."""
    from_unit = SpeedUnit(from_unit)
    if from_unit == SpeedUnit.KTS:
        return value
    if from_unit == SpeedUnit.FPS:
        return value / _KTS_TO_FPS
    if from_unit == SpeedUnit.MPH:
        return value / _KTS_TO_MPH
    if from_unit == SpeedUnit.MPS:
        return value / _KTS_TO_MPS
    if from_unit == SpeedUnit.KMH:
        return value / _KTS_TO_KMH


def speed_from_knots(value_kts, to_unit):
    """Convert a speed value from knots to another unit."""
    to_unit = SpeedUnit(to_unit)
    if to_unit == SpeedUnit.KTS:
        return value_kts
    if to_unit == SpeedUnit.FPS:
        return value_kts * _KTS_TO_FPS
    if to_unit == SpeedUnit.MPH:
        return value_kts * _KTS_TO_MPH
    if to_unit == SpeedUnit.MPS:
        return value_kts * _KTS_TO_MPS
    if to_unit == SpeedUnit.KMH:
        return value_kts * _KTS_TO_KMH


def speed_convert(value, from_unit, to_unit):
    """Convert a speed value between any two units."""
    return speed_from_knots(speed_to_knots(value, from_unit), to_unit)
