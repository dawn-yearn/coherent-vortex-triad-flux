#!/usr/bin/env python3
"""Exact arithmetic checks for the Card B certificate (Python stdlib only).

This script checks finite Fourier/Wick algebra and rational inequalities.
The analytic N-uniform semigroup and Poisson estimates are proved in the
companion note; running this script does NOT formally verify those proofs.

Usage: python3 card_b_exact_certificate.py --output card_b_exact_certificate.json
"""

from __future__ import annotations

import argparse
import json
from fractions import Fraction as F
from itertools import product
from pathlib import Path


def neg(k):
    return (-k[0], -k[1])


def add(k, l):
    return (k[0] + l[0], k[1] + l[1])


def norm2(k):
    return k[0] ** 2 + k[1] ** 2


def cross(k, l):
    return k[0] * l[1] - k[1] * l[0]


P = (3, 0)
Q = (-2, 1)
FORCED = {P, neg(P), Q, neg(Q)}


def cov(k, l):
    # E[z_k z_l] = delta_{k,-l} c_k, c_k=1 on forced pairs.
    return F(int(k in FORCED and l == neg(k)))


def wick4(a, b, c, d):
    return cov(a, b) * cov(c, d) + cov(a, c) * cov(b, d) + cov(a, d) * cov(b, c)


def beta(k, l):
    return F(cross(k, l), 2) * (F(1, norm2(k)) - F(1, norm2(l)))


def full_galerkin_flux_response(cutoff):
    """Compute the entire low-mode cubic response at A=0 by stationarity.

    This implementation uses UNSYMMETRIZED ordered coefficients of J,
    rather than the closed-form beta formula. No isolated-triad deletion.
    """
    modes = [
        k for k in product(range(-cutoff, cutoff + 1), repeat=2)
        if 1 < norm2(k) <= cutoff * cutoff
    ]
    mode_set = set(modes)
    pairs = {
        k: [(a, (k[0] - a[0], k[1] - a[1])) for a in modes
            if (k[0] - a[0], k[1] - a[1]) in mode_set]
        for k in modes
    }

    def triple_response(triad):
        # 0 = -(lambda_a+lambda_b+lambda_c) E[z_a z_b z_c]
        #     + epsilon E[ n_a z_b z_c + z_a n_b z_c + z_a z_b n_c ].
        # Noise pair terms leave a centered first moment, hence vanish.
        source = F(0)
        for i, target in enumerate(triad):
            rest = triad[:i] + triad[i + 1:]
            for a, b in pairs[target]:
                # n=-J(Gz,z); J_k=sum_(a+b=k) (a x b)/|a|^2 z_a z_b.
                source -= F(cross(a, b), norm2(a)) * wick4(a, b, *rest)
        return source / sum(norm2(k) for k in triad)

    result = F(0)
    nonzero = []
    for k in modes:
        if norm2(k) > 4:
            continue
        for a, b in pairs[k]:
            coefficient = F(cross(a, b), norm2(k) * norm2(a))
            if not coefficient:
                continue
            moment = triple_response((neg(k), a, b))
            contribution = coefficient * moment
            if contribution:
                result += contribution
                nonzero.append({
                    "output": k, "ordered_inputs": [a, b],
                    "T_coefficient": str(coefficient),
                    "third_moment_response": str(moment),
                    "contribution": str(contribution),
                })
    return {"N": cutoff, "retained_complex_modes": len(modes),
            "F": str(result), "nonzero_ordered_contributions": nonzero}, result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    k = add(P, Q)
    b = beta(P, Q)
    rate = norm2(k) + norm2(P) + norm2(Q)
    mprime = -2 * b / rate
    closed_form = 4 * b * mprime / norm2(k)
    assert b == F(-2, 15)
    assert mprime == F(1, 60)
    assert closed_form == F(-1, 225)
    assert norm2(k) <= 4 < min(norm2(P), norm2(Q))
    assert norm2(add(P, neg(Q))) == 26

    enumerations = []
    for cutoff in (3, 4):
        record, value = full_galerkin_flux_response(cutoff)
        assert value == closed_form
        enumerations.append(record)

    a_max = F(1, 100_000_000)
    disk_radius = F(1, 32)
    holomorphic_bound = F(300_000_000)
    ratio2 = (a_max / disk_radius) ** 2
    error = holomorphic_bound * ratio2 / (1 - ratio2)
    tolerance = F(1, 30_000)
    assert ratio2 < 1
    assert error < tolerance
    lower, upper = closed_form - tolerance, closed_form + tolerance
    assert (lower, upper) == (F(-403, 90000), F(-397, 90000))
    assert upper < 0

    # Arithmetic constants whose ANALYTIC premises are proved in the note.
    trace_h1_q = 2 * (9 ** 2 + 5 ** 2)
    gaussian_fourth_upper = 3 * (4 * trace_h1_q) ** 2
    assert trace_h1_q == 212
    assert gaussian_fourth_upper < 50 ** 4
    assert 6 * 2 * 4 * 50 ** 4 == holomorphic_bound
    assert 16 ** 3 * 3 * 4 * 5 == 245760
    assert F(1) / (1 - F(12, 32)) < 2
    assert F(1) / (1 - F(6, 32)) < 2

    output = {
        "status": "all_exact_arithmetic_checks_passed",
        "scope": "Fourier/Wick algebra and rational comparisons; not a formal SPDE proof",
        "arithmetic": "fractions.Fraction; no floating-point decisions",
        "parameters": {"nu": 1, "alpha": 0, "K": 2,
                       "forced_modes": sorted(FORCED),
                       "Q_p": 9, "Q_q": 5, "c_p": 1, "c_q": 1},
        "closed_form": {"output_k": k, "beta": str(b),
                        "sum_decay_rates": rate, "M_prime": str(mprime),
                        "F_0": str(closed_form), "valid_for_all_N_ge": 3},
        "full_finite_galerkin_independent_enumerations": enumerations,
        "small_A_certificate": {
            "A_max": str(a_max), "holomorphic_disk_radius": str(disk_radius),
            "sup_F_on_disk_analytic_upper_bound": str(holomorphic_bound),
            "cauchy_even_tail_exact": str(error), "outward_tolerance": str(tolerance),
            "F_lower": str(lower), "F_upper": str(upper),
            "validity": "every N>=3 and the proven N-to-infinity limit; 0<A<=A_max",
            "not_certified": "sign or background-induced change for A/nu of order one",
        },
        "analytic_dependencies_not_machine_checked": [
            "B-energy moments and H^{-3/2}-to-L2 semigroup smoothing",
            "bounded multilinear polynomial Poisson estimates and invariant identity",
            "Galerkin convergence and infinite-dimensional leading coefficient",
            "holomorphy, translation evenness, and full-disk 300000000 bound",
            "all-N sparsity argument excluding further leading low-mode triads",
        ],
    }
    encoded = json.dumps(output, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        args.output.write_text(encoded, encoding="utf-8")
        print(json.dumps({"status": output["status"], "output": str(args.output),
                          "F_0": str(closed_form), "interval": [str(lower), str(upper)],
                          "exact_tail_bound": str(error)}, ensure_ascii=False))
    else:
        print(encoded, end="")


if __name__ == "__main__":
    main()
