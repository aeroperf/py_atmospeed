"""ISA temperature, OAT, and delta ISA calculations. All functions accept scalars or numpy arrays."""

import numpy as np

from .constants import (
    HEIGHT_STRATOPAUSE_FT,
    HEIGHT_TROPOPAUSE_FT,
    LAPSE_RATE_C_PER_FT,
    LAPSE_RATE_F_PER_FT,
    TEMP_SL_STD_C,
    TEMP_SL_STD_F,
    TEMP_SL_STD_K,
    TEMP_SL_STD_R,
    TEMP_STRATOSPHERE_C,
    TEMP_STRATOSPHERE_F,
    ZERO_C_IN_K,
    ZERO_C_IN_R,
)
from .convert import length_to_feet
from .units import LengthUnit, TemperatureUnit


def isa(hp, alt_unit="ft", temp_unit="C"):
    """Calculate ISA (International Standard Atmosphere) temperature at a pressure altitude.

    Args:
        hp: Pressure altitude (scalar or array).
        alt_unit: Altitude unit (default "ft").
        temp_unit: Output temperature unit (default "C").

    Returns:
        ISA temperature in the requested unit.

    Raises:
        ValueError: If altitude is above the stratopause (20 km / 65617 ft).
    """
    temp_unit = TemperatureUnit(temp_unit)
    hp_ft = np.asarray(length_to_feet(hp, alt_unit), dtype=float)

    _validate_altitude(hp_ft)

    in_tropo = hp_ft <= HEIGHT_TROPOPAUSE_FT

    if temp_unit == TemperatureUnit.C:
        tropo = TEMP_SL_STD_C - LAPSE_RATE_C_PER_FT * hp_ft
        strato = np.full_like(hp_ft, TEMP_STRATOSPHERE_C)
    elif temp_unit == TemperatureUnit.F:
        tropo = TEMP_SL_STD_F - LAPSE_RATE_F_PER_FT * hp_ft
        strato = np.full_like(hp_ft, TEMP_STRATOSPHERE_F)
    elif temp_unit == TemperatureUnit.K:
        tropo = TEMP_SL_STD_K - LAPSE_RATE_C_PER_FT * hp_ft
        strato = np.full_like(hp_ft, TEMP_STRATOSPHERE_C + ZERO_C_IN_K)
    elif temp_unit == TemperatureUnit.R:
        tropo = TEMP_SL_STD_R - LAPSE_RATE_F_PER_FT * hp_ft
        strato = np.full_like(hp_ft, TEMP_STRATOSPHERE_F + ZERO_C_IN_R)

    result = np.where(in_tropo, tropo, strato)
    return result.item() if result.ndim == 0 else result


def oat(hp, delta_isa, alt_unit="ft", temp_unit="C"):
    """Calculate Outside Air Temperature from pressure altitude and delta ISA.

    Args:
        hp: Pressure altitude (scalar or array).
        delta_isa: Temperature deviation from ISA (scalar or array).
        alt_unit: Altitude unit (default "ft").
        temp_unit: Temperature unit (default "C").

    Returns:
        OAT in the requested unit.
    """
    return isa(hp, alt_unit=alt_unit, temp_unit=temp_unit) + delta_isa


def calc_delta_isa(hp, oat_value, alt_unit="ft", temp_unit="C"):
    """Calculate temperature deviation from ISA for a given pressure altitude and OAT.

    Args:
        hp: Pressure altitude (scalar or array).
        oat_value: Outside air temperature (scalar or array).
        alt_unit: Altitude unit (default "ft").
        temp_unit: Temperature unit (default "C").

    Returns:
        Delta ISA in the requested unit.
    """
    return oat_value - isa(hp, alt_unit=alt_unit, temp_unit=temp_unit)


def _validate_altitude(hp_ft):
    """Raise ValueError if any altitude exceeds the stratopause."""
    hp_arr = np.asarray(hp_ft)
    if np.any(hp_arr > HEIGHT_STRATOPAUSE_FT):
        raise ValueError("Altitude is above stratopause (20 km / 65617 ft)")
