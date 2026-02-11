"""Tests for atmospheric properties: ISA, OAT, delta ISA, theta, delta, sigma, speed of sound.
Ported from Dart atmospeed_test.dart with identical expected values."""

import pytest
import numpy as np
from atmospeed import Atmo, theta, delta, sigma, isa, oat, calc_delta_isa


class TestISA:
    def test_troposphere_celsius(self):
        atmo = Atmo(hp=24555.0, temperature=0)
        assert atmo.isa_temp == pytest.approx(-33.65, abs=0.02)

    def test_stratosphere_fahrenheit(self):
        atmo = Atmo(hp=43555.0, temperature=0, temp_unit="F")
        assert atmo.isa_temp == pytest.approx(-69.7)

    def test_troposphere_meters_celsius(self):
        atmo = Atmo(hp=7484.4, temperature=0, alt_unit="m")
        assert atmo.isa_temp == pytest.approx(-33.65, abs=0.02)

    def test_stratosphere_nm_fahrenheit(self):
        atmo = Atmo(hp=7.168, temperature=0, alt_unit="nm", temp_unit="F")
        assert atmo.isa_temp == pytest.approx(-69.7)


class TestOAT:
    def test_troposphere_celsius(self):
        atmo = Atmo(hp=31000.0, temperature=6.0)
        assert atmo.oat == pytest.approx(-40.425, abs=0.01)

    def test_troposphere_meters_kelvin(self):
        atmo = Atmo(hp=9448.8, temperature=6, alt_unit="m", temp_unit="K")
        assert atmo.oat == pytest.approx(232.725, abs=0.01)

    def test_stratosphere_celsius(self):
        atmo = Atmo(hp=41000.0, temperature=6.0)
        assert atmo.oat == pytest.approx(-50.5, abs=0.01)

    def test_troposphere_fahrenheit(self):
        atmo = Atmo(hp=31000.0, temperature=-10.8, temp_unit="F")
        assert atmo.oat == pytest.approx(-62.36, abs=0.01)

    def test_stratosphere_fahrenheit(self):
        atmo = Atmo(hp=41000.0, temperature=10.8, temp_unit="F")
        assert atmo.oat == pytest.approx(-58.9, abs=0.01)

    def test_stratosphere_sm_fahrenheit(self):
        atmo = Atmo(hp=7.765, temperature=10.8, alt_unit="sm", temp_unit="F")
        assert atmo.oat == pytest.approx(-58.9, abs=0.01)


class TestDeltaISA:
    def test_troposphere_celsius(self):
        atmo = Atmo(hp=31000.0, temperature=-40.42, temp_is_delta_isa=False)
        assert atmo.delta_isa == pytest.approx(6.0, abs=0.01)

    def test_stratosphere_celsius(self):
        atmo = Atmo(hp=41000.0, temperature=-50.5, temp_is_delta_isa=False)
        assert atmo.delta_isa == pytest.approx(6.0, abs=0.01)

    def test_troposphere_fahrenheit(self):
        atmo = Atmo(hp=31000.0, temperature=-62.36, temp_is_delta_isa=False, temp_unit="F")
        assert atmo.delta_isa == pytest.approx(-10.8, abs=0.01)

    def test_troposphere_km_fahrenheit(self):
        atmo = Atmo(hp=9.4488, temperature=-62.36, temp_is_delta_isa=False,
                    alt_unit="km", temp_unit="F")
        assert atmo.delta_isa == pytest.approx(-10.8, abs=0.01)

    def test_stratosphere_fahrenheit(self):
        atmo = Atmo(hp=41000.0, temperature=-58.9, temp_is_delta_isa=False, temp_unit="F")
        assert atmo.delta_isa == pytest.approx(10.8, abs=0.01)

    def test_stratosphere_nm_kelvin(self):
        atmo = Atmo(hp=6.74773, temperature=222.65, temp_is_delta_isa=False,
                    temp_unit="K", alt_unit="nm")
        assert atmo.delta_isa == pytest.approx(6.0, abs=0.01)


class TestTheta:
    # ISA (delta_isa=0)
    def test_troposphere_isa_celsius(self):
        assert Atmo(hp=31000.0, temperature=0).theta == pytest.approx(0.7869, abs=0.0001)

    def test_troposphere_isa_fahrenheit(self):
        assert Atmo(hp=31000.0, temperature=0, temp_unit="F").theta == pytest.approx(0.7869, abs=0.0001)

    def test_troposphere_isa_kelvin(self):
        assert Atmo(hp=31000.0, temperature=0, temp_unit="K").theta == pytest.approx(0.7869, abs=0.0001)

    def test_troposphere_isa_rankine(self):
        assert Atmo(hp=31000.0, temperature=0, temp_unit="R").theta == pytest.approx(0.7869, abs=0.0001)

    def test_stratosphere_isa_celsius(self):
        assert Atmo(hp=45000.0, temperature=0).theta == pytest.approx(0.7519, abs=0.0001)

    def test_stratosphere_isa_rankine(self):
        assert Atmo(hp=45000.0, temperature=0, temp_unit="R").theta == pytest.approx(0.7519, abs=0.0001)

    def test_troposphere_meters_isa_fahrenheit(self):
        assert Atmo(hp=9448.8, temperature=0, alt_unit="m", temp_unit="F").theta == pytest.approx(0.7869, abs=0.0001)

    # Non-standard (delta_isa != 0)
    def test_troposphere_disa20_celsius(self):
        assert Atmo(hp=31000.0, temperature=20.0).theta == pytest.approx(0.8563, abs=0.0001)

    def test_troposphere_meters_disa20_celsius(self):
        assert Atmo(hp=9448.8, temperature=20.0, alt_unit="m").theta == pytest.approx(0.8563, abs=0.0001)

    def test_troposphere_disa20_fahrenheit(self):
        assert Atmo(hp=31000.0, temperature=20.0, temp_unit="F").theta == pytest.approx(0.8254, abs=0.0001)

    def test_troposphere_disa20_kelvin(self):
        assert Atmo(hp=31000.0, temperature=20.0, temp_unit="K").theta == pytest.approx(0.8563, abs=0.0001)

    def test_troposphere_disa36_rankine(self):
        assert Atmo(hp=31000.0, temperature=36.0, temp_unit="R").theta == pytest.approx(0.8563, abs=0.0001)

    def test_stratosphere_disa20_celsius(self):
        assert Atmo(hp=45000.0, temperature=20.0, temp_unit="C").theta == pytest.approx(0.8213, abs=0.0001)

    def test_stratosphere_disa20_rankine(self):
        assert Atmo(hp=45000.0, temperature=20.0, temp_unit="R").theta == pytest.approx(0.7905, abs=0.0001)


class TestDelta:
    def test_troposphere_ft(self):
        assert Atmo(hp=15000.0, temperature=0).delta == pytest.approx(0.5643, abs=0.0001)

    def test_troposphere_sm(self):
        assert Atmo(hp=5.456, temperature=0, alt_unit="sm").delta == pytest.approx(0.3134, abs=0.0001)

    def test_stratosphere_m(self):
        assert Atmo(hp=11782.0, temperature=0, alt_unit="m").delta == pytest.approx(0.1974, abs=0.0001)

    def test_stratosphere_ft(self):
        assert Atmo(hp=43333.0, temperature=0).delta == pytest.approx(0.1577, abs=0.0001)


class TestSigma:
    def test_troposphere_ft_isa(self):
        assert Atmo(hp=15000.0, temperature=0).sigma == pytest.approx(0.6292, abs=0.0001)

    def test_troposphere_sm_isa(self):
        assert Atmo(hp=5.456, temperature=0, alt_unit="sm").sigma == pytest.approx(0.3909, abs=0.0001)

    def test_stratosphere_m_isa(self):
        assert Atmo(hp=11782.0, temperature=0, alt_unit="m").sigma == pytest.approx(0.2626, abs=0.0001)

    def test_stratosphere_ft_isa(self):
        assert Atmo(hp=43333.0, temperature=0).sigma == pytest.approx(0.2097, abs=0.0001)

    def test_troposphere_ft_disa14c(self):
        assert Atmo(hp=15000.0, temperature=14.0).sigma == pytest.approx(0.5969, abs=0.0001)

    def test_stratosphere_m_disa_neg32f(self):
        assert Atmo(hp=11782.0, temperature=-32.0, temp_unit="F", alt_unit="m").sigma == pytest.approx(0.2861, abs=0.0001)


class TestStratopauseError:
    def test_raises_above_stratopause(self):
        with pytest.raises(ValueError):
            Atmo(hp=65618.0, temperature=0)


class TestSpeedOfSound:
    def test_troposphere_knots(self):
        assert Atmo(hp=13456.0, temperature=28.6).speed_of_sound() == pytest.approx(663.7, abs=0.1)

    def test_stratosphere_knots(self):
        assert Atmo(hp=43456.0, temperature=-13.7).speed_of_sound() == pytest.approx(555.1, abs=0.1)

    def test_troposphere_m_f_knots(self):
        assert Atmo(hp=5555.0, temperature=13.7, alt_unit="m", temp_unit="F").speed_of_sound() == pytest.approx(627.9, abs=0.1)

    def test_stratosphere_m_f_knots(self):
        assert Atmo(hp=13777, temperature=-33.7, alt_unit="m", temp_unit="F").speed_of_sound() == pytest.approx(548.2, abs=0.1)

    def test_troposphere_fps(self):
        assert Atmo(hp=13456.0, temperature=28.6).speed_of_sound("fps") == pytest.approx(1120.2, abs=0.1)

    def test_troposphere_mph(self):
        assert Atmo(hp=13456.0, temperature=28.6).speed_of_sound("mph") == pytest.approx(763.8, abs=0.1)

    def test_troposphere_mps(self):
        assert Atmo(hp=13456.0, temperature=28.6).speed_of_sound("mps") == pytest.approx(341.4, abs=0.1)

    def test_troposphere_kmh(self):
        assert Atmo(hp=13456.0, temperature=28.6).speed_of_sound("kmh") == pytest.approx(1229.2, abs=0.1)


class TestAtmoClass:
    def test_troposphere_disa20_celsius(self):
        atmo = Atmo(hp=31000, temperature=20, temp_is_delta_isa=True)
        assert atmo.theta == pytest.approx(0.8563, abs=0.0001)
        assert atmo.delta == pytest.approx(0.2837, abs=0.0001)
        assert atmo.sigma == pytest.approx(0.3313, abs=0.0001)
        assert atmo.oat == pytest.approx(-26.42, abs=0.01)
        assert atmo.delta_isa == pytest.approx(20, abs=0.01)
        assert atmo.isa_temp == pytest.approx(-46.42, abs=0.01)
        assert atmo.speed_of_sound("kmh") == pytest.approx(1133.6, abs=0.1)

    def test_troposphere_oat_neg17_celsius(self):
        atmo = Atmo(hp=31000, temperature=-17, temp_is_delta_isa=False)
        assert atmo.theta == pytest.approx(0.8890, abs=0.0001)
        assert atmo.delta == pytest.approx(0.2837, abs=0.0001)
        assert atmo.sigma == pytest.approx(0.3191, abs=0.0001)
        assert atmo.oat == pytest.approx(-17, abs=0.01)
        assert atmo.delta_isa == pytest.approx(29.42, abs=0.01)
        assert atmo.isa_temp == pytest.approx(-46.42, abs=0.01)
        assert atmo.speed_of_sound("fps") == pytest.approx(1052.6, abs=0.1)

    def test_stratosphere_disa_neg17f(self):
        atmo = Atmo(hp=43333, temperature=-17, temp_is_delta_isa=True, temp_unit="F")
        assert atmo.theta == pytest.approx(0.7191, abs=0.0001)
        assert atmo.delta == pytest.approx(0.1577, abs=0.0001)
        assert atmo.sigma == pytest.approx(0.2193, abs=0.0001)
        assert atmo.oat == pytest.approx(-86.7, abs=0.1)
        assert atmo.delta_isa == pytest.approx(-17, abs=0.01)
        assert atmo.isa_temp == pytest.approx(-69.7, abs=0.1)
        assert atmo.speed_of_sound("mph") == pytest.approx(645.5, abs=0.1)


class TestVectorized:
    def test_delta_array(self):
        result = delta(np.array([0, 15000, 31000]))
        assert result[0] == pytest.approx(1.0, abs=0.0001)
        assert result[1] == pytest.approx(0.5643, abs=0.0001)
        assert result[2] == pytest.approx(0.2837, abs=0.0001)

    def test_theta_array(self):
        result = theta(np.array([0, 31000, 45000]))
        assert result[0] == pytest.approx(1.0, abs=0.0001)
        assert result[1] == pytest.approx(0.7869, abs=0.0001)
        assert result[2] == pytest.approx(0.7519, abs=0.0001)

    def test_isa_array(self):
        result = isa(np.array([0, 24555]))
        assert result[0] == pytest.approx(15.0, abs=0.01)
        assert result[1] == pytest.approx(-33.65, abs=0.02)
