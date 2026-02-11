# AtmoSpeed User Guide

AtmoSpeed is a Python library and command-line tool for standard atmosphere property calculations and airspeed conversions based on the **1976 US Standard Atmosphere** (NASA-TM-X-74335). It is valid through 20 km (65,617 ft) altitude.

**What it does:**

- Calculate atmosphere properties at any altitude: temperature ratio (theta), pressure ratio (delta), density ratio (sigma), ISA temperature, OAT, speed of sound
- Convert between airspeed types: CAS, EAS, TAS, and Mach
- Calculate pressure altitude from airport elevation and altimeter setting (QNH)
- Process bulk conversions from CSV files

---

## Table of Contents

1. [Installation](#installation)
2. [Command-Line Usage](#command-line-usage)
   - [Speed Conversions](#speed-conversions)
   - [Atmosphere Properties](#atmosphere-properties)
   - [Pressure Altitude](#pressure-altitude)
   - [CSV Batch Processing](#csv-batch-processing)
3. [Python API Usage](#python-api-usage)
4. [Unit Reference](#unit-reference)
5. [Concepts](#concepts)

---

## Installation

### Step 1: Install uv (Python package manager)

AtmoSpeed uses **uv**, a fast Python project manager. Install it first if you don't have it.

**macOS (Terminal):**

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows (PowerShell):**

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

After installing, **close and reopen your terminal** so the `uv` command is available.

Verify it worked:

```bash
uv --version
```

You should see something like `uv 0.7.x`. You do **not** need to install Python separately — uv will handle that automatically.

### Step 2: Clone the repository

```bash
git clone https://github.com/aeroperf/py-atmospeed.git
cd py-atmospeed
```

### Step 3: Install dependencies

```bash
uv sync
```

This command does three things automatically:
1. Downloads and installs the correct Python version if you don't have it
2. Creates an isolated virtual environment in `.venv/`
3. Installs all dependencies (numpy, pytest)

That's it. You're ready to go.

### Verify the install

```bash
uv run atmospeed --help
```

You should see:

```
usage: atmospeed [-h] {convert,pressure-alt,batch} ...

Standard atmosphere properties and airspeed conversions
```

> **Note:** Every command in this guide uses `uv run atmospeed ...` which ensures the correct Python environment is used. You do not need to activate a virtual environment manually.

---

## Command-Line Usage

All commands follow this pattern:

```
uv run atmospeed <subcommand> [options]
```

There are three subcommands: `convert`, `pressure-alt`, and `batch`.

---

### Speed Conversions

Convert a speed from one type to another at a given atmospheric condition.

**Required arguments:**

| Argument | Description |
|----------|-------------|
| `--hp` | Pressure altitude |
| `--temp` | Temperature (delta ISA by default) |
| `--speed` | Speed value to convert |
| `--from` | Input speed type: `cas`, `eas`, `tas`, or `mach` |
| `--to` | Output speed type: `cas`, `eas`, `tas`, or `mach` |

**Example: CAS to TAS**

At 18,455 ft pressure altitude, ISA+13C, convert 255.6 KCAS to KTAS:

```bash
uv run atmospeed convert --hp 18455 --temp 13 --speed 255.6 --from cas --to tas
```

Output:

```
343.7 kts
```

**Example: CAS to Mach**

```bash
uv run atmospeed convert --hp 31000 --temp 0 --speed 287.3 --from cas --to mach
```

Output:

```
0.7130 Mach
```

**Example: Mach to TAS**

```bash
uv run atmospeed convert --hp 41000 --temp 0 --speed 0.85 --from mach --to tas
```

**Example: With non-default units**

Altitude in meters, temperature in Fahrenheit, speed in km/h:

```bash
uv run atmospeed convert --hp 9449 --alt-unit m --temp 20 --temp-unit F --speed 473 --speed-unit kmh --from cas --to tas
```

**Example: Using OAT instead of delta ISA**

By default, `--temp` is interpreted as a delta ISA (deviation from standard). Add `--oat` to treat it as Outside Air Temperature instead:

```bash
uv run atmospeed convert --hp 31000 --temp -17 --oat --speed 250 --from cas --to tas
```

#### Optional arguments for speed conversions

| Argument | Default | Options | Description |
|----------|---------|---------|-------------|
| `--alt-unit` | `ft` | `ft`, `m`, `km`, `sm`, `nm` | Altitude unit |
| `--temp-unit` | `C` | `C`, `F`, `K`, `R` | Temperature unit |
| `--speed-unit` | `kts` | `kts`, `fps`, `mph`, `mps`, `kmh` | Speed unit (input and output) |
| `--oat` | off | — | Treat `--temp` as OAT instead of delta ISA |

---

### Atmosphere Properties

Get all standard atmosphere properties at a given altitude and temperature condition. Use `--atmo` instead of speed arguments.

```bash
uv run atmospeed convert --hp 31000 --temp 20 --atmo
```

Output:

```
theta  = 0.8563
delta  = 0.2837
sigma  = 0.3313
OAT    = -26.42 C
ISA    = -46.42 C
dISA   = 20.00 C
a      = 612.1 kts
```

| Property | Description |
|----------|-------------|
| theta | Temperature ratio (T / T_SL_std) |
| delta | Pressure ratio (P / P_SL_std) |
| sigma | Density ratio (rho / rho_SL_std) |
| OAT | Outside Air Temperature |
| ISA | Standard atmosphere temperature at this altitude |
| dISA | Temperature deviation from standard |
| a | Speed of sound |

**Example: ISA conditions at FL350**

```bash
uv run atmospeed convert --hp 35000 --temp 0 --atmo
```

**Example: Using OAT input in Fahrenheit at altitude in meters**

```bash
uv run atmospeed convert --hp 10000 --alt-unit m --temp -58 --temp-unit F --oat --atmo
```

---

### Pressure Altitude

Calculate pressure altitude from airport field elevation and altimeter setting (QNH).

```bash
uv run atmospeed pressure-alt --elevation 1000 --altimeter 29.40
```

Output:

```
1484.0 ft
```

**Example: Metric units with hPa**

```bash
uv run atmospeed pressure-alt --elevation 1708 --elev-unit m --altimeter 1032 --altimeter-unit hPa
```

| Argument | Default | Options | Description |
|----------|---------|---------|-------------|
| `--elevation` | *(required)* | — | Airport field elevation |
| `--altimeter` | *(required)* | — | Altimeter setting (QNH) |
| `--elev-unit` | `ft` | `ft`, `m`, `km`, `sm`, `nm` | Elevation unit (also used for output) |
| `--altimeter-unit` | `inHg` | `inHg`, `hPa` | Pressure unit |

---

### CSV Batch Processing

Process a CSV file of speed conditions and convert them all at once. This is the most efficient way to convert large datasets.

```
uv run atmospeed batch <input.csv> <output.csv> --to <speed_type>
```

#### Input CSV format

The CSV must have a header row. These columns are **required**:

| Column | Description | Example |
|--------|-------------|---------|
| `hp` | Pressure altitude | `31000` |
| `temperature` | Temperature value (delta ISA by default) | `20` |
| `speed_value` | Speed to convert | `255.6` |
| `speed_type` | Input speed type | `cas`, `eas`, `tas`, or `mach` |

These columns are **optional** (defaults are used when omitted):

| Column | Default | Description |
|--------|---------|-------------|
| `alt_unit` | `ft` | Altitude unit |
| `temp_unit` | `C` | Temperature unit |
| `speed_unit` | `kts` | Speed unit |
| `temp_is_delta_isa` | `true` | Set to `false` if temperature is OAT |

#### Example: Basic CSV

Create a file called `input.csv`:

```csv
hp,temperature,speed_value,speed_type
31000,20,255.6,cas
18455,13,287.3,cas
41000,0,0.85,mach
35000,-10,300,eas
```

Run the batch conversion to TAS:

```bash
uv run atmospeed batch input.csv output.csv --to tas
```

Output file `output.csv`:

```csv
hp,temperature,speed_value,speed_type,tas_result
31000,20,255.6,cas,426.1220
18455,13,287.3,cas,384.6465
41000,0,0.85,mach,487.5338
35000,-10,300,eas,526.4656
```

The tool appends a result column named `<speed_type>_result` (e.g., `tas_result`, `mach_result`, `cas_result`).

#### Example: Convert to Mach

```bash
uv run atmospeed batch input.csv mach_output.csv --to mach
```

#### Example: CSV with mixed units and OAT

```csv
hp,temperature,speed_value,speed_type,alt_unit,temp_unit,speed_unit,temp_is_delta_isa
31000,20,255.6,cas,ft,C,kts,true
10000,-15,500,cas,m,F,kmh,false
41000,0,0.85,mach,ft,C,kts,true
```

```bash
uv run atmospeed batch mixed_units.csv results.csv --to tas
```

#### Tips for CSV files

- You can create and edit CSV files in Excel, Google Sheets, or any text editor
- When saving from Excel, use **Save As > CSV (Comma delimited)**
- The column order does not matter as long as the header names match
- Empty optional columns use their default values
- Mach inputs ignore the `speed_unit` column (Mach is unitless)

---

## Python API Usage

For integration into your own Python scripts or Jupyter notebooks, you can use AtmoSpeed as a library.

```python
from atmospeed import Atmo, Speed
```

### Atmospheric properties

```python
from atmospeed import Atmo

# Define an atmospheric point: 31,000 ft, ISA+20C
atmo = Atmo(hp=31000, temperature=20)

atmo.theta       # 0.8563  — temperature ratio
atmo.delta       # 0.2837  — pressure ratio
atmo.sigma       # 0.3313  — density ratio
atmo.oat         # -26.42  — OAT in C
atmo.isa_temp    # -46.42  — ISA temperature in C
atmo.delta_isa   # 20.0    — delta ISA
atmo.speed_of_sound()       # 612.1 kts
atmo.speed_of_sound("kmh")  # 1133.6 km/h
```

**With different units:**

```python
# Altitude in meters, temperature in Fahrenheit, using OAT input
atmo = Atmo(hp=10000, temperature=-22, temp_is_delta_isa=False,
            alt_unit="m", temp_unit="F")
```

### Speed conversions

```python
from atmospeed import Atmo, Speed

atmo = Atmo(hp=18455, temperature=13)
spd = Speed(255.6, "cas")

spd.to_tas(atmo)   # 343.7 KTAS
spd.to_eas(atmo)   # 251.1 KEAS
spd.to_mach(atmo)  # 0.5422 Mach
```

**With different speed units:**

```python
# EAS in m/s
spd = Speed(150, "eas", speed_unit="mps")
spd.to_cas(atmo)   # result in m/s (matches input unit)
spd.to_mach(atmo)  # Mach (always unitless)
```

**Speed unit conversion:**

```python
from atmospeed import speed_convert

speed_convert(250, "kts", "kmh")  # 463.0 km/h
speed_convert(150, "mph", "mps")  # 67.04 m/s
```

### Pressure altitude

```python
from atmospeed import pressure_altitude

pressure_altitude(1000, 29.40)  # 1484.0 ft
pressure_altitude(1708, 1032, elev_unit="m", altimeter_unit="hPa")
```

### Standalone atmosphere functions

You can call atmosphere functions directly without creating an `Atmo` object:

```python
from atmospeed import theta, delta, sigma, isa, oat

isa(31000)                  # -46.42 C (ISA temperature)
oat(31000, 20)              # -26.42 C (OAT with dISA=+20)
theta(31000)                # 0.7869  (ISA, no deviation)
theta(31000, delta_isa=20)  # 0.8563  (with +20C deviation)
delta(31000)                # 0.2837
sigma(31000)                # 0.3604  (ISA)
sigma(31000, delta_isa=20)  # 0.3313  (non-standard)
```

### Vectorized operations with NumPy

All standalone functions accept NumPy arrays for fast batch calculations:

```python
import numpy as np
from atmospeed import delta, theta, isa

altitudes = np.array([0, 10000, 20000, 30000, 40000])

delta(altitudes)   # [1.0, 0.6877, 0.4595, 0.2970, 0.1851]
theta(altitudes)   # [1.0, 0.9312, 0.8625, 0.7937, 0.7519]
isa(altitudes)     # [15.0, -4.81, -24.62, -44.44, -56.50]
```

This is useful when working with pandas DataFrames:

```python
import pandas as pd
from atmospeed import delta

df = pd.DataFrame({"altitude_ft": [0, 10000, 20000, 30000]})
df["pressure_ratio"] = delta(df["altitude_ft"].values)
```

---

## Unit Reference

### Altitude units (`--alt-unit`)

| Value | Unit |
|-------|------|
| `ft` | Feet (default) |
| `m` | Meters |
| `km` | Kilometers |
| `sm` | Statute miles |
| `nm` | Nautical miles |

### Temperature units (`--temp-unit`)

| Value | Unit |
|-------|------|
| `C` | Celsius (default) |
| `F` | Fahrenheit |
| `K` | Kelvin |
| `R` | Rankine |

### Speed units (`--speed-unit`)

| Value | Unit |
|-------|------|
| `kts` | Knots (default) |
| `fps` | Feet per second |
| `mph` | Statute miles per hour |
| `mps` | Meters per second |
| `kmh` | Kilometers per hour |

### Speed types (`--from` / `--to`)

| Value | Description |
|-------|-------------|
| `cas` | Calibrated Airspeed |
| `eas` | Equivalent Airspeed |
| `tas` | True Airspeed |
| `mach` | Mach number |

### Pressure units (`--altimeter-unit`)

| Value | Unit |
|-------|------|
| `inHg` | Inches of mercury (default) |
| `hPa` | Hectopascals / millibars |

---

## Concepts

### Temperature input: Delta ISA vs. OAT

By default, the `--temp` argument (and the `temperature` CSV column) is a **delta ISA** value — the deviation from the International Standard Atmosphere temperature at that altitude.

| Delta ISA | Meaning |
|-----------|---------|
| `0` | Standard day (ISA) |
| `+20` | 20 degrees warmer than standard |
| `-10` | 10 degrees colder than standard |

If you have an OAT (Outside Air Temperature) reading instead, use the `--oat` flag on the command line, or set `temp_is_delta_isa` to `false` in your CSV.

### Valid altitude range

Calculations are valid from sea level through **20 km (65,617 ft)** — the stratopause. Altitudes above this limit will produce an error.

### Atmosphere model

This library uses the **1976 US Standard Atmosphere** (NASA-TM-X-74335), which is identical to the ICAO Standard Atmosphere through 51 km. The two atmospheric regions modeled are:

- **Troposphere** (0 to 36,089 ft / 11,000 m): Temperature decreases linearly at 0.0019812 C/ft
- **Stratosphere** (36,089 to 65,617 ft / 11,000 to 20,000 m): Temperature is constant at -56.5 C

---

## Running Tests

To run the test suite (105 tests):

```bash
uv run pytest
```

For verbose output:

```bash
uv run pytest -v
```
