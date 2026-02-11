"""Pressure altitude calculation from airport elevation and altimeter setting."""

import numpy as np

from .constants import (
    PRESSURE_CALC_CONST,
    PRESSURE_CALC_EXP,
    PRESSURE_SL_STD_HPA,
    PRESSURE_SL_STD_INHG,
)
from .convert import length_convert, length_to_feet
from .units import LengthUnit, PressureUnit


def pressure_altitude(elevation, altimeter, elev_unit="ft", altimeter_unit="inHg"):
    """Calculate pressure altitude from airport elevation and altimeter setting (QNH).

    Args:
        elevation: Airport elevation.
        altimeter: Altimeter setting (QNH).
        elev_unit: Elevation unit (default "ft").
        altimeter_unit: Pressure unit (default "inHg").

    Returns:
        Pressure altitude in the same unit as the elevation input.
    """
    elev_unit = LengthUnit(elev_unit)
    altimeter_unit = PressureUnit(altimeter_unit)

    elev_ft = length_to_feet(elevation, elev_unit)

    p_sl = (PRESSURE_SL_STD_INHG if altimeter_unit == PressureUnit.INHG
            else PRESSURE_SL_STD_HPA)

    hp_ft = elev_ft + PRESSURE_CALC_CONST * (
        1.0 - np.power(altimeter / p_sl, PRESSURE_CALC_EXP)
    )

    if elev_unit == LengthUnit.FT:
        return hp_ft
    return length_convert(hp_ft, LengthUnit.FT, elev_unit)
