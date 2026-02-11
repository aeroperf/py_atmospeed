"""Atmospheric constants based on the 1976 US Standard Atmosphere (NASA-TM-X-74335)."""

# Altitude limits
HEIGHT_TROPOPAUSE_FT = 11_000 / 0.3048  # 11000 m by definition, ~36089.24 ft
HEIGHT_STRATOPAUSE_FT = 20_000 / 0.3048  # 20000 m by definition, ~65617 ft

# Troposphere lapse rates
LAPSE_RATE_C_PER_FT = 0.0019812  # °C/ft
LAPSE_RATE_F_PER_FT = 0.00356616  # °F/ft

# Sea level standard day temperatures
TEMP_SL_STD_C = 15.0  # °C
TEMP_SL_STD_F = 59.0  # °F
TEMP_SL_STD_K = 288.15  # K
TEMP_SL_STD_R = 518.67  # R

# Stratosphere temperatures
TEMP_STRATOSPHERE_C = -56.5  # °C
TEMP_STRATOSPHERE_F = -69.7  # °F

# Temperature offsets
ZERO_C_IN_K = 273.15  # K
ZERO_C_IN_R = 459.67  # R

# Pressure ratio constants
TROPOPAUSE_CONST_US = 20805.7  # R * Ttrop / g0
TROPOSPHERE_DELTA_EXP = 5.25588
DELTA_AT_TROPOPAUSE = 0.22336

# Sea level standard pressures
PRESSURE_SL_STD_INHG = 29.92  # inHg
PRESSURE_SL_STD_HPA = 1013.25  # hPa

# Pressure altitude calculation
PRESSURE_CALC_CONST = 145442.15  # ft
PRESSURE_CALC_EXP = 0.190263

# Speed of sound at sea level standard day
A0_KTS = 661.4786  # knots
A0_FPS = 1116.45  # ft/s
A0_MPS = 340.29  # m/s
A0_KMH = 3.6 * A0_MPS  # km/h
A0_MPH = 761.2  # mph

# Speed calculation constant: (2*gamma*P0/((gamma-1)*rho0))^0.5 / 1.6878
SPEED_CALC_CONST = 1479.1
