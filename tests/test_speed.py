"""Tests for speed conversions — both internal functions and Speed class.
Ported from Dart atmospeed_test.dart with identical expected values."""

import pytest
from atmospeed import Atmo, Speed
from atmospeed._speed_conv import (
    kcas_to_keas, kcas_to_ktas, kcas_to_mach,
    keas_to_kcas, keas_to_ktas, keas_to_mach,
    ktas_to_kcas, ktas_to_keas, ktas_to_mach,
    mach_to_kcas, mach_to_keas, mach_to_ktas,
)


class TestKCASConversions:
    def test_kcas_to_keas(self):
        assert kcas_to_keas(287.3, 26788) == pytest.approx(276.2, abs=0.1)

    def test_kcas_to_ktas(self):
        assert kcas_to_ktas(287.3, 26788, 0) == pytest.approx(426.0, abs=0.1)

    def test_kcas_to_mach(self):
        assert kcas_to_mach(287.3, 26788) == pytest.approx(0.7130, abs=0.001)


class TestKEASConversions:
    def test_keas_to_kcas(self):
        assert keas_to_kcas(219.4, 38405) == pytest.approx(231.3, abs=0.1)

    def test_keas_to_kcas_high(self):
        assert keas_to_kcas(519.4, 38405) == pytest.approx(656.0, abs=0.1)

    def test_keas_to_ktas(self):
        assert keas_to_ktas(133.7, 13678, 0) == pytest.approx(165.0, abs=0.1)

    def test_keas_to_mach(self):
        assert keas_to_mach(333.3, 30538) == pytest.approx(0.9361, abs=0.001)


class TestKTASConversions:
    def test_ktas_to_keas(self):
        assert ktas_to_keas(389.4, 17408, 0) == pytest.approx(296.9, abs=0.1)

    def test_ktas_to_kcas(self):
        assert ktas_to_kcas(507.5, 43777, 0) == pytest.approx(248.6, abs=0.1)

    def test_ktas_to_mach(self):
        assert ktas_to_mach(287.3, 7564, 0) == pytest.approx(0.4461, abs=0.001)


class TestMachConversions:
    def test_mach_to_keas(self):
        assert mach_to_keas(0.4706, 4862) == pytest.approx(284.7, abs=0.1)

    def test_mach_to_ktas(self):
        assert mach_to_ktas(0.9127, 39422, 0) == pytest.approx(523.5, abs=0.1)

    def test_mach_to_kcas(self):
        assert mach_to_kcas(0.74, 21755) == pytest.approx(331.6, abs=0.1)


class TestSpeedClassToCAS:
    def test_eas_to_cas_kts(self):
        spd = Speed(219.4, "eas")
        assert spd.to_cas(Atmo(hp=38405, temperature=0)) == pytest.approx(231.3, abs=0.1)

    def test_eas_to_cas_mps(self):
        spd = Speed(112.87, "eas", speed_unit="mps")
        assert spd.to_cas(Atmo(hp=38405, temperature=0)) == pytest.approx(119.0, abs=0.1)

    def test_tas_to_cas_fps_disa15(self):
        spd = Speed(719.7, "tas", speed_unit="fps")
        assert spd.to_cas(Atmo(hp=33485, temperature=15)) == pytest.approx(417.5, abs=0.1)

    def test_tas_to_cas_fps_m_f(self):
        spd = Speed(719.7, "tas", speed_unit="fps")
        atmo = Atmo(hp=5777, temperature=-13, alt_unit="m", temp_unit="F")
        assert spd.to_cas(atmo) == pytest.approx(558.8, abs=0.1)

    def test_mach_to_cas(self):
        spd = Speed(0.4916, "mach")
        atmo = Atmo(hp=1.67, temperature=0, alt_unit="nm")
        assert spd.to_cas(atmo) == pytest.approx(271.4, abs=0.1)


class TestSpeedClassToEAS:
    def test_cas_to_eas_kts(self):
        spd = Speed(148.7, "cas")
        assert spd.to_eas(Atmo(hp=6944, temperature=0)) == pytest.approx(148.4, abs=0.1)

    def test_cas_to_eas_kmh(self):
        spd = Speed(528.4, "cas", speed_unit="kmh")
        assert spd.to_eas(Atmo(hp=37844, temperature=0)) == pytest.approx(491.3, abs=0.1)

    def test_tas_to_eas_kts_disa_neg24(self):
        spd = Speed(285.3, "tas")
        assert spd.to_eas(Atmo(hp=37844, temperature=-24)) == pytest.approx(158.1, abs=0.1)

    def test_tas_to_eas_fps_disa33f(self):
        spd = Speed(337.6, "tas", speed_unit="fps")
        atmo = Atmo(hp=16543, temperature=33, temp_unit="F")
        assert spd.to_eas(atmo) == pytest.approx(252.2, abs=0.1)

    def test_mach_to_eas(self):
        spd = Speed(0.6385, "mach")
        atmo = Atmo(hp=10075.5, temperature=0, alt_unit="m")
        assert spd.to_eas(atmo) == pytest.approx(214.5, abs=0.1)


class TestSpeedClassToTAS:
    def test_cas_to_tas_kts(self):
        spd = Speed(148.7, "cas")
        assert spd.to_tas(Atmo(hp=6944, temperature=0)) == pytest.approx(164.7, abs=0.1)

    def test_cas_to_tas_mph_disa17(self):
        spd = Speed(281.7, "cas", speed_unit="mph")
        assert spd.to_tas(Atmo(hp=37844, temperature=17)) == pytest.approx(529.2, abs=0.1)

    def test_eas_to_tas_kts_disa_neg24f(self):
        spd = Speed(285.3, "eas")
        atmo = Atmo(hp=23030, temperature=-24, temp_unit="F")
        assert spd.to_tas(atmo) == pytest.approx(400.2, abs=0.1)

    def test_eas_to_tas_mps_disa33(self):
        spd = Speed(90, "eas", speed_unit="mps")
        assert spd.to_tas(Atmo(hp=16543, temperature=33)) == pytest.approx(123.6, abs=0.1)

    def test_mach_to_tas_disa11f(self):
        spd = Speed(0.8474, "mach")
        assert spd.to_tas(Atmo(hp=47854, temperature=11, temp_unit="F")) == pytest.approx(492.8, abs=0.1)

    def test_tas_to_tas_identity(self):
        spd = Speed(333.0, "tas", speed_unit="mph")
        atmo = Atmo(hp=8888.0, temperature=33, alt_unit="m", temp_unit="F",
                    temp_is_delta_isa=True)
        assert spd.to_tas(atmo) == pytest.approx(333.0, abs=0.1)


class TestSpeedClassToMach:
    def test_cas_to_mach_kts(self):
        spd = Speed(148.7, "cas")
        assert spd.to_mach(Atmo(hp=6944, temperature=0)) == pytest.approx(0.2552, abs=0.0001)

    def test_cas_to_mach_mph(self):
        spd = Speed(281.7, "cas", speed_unit="mph")
        assert spd.to_mach(Atmo(hp=37844, temperature=0)) == pytest.approx(0.7721, abs=0.0001)

    def test_eas_to_mach(self):
        spd = Speed(285.3, "eas")
        assert spd.to_mach(Atmo(hp=23030, temperature=0)) == pytest.approx(0.6785, abs=0.0001)

    def test_tas_to_mach_mps(self):
        spd = Speed(387.4, "tas", speed_unit="mps")
        assert spd.to_mach(Atmo(hp=38495, temperature=-23)) == pytest.approx(1.389, abs=0.001)

    def test_tas_to_mach_disa11f(self):
        spd = Speed(513.4, "tas")
        atmo = Atmo(hp=39000, temperature=21, temp_unit="F")
        assert spd.to_mach(atmo) == pytest.approx(0.8719, abs=0.0001)


class TestSpeedUnitConversion:
    def test_kts_to_fps(self):
        spd = Speed(148.7, "cas")
        assert spd.convert_unit("kts", "fps") == pytest.approx(251.0, abs=0.1)

    def test_fps_to_mps(self):
        spd = Speed(148.7, "cas", speed_unit="fps")
        assert spd.convert_unit("fps", "mps") == pytest.approx(45.3, abs=0.1)

    def test_kmh_to_mph(self):
        spd = Speed(148.7, "cas", speed_unit="kmh")
        assert spd.convert_unit("kmh", "mph") == pytest.approx(92.4, abs=0.1)

    def test_standalone_speed_convert(self):
        from atmospeed import speed_convert
        assert speed_convert(147.8, "kts", "fps") == pytest.approx(249.5, abs=0.1)
