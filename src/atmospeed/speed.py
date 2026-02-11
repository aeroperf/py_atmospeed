"""Speed class — defines a speed value with type and unit, and converts between speed types."""

from .atmo import Atmo
from .convert import speed_convert, speed_from_knots, speed_to_knots
from .units import SpeedType, SpeedUnit
from . import _speed_conv as sc


class Speed:
    """A speed value with a type (CAS, EAS, TAS, Mach) and unit.

    Args:
        value: Speed value.
        speed_type: One of "cas", "eas", "tas", "mach".
        speed_unit: Speed unit (default "kts"). Ignored for Mach input.

    Note:
        When converting to another speed type, the output unit matches
        the input unit. Mach output is always unitless.
    """

    __slots__ = ("_value", "_type", "_unit", "_kts")

    def __init__(self, value, speed_type, speed_unit="kts"):
        self._value = value
        self._type = SpeedType(speed_type)
        self._unit = SpeedUnit(speed_unit)
        self._kts = speed_to_knots(value, self._unit)

    def __repr__(self):
        return f"Speed({self._value} {self._type} {self._unit})"

    @property
    def value(self):
        return self._value

    @property
    def speed_type(self):
        return self._type

    @property
    def speed_unit(self):
        return self._unit

    def to_cas(self, atmo: Atmo) -> float:
        """Convert to Calibrated Airspeed at the given atmospheric point."""
        if self._type == SpeedType.CAS:
            return self._value
        hp_ft = atmo.hp_ft
        disa_c = atmo._disa_in_celsius()
        if self._type == SpeedType.EAS:
            result_kts = sc.keas_to_kcas(self._kts, hp_ft)
        elif self._type == SpeedType.TAS:
            result_kts = sc.ktas_to_kcas(self._kts, hp_ft, disa_c)
        elif self._type == SpeedType.MACH:
            result_kts = sc.mach_to_kcas(self._value, hp_ft)
        return speed_from_knots(result_kts, self._unit)

    def to_eas(self, atmo: Atmo) -> float:
        """Convert to Equivalent Airspeed at the given atmospheric point."""
        if self._type == SpeedType.EAS:
            return self._value
        hp_ft = atmo.hp_ft
        disa_c = atmo._disa_in_celsius()
        if self._type == SpeedType.CAS:
            result_kts = sc.kcas_to_keas(self._kts, hp_ft)
        elif self._type == SpeedType.TAS:
            result_kts = sc.ktas_to_keas(self._kts, hp_ft, disa_c)
        elif self._type == SpeedType.MACH:
            result_kts = sc.mach_to_keas(self._value, hp_ft)
        return speed_from_knots(result_kts, self._unit)

    def to_tas(self, atmo: Atmo) -> float:
        """Convert to True Airspeed at the given atmospheric point."""
        if self._type == SpeedType.TAS:
            return self._value
        hp_ft = atmo.hp_ft
        disa_c = atmo._disa_in_celsius()
        if self._type == SpeedType.CAS:
            result_kts = sc.kcas_to_ktas(self._kts, hp_ft, disa_c)
        elif self._type == SpeedType.EAS:
            result_kts = sc.keas_to_ktas(self._kts, hp_ft, disa_c)
        elif self._type == SpeedType.MACH:
            result_kts = sc.mach_to_ktas(self._value, hp_ft, disa_c)
        return speed_from_knots(result_kts, self._unit)

    def to_mach(self, atmo: Atmo) -> float:
        """Convert to Mach number at the given atmospheric point."""
        if self._type == SpeedType.MACH:
            return self._value
        hp_ft = atmo.hp_ft
        disa_c = atmo._disa_in_celsius()
        if self._type == SpeedType.CAS:
            return sc.kcas_to_mach(self._kts, hp_ft)
        elif self._type == SpeedType.EAS:
            return sc.keas_to_mach(self._kts, hp_ft)
        elif self._type == SpeedType.TAS:
            return sc.ktas_to_mach(self._kts, hp_ft, disa_c)

    def convert_unit(self, from_unit, to_unit) -> float:
        """Convert the speed value between units (e.g., knots to ft/s)."""
        return speed_convert(self._value, from_unit, to_unit)
