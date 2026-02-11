"""Internal speed conversion functions. All operate in knots (KCAS/KEAS/KTAS),
feet (hp), and Celsius (delta ISA). Accept scalars or numpy arrays."""

import numpy as np

from .constants import A0_KTS, SPEED_CALC_CONST
from .ratio import delta as calc_delta
from .ratio import sigma as calc_sigma
from .ratio import theta as calc_theta


# --- From KCAS ---

def _common_kcas_term(kcas, hp_ft):
    d = calc_delta(hp_ft, alt_unit="ft")
    term1 = 1.0 + 0.2 * np.power(kcas / A0_KTS, 2)
    term2 = np.power(term1, 3.5) - 1.0
    term3 = (1.0 / d) * term2 + 1.0
    return np.power(term3, 1.0 / 3.5) - 1.0


def kcas_to_keas(kcas, hp_ft):
    d = calc_delta(hp_ft, alt_unit="ft")
    return SPEED_CALC_CONST * np.sqrt(d * _common_kcas_term(kcas, hp_ft))


def kcas_to_mach(kcas, hp_ft):
    return np.sqrt(5.0 * _common_kcas_term(kcas, hp_ft))


def kcas_to_ktas(kcas, hp_ft, disa_c):
    t = calc_theta(hp_ft, delta_isa=disa_c, alt_unit="ft", temp_unit="C")
    return SPEED_CALC_CONST * np.sqrt(t * _common_kcas_term(kcas, hp_ft))


# --- From KEAS ---

def keas_to_kcas(keas, hp_ft):
    d = calc_delta(hp_ft, alt_unit="ft")
    term1 = 1.0 + (1.0 / d) * np.power(keas / SPEED_CALC_CONST, 2)
    term2 = np.power(term1, 3.5) - 1.0
    term3 = d * term2 + 1.0
    return SPEED_CALC_CONST * np.sqrt(np.power(term3, 1.0 / 3.5) - 1.0)


def keas_to_mach(keas, hp_ft):
    d = calc_delta(hp_ft, alt_unit="ft")
    return keas / A0_KTS * np.sqrt(1.0 / d)


def keas_to_ktas(keas, hp_ft, disa_c):
    s = calc_sigma(hp_ft, delta_isa=disa_c, alt_unit="ft", temp_unit="C")
    return keas / np.sqrt(s)


# --- From KTAS ---

def ktas_to_kcas(ktas, hp_ft, disa_c):
    t = calc_theta(hp_ft, delta_isa=disa_c, alt_unit="ft", temp_unit="C")
    term1 = 1.0 + (1.0 / t) * np.power(ktas / SPEED_CALC_CONST, 2)
    term2 = np.power(term1, 3.5) - 1.0
    d = calc_delta(hp_ft, alt_unit="ft")
    term3 = d * term2 + 1.0
    return SPEED_CALC_CONST * np.sqrt(np.power(term3, 1.0 / 3.5) - 1.0)


def ktas_to_keas(ktas, hp_ft, disa_c):
    s = calc_sigma(hp_ft, delta_isa=disa_c, alt_unit="ft", temp_unit="C")
    return ktas * np.sqrt(s)


def ktas_to_mach(ktas, hp_ft, disa_c):
    t = calc_theta(hp_ft, delta_isa=disa_c, alt_unit="ft", temp_unit="C")
    return ktas / (A0_KTS * np.sqrt(t))


# --- From Mach ---

def mach_to_kcas(mach, hp_ft):
    term1 = np.power(0.2 * mach * mach + 1.0, 3.5) - 1.0
    d = calc_delta(hp_ft, alt_unit="ft")
    term2 = d * term1 + 1.0
    term3 = np.power(term2, 1.0 / 3.5) - 1.0
    return SPEED_CALC_CONST * np.sqrt(term3)


def mach_to_keas(mach, hp_ft):
    d = calc_delta(hp_ft, alt_unit="ft")
    return A0_KTS * mach * np.sqrt(d)


def mach_to_ktas(mach, hp_ft, disa_c):
    t = calc_theta(hp_ft, delta_isa=disa_c, alt_unit="ft", temp_unit="C")
    return A0_KTS * mach * np.sqrt(t)
