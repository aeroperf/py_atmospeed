"""Atmo class — defines an atmospheric point at a pressure altitude and temperature condition."""

import numpy as np

from .constants import A0_FPS, A0_KMH, A0_KTS, A0_MPH, A0_MPS
from .convert import length_to_feet
from .ratio import delta as calc_delta
from .ratio import sigma as calc_sigma
from .ratio import theta as calc_theta
from .temperature import calc_delta_isa as _calc_delta_isa
from .temperature import isa as calc_isa
from .temperature import oat as calc_oat
from .units import LengthUnit, SpeedUnit, TemperatureUnit


class Atmo:
    """Atmospheric point defined by pressure altitude and temperature condition.

    Args:
        hp: Pressure altitude.
        temperature: Temperature value. Interpreted as delta ISA by default,
            or as OAT if ``temp_is_delta_isa=False``.
        temp_is_delta_isa: If True (default), temperature is a delta ISA value.
            If False, temperature is OAT.
        alt_unit: Altitude unit (default "ft").
        temp_unit: Temperature unit (default "C").

    Raises:
        ValueError: If altitude is above the stratopause.
    """

    __slots__ = ("_hp", "_temperature", "_temp_is_delta_isa", "_alt_unit",
                 "_temp_unit", "_hp_ft", "_disa")

    def __init__(self, hp, temperature, temp_is_delta_isa=True,
                 alt_unit="ft", temp_unit="C"):
        self._hp = hp
        self._temperature = temperature
        self._temp_is_delta_isa = temp_is_delta_isa
        self._alt_unit = LengthUnit(alt_unit)
        self._temp_unit = TemperatureUnit(temp_unit)

        self._hp_ft = length_to_feet(hp, self._alt_unit)

        from .constants import HEIGHT_STRATOPAUSE_FT
        if self._hp_ft > HEIGHT_STRATOPAUSE_FT:
            raise ValueError("Altitude is above stratopause (20 km / 65617 ft)")

        if temp_is_delta_isa:
            self._disa = temperature
        else:
            self._disa = _calc_delta_isa(
                hp, temperature, alt_unit=self._alt_unit, temp_unit=self._temp_unit
            )

    def __repr__(self):
        return (f"Atmo(hp={self._hp} {self._alt_unit}, "
                f"temp={self._temperature} {self._temp_unit}, "
                f"is_delta_isa={self._temp_is_delta_isa})")

    @property
    def hp_ft(self):
        """Pressure altitude in feet."""
        return self._hp_ft

    @property
    def alt_unit(self):
        return self._alt_unit

    @property
    def temp_unit(self):
        return self._temp_unit

    @property
    def theta(self):
        """Temperature ratio."""
        return calc_theta(
            self._hp, delta_isa=self._disa,
            alt_unit=self._alt_unit, temp_unit=self._temp_unit
        )

    @property
    def delta(self):
        """Pressure ratio."""
        return calc_delta(self._hp, alt_unit=self._alt_unit)

    @property
    def sigma(self):
        """Density ratio."""
        return calc_sigma(
            self._hp, delta_isa=self._disa,
            alt_unit=self._alt_unit, temp_unit=self._temp_unit
        )

    @property
    def oat(self):
        """Outside air temperature in the Atmo point's temperature unit."""
        return calc_oat(
            self._hp, self._disa,
            alt_unit=self._alt_unit, temp_unit=self._temp_unit
        )

    @property
    def delta_isa(self):
        """Temperature deviation from ISA."""
        return self._disa

    @property
    def isa_temp(self):
        """ISA temperature in the Atmo point's temperature unit."""
        return calc_isa(self._hp, alt_unit=self._alt_unit, temp_unit=self._temp_unit)

    def speed_of_sound(self, speed_unit="kts"):
        """Speed of sound at this atmospheric point.

        Args:
            speed_unit: Output speed unit (default "kts").

        Returns:
            Speed of sound in the requested unit.
        """
        speed_unit = SpeedUnit(speed_unit)
        a0 = {
            SpeedUnit.KTS: A0_KTS,
            SpeedUnit.FPS: A0_FPS,
            SpeedUnit.MPH: A0_MPH,
            SpeedUnit.MPS: A0_MPS,
            SpeedUnit.KMH: A0_KMH,
        }[speed_unit]
        return a0 * np.sqrt(self.theta)

    def _disa_in_celsius(self):
        """Get delta ISA in Celsius regardless of the point's temperature unit."""
        if self._temp_unit in (TemperatureUnit.C, TemperatureUnit.K):
            return self._disa
        else:
            return self._disa / 1.8
