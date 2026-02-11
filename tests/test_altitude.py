"""Tests for pressure altitude calculation.
Ported from Dart atmospeed_test.dart with identical expected values."""

import pytest
from atmospeed import pressure_altitude


class TestPressureAltitude:
    def test_ft_inhg(self):
        assert pressure_altitude(1000.0, 29.40) == pytest.approx(1484.0, abs=0.5)

    def test_ft_hpa(self):
        assert pressure_altitude(5555.0, 981.0, altimeter_unit="hPa") == pytest.approx(6447.0, abs=0.5)

    def test_m_inhg(self):
        assert pressure_altitude(1708.0, 30.47, elev_unit="m") == pytest.approx(1554.0, abs=0.5)

    def test_m_hpa(self):
        assert pressure_altitude(3795.0, 1044.0, elev_unit="m", altimeter_unit="hPa") == pytest.approx(3542.0, abs=0.5)

    def test_km_hpa(self):
        assert pressure_altitude(2.345, 982, elev_unit="km", altimeter_unit="hPa") == pytest.approx(2.608, abs=0.5)

    def test_nm_hpa(self):
        assert pressure_altitude(2.049, 1044.0, elev_unit="nm", altimeter_unit="hPa") == pytest.approx(1.913, abs=0.001)

    def test_sm_hpa(self):
        assert pressure_altitude(2.358, 1044.0, elev_unit="sm", altimeter_unit="hPa") == pytest.approx(2.201, abs=0.001)
