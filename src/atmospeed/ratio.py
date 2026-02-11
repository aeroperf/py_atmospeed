"""Atmospheric ratio calculations: theta, delta, sigma. All functions accept scalars or numpy arrays."""

import numpy as np

from .constants import (
    DELTA_AT_TROPOPAUSE,
    HEIGHT_STRATOPAUSE_FT,
    HEIGHT_TROPOPAUSE_FT,
    TEMP_SL_STD_K,
    TEMP_SL_STD_R,
    TROPOSPHERE_DELTA_EXP,
    TROPOPAUSE_CONST_US,
    ZERO_C_IN_K,
    ZERO_C_IN_R,
)
from .convert import length_to_feet
from .temperature import _validate_altitude, oat
from .units import TemperatureUnit


def theta(hp, delta_isa=0, alt_unit="ft", temp_unit="C"):
    """Calculate temperature ratio (theta = T / T_SL_std).

    Args:
        hp: Pressure altitude (scalar or array).
        delta_isa: Temperature deviation from ISA (default 0).
        alt_unit: Altitude unit (default "ft").
        temp_unit: Temperature unit (default "C").

    Returns:
        Temperature ratio theta.
    """
    temp_unit = TemperatureUnit(temp_unit)
    hp_ft = np.asarray(length_to_feet(hp, alt_unit), dtype=float)
    _validate_altitude(hp_ft)

    oat_val = oat(hp_ft, delta_isa, alt_unit="ft", temp_unit=temp_unit)

    if temp_unit == TemperatureUnit.C:
        return (oat_val + ZERO_C_IN_K) / TEMP_SL_STD_K
    elif temp_unit == TemperatureUnit.F:
        return (oat_val + ZERO_C_IN_R) / TEMP_SL_STD_R
    elif temp_unit == TemperatureUnit.K:
        return oat_val / TEMP_SL_STD_K
    elif temp_unit == TemperatureUnit.R:
        return oat_val / TEMP_SL_STD_R


def delta(hp, alt_unit="ft"):
    """Calculate pressure ratio (delta = P / P_SL_std).

    Args:
        hp: Pressure altitude (scalar or array).
        alt_unit: Altitude unit (default "ft").

    Returns:
        Pressure ratio delta.
    """
    hp_ft = np.asarray(length_to_feet(hp, alt_unit), dtype=float)
    _validate_altitude(hp_ft)

    in_tropo = hp_ft <= HEIGHT_TROPOPAUSE_FT

    # Troposphere: delta = theta^5.25588 (at ISA, delta_isa=0)
    theta_isa = theta(hp_ft, delta_isa=0, alt_unit="ft", temp_unit="C")
    tropo_delta = np.power(theta_isa, TROPOSPHERE_DELTA_EXP)

    # Stratosphere: delta = delta_trop * exp((h_trop - h) / const)
    strato_delta = DELTA_AT_TROPOPAUSE * np.exp(
        (HEIGHT_TROPOPAUSE_FT - hp_ft) / TROPOPAUSE_CONST_US
    )

    result = np.where(in_tropo, tropo_delta, strato_delta)
    return result.item() if np.ndim(result) == 0 else result


def sigma(hp, delta_isa=0, alt_unit="ft", temp_unit="C"):
    """Calculate density ratio (sigma = rho / rho_SL_std = delta / theta).

    Args:
        hp: Pressure altitude (scalar or array).
        delta_isa: Temperature deviation from ISA (default 0).
        alt_unit: Altitude unit (default "ft").
        temp_unit: Temperature unit (default "C").

    Returns:
        Density ratio sigma.
    """
    return delta(hp, alt_unit=alt_unit) / theta(
        hp, delta_isa=delta_isa, alt_unit=alt_unit, temp_unit=temp_unit
    )
