"""CLI entry point for atmospeed — point calculations and CSV batch processing."""

import argparse
import csv
import sys

from .altitude import pressure_altitude
from .atmo import Atmo
from .speed import Speed


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="atmospeed",
        description="Standard atmosphere properties and airspeed conversions",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # --- convert subcommand ---
    p_conv = subparsers.add_parser(
        "convert",
        help="Single-point speed conversion or atmosphere lookup",
    )
    p_conv.add_argument("--hp", type=float, required=True, help="Pressure altitude")
    p_conv.add_argument("--temp", type=float, required=True,
                        help="Temperature (delta ISA by default, or OAT with --oat)")
    p_conv.add_argument("--oat", action="store_true",
                        help="Treat --temp as OAT instead of delta ISA")
    p_conv.add_argument("--alt-unit", default="ft",
                        choices=["ft", "m", "km", "sm", "nm"],
                        help="Altitude unit (default: ft)")
    p_conv.add_argument("--temp-unit", default="C",
                        choices=["C", "F", "K", "R"],
                        help="Temperature unit (default: C)")
    p_conv.add_argument("--speed", type=float, help="Speed value to convert")
    p_conv.add_argument("--from", dest="from_type",
                        choices=["cas", "eas", "tas", "mach"],
                        help="Input speed type")
    p_conv.add_argument("--to", dest="to_type",
                        choices=["cas", "eas", "tas", "mach"],
                        help="Output speed type")
    p_conv.add_argument("--speed-unit", default="kts",
                        choices=["kts", "fps", "mph", "mps", "kmh"],
                        help="Speed unit (default: kts)")
    p_conv.add_argument("--atmo", action="store_true",
                        help="Print atmosphere properties instead of speed conversion")

    # --- pressure-alt subcommand ---
    p_palt = subparsers.add_parser(
        "pressure-alt",
        help="Calculate pressure altitude from elevation and altimeter",
    )
    p_palt.add_argument("--elevation", type=float, required=True,
                        help="Airport elevation")
    p_palt.add_argument("--altimeter", type=float, required=True,
                        help="Altimeter setting (QNH)")
    p_palt.add_argument("--elev-unit", default="ft",
                        choices=["ft", "m", "km", "sm", "nm"],
                        help="Elevation unit (default: ft)")
    p_palt.add_argument("--altimeter-unit", default="inHg",
                        choices=["inHg", "hPa"],
                        help="Altimeter pressure unit (default: inHg)")

    # --- batch subcommand ---
    p_batch = subparsers.add_parser(
        "batch",
        help="Batch speed conversion from CSV",
    )
    p_batch.add_argument("input", help="Input CSV file path")
    p_batch.add_argument("output", help="Output CSV file path")
    p_batch.add_argument("--to", dest="to_type", required=True,
                         choices=["cas", "eas", "tas", "mach"],
                         help="Target speed type")

    args = parser.parse_args(argv)

    if args.command == "convert":
        _cmd_convert(args)
    elif args.command == "pressure-alt":
        _cmd_pressure_alt(args)
    elif args.command == "batch":
        _cmd_batch(args)


def _cmd_convert(args):
    atmo = Atmo(
        hp=args.hp,
        temperature=args.temp,
        temp_is_delta_isa=not args.oat,
        alt_unit=args.alt_unit,
        temp_unit=args.temp_unit,
    )

    if args.atmo:
        print(f"theta  = {atmo.theta:.4f}")
        print(f"delta  = {atmo.delta:.4f}")
        print(f"sigma  = {atmo.sigma:.4f}")
        print(f"OAT    = {atmo.oat:.2f} {atmo.temp_unit}")
        print(f"ISA    = {atmo.isa_temp:.2f} {atmo.temp_unit}")
        print(f"dISA   = {atmo.delta_isa:.2f} {atmo.temp_unit}")
        print(f"a      = {atmo.speed_of_sound():.1f} kts")
        return

    if args.speed is None or args.from_type is None:
        print("Error: --speed and --from are required for speed conversion.",
              file=sys.stderr)
        sys.exit(1)

    spd = Speed(args.speed, args.from_type, speed_unit=args.speed_unit)
    converters = {"cas": spd.to_cas, "eas": spd.to_eas,
                  "tas": spd.to_tas, "mach": spd.to_mach}

    targets = [args.to_type] if args.to_type else [
        t for t in converters if t != args.from_type
    ]

    for target in targets:
        result = converters[target](atmo)
        label = f" {target.upper()}" if len(targets) > 1 else ""
        if target == "mach":
            print(f"{result:.4f} Mach")
        else:
            print(f"{result:.1f} {args.speed_unit}{label}")


def _cmd_pressure_alt(args):
    hp = pressure_altitude(
        args.elevation, args.altimeter,
        elev_unit=args.elev_unit, altimeter_unit=args.altimeter_unit,
    )
    print(f"{hp:.1f} {args.elev_unit}")


def _cmd_batch(args):
    with open(args.input, newline="") as f_in:
        reader = csv.DictReader(f_in)
        fieldnames = list(reader.fieldnames or [])
        result_col = f"{args.to_type}_result"
        out_fields = fieldnames + [result_col]

        rows = []
        for row in reader:
            hp = float(row["hp"])
            temperature = float(row["temperature"])
            speed_value = float(row["speed_value"])
            speed_type = row["speed_type"].strip().lower()

            alt_unit = row.get("alt_unit", "ft").strip() or "ft"
            temp_unit = row.get("temp_unit", "C").strip() or "C"
            speed_unit = row.get("speed_unit", "kts").strip() or "kts"
            temp_is_disa = row.get("temp_is_delta_isa", "true").strip().lower()
            temp_is_disa = temp_is_disa in ("true", "1", "yes", "")

            atmo = Atmo(
                hp=hp, temperature=temperature,
                temp_is_delta_isa=temp_is_disa,
                alt_unit=alt_unit, temp_unit=temp_unit,
            )
            spd = Speed(speed_value, speed_type, speed_unit=speed_unit)
            converters = {"cas": spd.to_cas, "eas": spd.to_eas,
                          "tas": spd.to_tas, "mach": spd.to_mach}
            result = converters[args.to_type](atmo)

            row[result_col] = f"{result:.4f}"
            rows.append(row)

    with open(args.output, "w", newline="") as f_out:
        writer = csv.DictWriter(f_out, fieldnames=out_fields)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Processed {len(rows)} rows -> {args.output}")


if __name__ == "__main__":
    main()
