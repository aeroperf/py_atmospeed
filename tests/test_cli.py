"""Smoke tests for the CLI."""

import csv
import tempfile
import os
import pytest
from atmospeed.cli import main


class TestCLIConvert:
    def test_speed_conversion(self, capsys):
        main(["convert", "--hp", "18455", "--temp", "13",
              "--speed", "255.6", "--from", "cas", "--to", "tas"])
        out = capsys.readouterr().out
        # Should contain a number close to 343.7
        value = float(out.split()[0])
        assert value == pytest.approx(343.7, abs=0.2)

    def test_atmo_properties(self, capsys):
        main(["convert", "--hp", "31000", "--temp", "20", "--atmo"])
        out = capsys.readouterr().out
        assert "theta" in out
        assert "delta" in out
        assert "sigma" in out

    def test_mach_output(self, capsys):
        main(["convert", "--hp", "31000", "--temp", "0",
              "--speed", "287.3", "--from", "cas", "--to", "mach"])
        out = capsys.readouterr().out
        assert "Mach" in out

    def test_convert_all(self, capsys):
        main(["convert", "--hp", "18455", "--temp", "13",
              "--speed", "255.6", "--from", "cas"])
        out = capsys.readouterr().out
        lines = out.strip().splitlines()
        assert len(lines) == 3
        assert "EAS" in lines[0]
        assert "TAS" in lines[1]
        assert "Mach" in lines[2]


class TestCLIPressureAlt:
    def test_basic(self, capsys):
        main(["pressure-alt", "--elevation", "1000", "--altimeter", "29.40"])
        out = capsys.readouterr().out
        value = float(out.split()[0])
        assert value == pytest.approx(1484.0, abs=1)


class TestCLIBatch:
    def test_batch_csv(self, capsys):
        with tempfile.TemporaryDirectory() as tmpdir:
            in_path = os.path.join(tmpdir, "input.csv")
            out_path = os.path.join(tmpdir, "output.csv")

            with open(in_path, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["hp", "temperature", "speed_value", "speed_type"])
                writer.writerow([31000, 20, 255.6, "cas"])
                writer.writerow([18455, 13, 287.3, "cas"])

            main(["batch", in_path, out_path, "--to", "tas"])

            with open(out_path, newline="") as f:
                reader = list(csv.DictReader(f))

            assert len(reader) == 2
            assert "tas_result" in reader[0]
            assert float(reader[0]["tas_result"]) == pytest.approx(426.1, abs=1)
