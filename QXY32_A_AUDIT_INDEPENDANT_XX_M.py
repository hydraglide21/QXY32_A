#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
QXY32_A — CONTRE-EXPERTISE INDEPENDANTE XX-M
============================================
Reconstruction exacte depuis les définitions de M dans Q(sqrt(5)).

Ce script ne lit pas les anciens scripts XIX/XX et ne reprend pas leurs
comptages comme données d'entrée. Il reconstruit les polynômes, leurs bases
de Bernstein, les signes exacts, les identités de permutation et les lieux
d'annulation du déterminant.

Dépendance : sympy
Aucune arithmétique flottante n'est utilisée pour les certificats de signe.
"""

from __future__ import annotations

import itertools
import json
import math
from collections import Counter
from fractions import Fraction

import sympy as sp

R = sp.sqrt(5)
PHI = (1 + R) / 2
KC = (1 + 2 * R) / 4

s, t, W, T, q = sp.symbols("s t W T q", real=True)
x, y, z, k = sp.symbols("x y z k", real=True)


def u(a):
    return a * (2 - a)


def F(a, b, c, kval):
    # F est symétrique dans ses deux derniers arguments.
    B = (PHI + kval) / 2
    return sp.expand(a * (R - B * (2 - a)) + (PHI - kval * a) * (b + c))


def sign_qsqrt5(expr):
    """Signe exact de a+b*sqrt(5), a,b rationnels."""
    p = sp.Poly(sp.expand(expr), R, domain=sp.QQ)
    a = sp.Rational(p.coeff_monomial(1))
    b = sp.Rational(p.coeff_monomial(R))
    if a == 0 and b == 0:
        return 0
    if b == 0:
        return 1 if a > 0 else -1
    if a == 0:
        return 1 if b > 0 else -1
    if a > 0 and b > 0:
        return 1
    if a < 0 and b < 0:
        return -1
    d = a * a - 5 * b * b
    if a > 0 and b < 0:
        return 1 if d > 0 else (-1 if d < 0 else 0)
    if a < 0 and b > 0:
        return 1 if d < 0 else (-1 if d > 0 else 0)
    raise AssertionError("Cas de signe non traité")


def bernstein_coefficients(expr, variables, degrees):
    """Coefficients Bernstein tensoriels exacts sur [0,1]^n."""
    P = sp.Poly(sp.expand(expr), *variables, extension=R)
    power = P.as_dict()
    out = {}
    for idx in itertools.product(*[range(n + 1) for n in degrees]):
        value = sp.S.Zero
        for exponent, coefficient in power.items():
            if all(exponent[j] <= idx[j] for j in range(len(variables))):
                factor = sp.prod(
                    sp.Rational(
                        math.comb(idx[j], exponent[j]),
                        math.comb(degrees[j], exponent[j])
                    )
                    for j in range(len(variables))
                )
                value += coefficient * factor
        out[idx] = sp.expand(value)
    return out


def bernstein_reconstruct(coefficients, variables, degrees):
    expr = sp.S.Zero
    for idx, value in coefficients.items():
        basis = sp.prod(
            sp.binomial(n, i) * v**i * (1-v)**(n-i)
            for v, n, i in zip(variables, degrees, idx)
        )
        expr += value * basis
    return sp.expand(expr)


def signs_report(coefficients):
    c = Counter(sign_qsqrt5(v) for v in coefficients.values())
    return {
        "total": len(coefficients),
        "positive": c[1],
        "zero": c[0],
        "negative": c[-1],
    }


def check_reconstruction(expr, coefficients, variables, degrees):
    return sp.expand(bernstein_reconstruct(
        coefficients, variables, degrees
    ) - expr) == 0


def zero_boundary_faces(coefficients, degrees):
    """
    Enumerates all 3^4 boundary patterns:
    None = coordinate free/interior, 0 = lower face, 1 = upper face.
    With nonnegative Bernstein coefficients, a face is a zero face iff
    no positive coefficient has a basis function nonzero on that face.
    """
    patterns = []
    for state in itertools.product([None, 0, 1], repeat=4):
        if all(v is None for v in state):
            continue
        has_positive_term = False
        for idx, value in coefficients.items():
            if sign_qsqrt5(value) <= 0:
                continue
            compatible = True
            for j, fixed in enumerate(state):
                if fixed == 0 and idx[j] != 0:
                    compatible = False
                    break
                if fixed == 1 and idx[j] != degrees[j]:
                    compatible = False
                    break
            if compatible:
                has_positive_term = True
                break
        if not has_positive_term:
            patterns.append(state)

    maximal = []
    for state in patterns:
        state_fixed = sum(v is not None for v in state)
        contained_in_larger = False
        for other in patterns:
            other_fixed = sum(v is not None for v in other)
            if other_fixed >= state_fixed:
                continue
            if all(a is None or a == b for a, b in zip(other, state)):
                contained_in_larger = True
                break
        if not contained_in_larger:
            maximal.append(state)
    return patterns, maximal


def make_region(region):
    if region == "LOWER":
        xx = s * (1 + t)
        yy = s * (1 - t)
    elif region == "UPPER":
        xx = 1 + s + (1 - s) * t
        yy = 1 + s - (1 - s) * t
    else:
        raise ValueError(region)

    zz = 2 * W
    kval = KC * T
    B = (PHI + kval) / 2
    Fx = F(xx, yy, zz, kval)
    Fy = F(yy, xx, zz, kval)
    Fz = F(zz, xx, yy, kval)
    ux, uy, uz = u(xx), u(yy), u(zz)

    minors = {
        "Mxx": sp.expand(Fx + B * ux),
        "Myy": sp.expand(Fy + B * uy),
        "Mzz": sp.expand(Fz + B * uz),
        "Nxy": sp.expand(Fx * Fy + B * (Fx * uy + Fy * ux)),
        "Nxz": sp.expand(Fx * Fz + B * (Fx * uz + Fz * ux)),
        "Nyz": sp.expand(Fy * Fz + B * (Fy * uz + Fz * uy)),
        "DET": sp.expand(
            Fx * Fy * Fz
            + B * (Fy * Fz * ux + Fx * Fz * uy + Fx * Fy * uz)
        ),
    }
    return minors


def main():
    report = {
        "project": "QXY32_A",
        "audit": "XX-M",
        "field": "Q(sqrt(5))",
        "floating_point_used_for_signs": False,
        "checks": {},
        "certificates": {},
        "reservations": [],
    }

    # 1. Determinant rank-one identity, with independent formal s_i.
    f1, f2, f3, h1, h2, h3, beta = sp.symbols(
        "f1 f2 f3 h1 h2 h3 beta"
    )
    MM = sp.diag(f1, f2, f3) + beta * sp.Matrix([h1, h2, h3]) * sp.Matrix([[h1, h2, h3]])
    det_direct = sp.expand(MM.det())
    det_rank_one = sp.expand(
        f1*f2*f3 + beta*(f2*f3*h1**2 + f1*f3*h2**2 + f1*f2*h3**2)
    )
    report["checks"]["determinant_rank_one_identity"] = (
        sp.expand(det_direct - det_rank_one) == 0
    )

    # 2. Exact scalar formulas and permutation identities.
    X, Y, Z, K = sp.symbols("X Y Z K", real=True)
    BB = (PHI + K) / 2
    def FF(a, b, c):
        return sp.expand(a*(R-BB*(2-a)) + (PHI-K*a)*(b+c))
    def Npair(a, b, c):
        fa, fb = FF(a,b,c), FF(b,a,c)
        return sp.expand(fa*fb + BB*(fa*u(b) + fb*u(a)))

    fx, fy, fz = FF(X,Y,Z), FF(Y,X,Z), FF(Z,X,Y)
    ux, uy, uz = u(X), u(Y), u(Z)
    detpoly = sp.expand(fx*fy*fz + BB*(fy*fz*ux + fx*fz*uy + fx*fy*uz))
    perms = list(itertools.permutations([X,Y,Z]))
    report["checks"]["determinant_invariant_under_six_permutations"] = all(
        sp.expand(detpoly.subs({X:p[0],Y:p[1],Z:p[2]}, simultaneous=True)-detpoly) == 0
        for p in perms
    )
    nxy = Npair(X,Y,Z)
    report["checks"]["Nxy_symmetric_in_x_y"] = sp.expand(nxy-Npair(Y,X,Z)) == 0
    report["checks"]["Nxz_is_permuted_Nxy"] = sp.expand(
        (fx*fz + BB*(fx*uz + fz*ux)) - Npair(X,Z,Y)
    ) == 0
    report["checks"]["Nyz_is_permuted_Nxy"] = sp.expand(
        (fy*fz + BB*(fy*uz + fz*uy)) - Npair(Y,Z,X)
    ) == 0

    # 3. Diagonal Bernstein certificates on x,y,z in [0,2], k=KC*T.
    TT = sp.symbols("TT")
    kval = KC * TT
    diag_polys = {
        "Mxx": 2*R*X + (PHI - 2*kval*X)*(2*Y+2*Z),
        "Myy": 2*R*Y + (PHI - 2*kval*Y)*(2*X+2*Z),
        "Mzz": 2*R*Z + (PHI - 2*kval*Z)*(2*X+2*Y),
    }
    for name, expr in diag_polys.items():
        degrees = (1,1,1,1)
        bc = bernstein_coefficients(expr, (X,Y,Z,TT), degrees)
        report["certificates"][name] = {
            **signs_report(bc),
            "degree": degrees,
            "exact_reconstruction": check_reconstruction(
                expr, bc, (X,Y,Z,TT), degrees
            ),
        }

    # 4. LOWER/UPPER determinant and representative Nxy certificates.
    regions = {name: make_region(name) for name in ("LOWER","UPPER")}
    det_bases = {}
    for region, polynomials in regions.items():
        det_q = sp.expand(polynomials["DET"].subs(t**2, q))
        det_degrees = (5,2,3,3)
        det_bc = bernstein_coefficients(det_q, (s,q,W,T), det_degrees)
        det_bases[region] = det_bc
        report["certificates"][f"{region}_DET"] = {
            **signs_report(det_bc),
            "degree": det_degrees,
            "exact_reconstruction": check_reconstruction(
                det_q, det_bc, (s,q,W,T), det_degrees
            ),
        }

        nxy_q = sp.expand(polynomials["Nxy"].subs(t**2, q))
        nxy_degrees = (4,2,2,2)
        nxy_bc = bernstein_coefficients(nxy_q, (s,q,W,T), nxy_degrees)
        report["certificates"][f"{region}_Nxy"] = {
            **signs_report(nxy_bc),
            "degree": nxy_degrees,
            "exact_reconstruction": check_reconstruction(
                nxy_q, nxy_bc, (s,q,W,T), nxy_degrees
            ),
        }
        report["checks"][f"{region}_Nxy_even_in_t"] = all(
            exponent[0] % 2 == 0
            for exponent, coefficient in sp.Poly(
                polynomials["Nxy"], t
            ).terms()
            if coefficient != 0
        )
        patterns, maximal = zero_boundary_faces(det_bc, det_degrees)
        report["checks"][f"{region}_DET_zero_boundary_patterns"] = {
            "number_of_zero_patterns": len(patterns),
            "maximal_zero_faces": maximal,
        }

    # 5. XX-F1: UPPER Nxy, Nxz, Nyz, with correct t treatment.
    upper = regions["UPPER"]
    xx_f1 = {}
    for name in ("Nxy","Nxz","Nyz"):
        expr = upper[name]
        if name == "Nxy":
            expr = sp.expand(expr.subs(t**2, q))
            variables = (s,q,W,T)
        else:
            variables = (s,t,W,T)
        degrees = (4,2,2,2)
        bc = bernstein_coefficients(expr, variables, degrees)
        xx_f1[name] = bc
        report["certificates"][f"XX_F1_UPPER_{name}"] = {
            **signs_report(bc),
            "degree": degrees,
            "exact_reconstruction": check_reconstruction(
                expr, bc, variables, degrees
            ),
        }

    report["checks"]["UPPER_Nxz_minus_t_equals_Nyz_plus_t"] = (
        sp.expand(upper["Nxz"].subs(t,-t)-upper["Nyz"]) == 0
    )
    report["checks"]["LOWER_Nxz_minus_t_equals_Nyz_plus_t"] = (
        sp.expand(regions["LOWER"]["Nxz"].subs(t,-t)-regions["LOWER"]["Nyz"]) == 0
    )

    # 6. Historical LOWER fixed-pair Nxz diagnostic.
    lower_nxz = regions["LOWER"]["Nxz"]
    lower_nxz_bc = bernstein_coefficients(
        lower_nxz, (s,t,W,T), (4,2,2,2)
    )
    negs = [
        (idx, sp.sstr(value))
        for idx,value in lower_nxz_bc.items()
        if sign_qsqrt5(value) < 0
    ]
    report["certificates"]["LOWER_fixed_chart_Nxz_diagnostic"] = {
        **signs_report(lower_nxz_bc),
        "degree": (4,2,2,2),
        "negative_coefficients": negs,
        "interpretation": (
            "This fixed-chart certificate is not used in the proof: "
            "all pair-minors are covered by the exact permutation identities "
            "and the LOWER/UPPER Nxy representative certificates."
        ),
    }

    # 7. Exact zero matrices at the two determinant zero points.
    f_origin = [F(0,0,0,0)] * 3
    f_corner = [sp.simplify(F(2,2,2,KC))] * 3
    report["checks"]["F_all_zero_at_origin"] = all(sp.simplify(v)==0 for v in f_origin)
    report["checks"]["F_all_zero_at_upper_corner_kc"] = all(sp.simplify(v)==0 for v in f_corner)
    report["checks"]["u_all_zero_at_both_zero_points"] = (
        all(u(v)==0 for v in (0,0,0,2,2,2))
    )

    # 8. Aggregate count for the minimal permutation-reduced proof.
    minimal = []
    for name in ("Mxx","Myy","Mzz"):
        minimal.append(report["certificates"][name])
    for region in ("LOWER","UPPER"):
        minimal.append(report["certificates"][f"{region}_Nxy"])
        minimal.append(report["certificates"][f"{region}_DET"])
    report["minimal_proof_coefficient_totals"] = {
        key: sum(item[key] for item in minimal)
        for key in ("total","positive","zero","negative")
    }

    report["proof_logic"] = [
        "All three diagonal principal minors are nonnegative by their exact Bernstein certificates.",
        "Nxy is nonnegative on the full domain by LOWER/UPPER coverage and exact Bernstein certificates.",
        "Nxy symmetry and the exact permutation identities transfer this certificate to Nxz and Nyz.",
        "The determinant is symmetric under all six coordinate permutations and nonnegative by LOWER/UPPER Bernstein certificates.",
        "All seven principal minors of the real symmetric 3x3 matrix are therefore nonnegative, hence M is positive semidefinite.",
        "The Bernstein support analysis gives the only determinant zero faces: LOWER s=0,W=0 and UPPER s=1,W=1,T=1.",
        "These faces map respectively to (x,y,z)=(0,0,0), arbitrary k, and (x,y,z)=(2,2,2), k=kc; M is exactly zero at both.",
        "Away from these two points det(M)>0, so M is positive definite and has rank 3; at the two points M has rank 0."
    ]
    report["reservations"] = [
        "The original physical XIX/XX source files and their raw outputs were not available to this script; it is an independent reconstruction from the mathematical definitions.",
        "The historical claim for the LOWER fixed-coordinate Nxz coefficient count is not reproduced in this chart; a negative Bernstein coefficient is recorded. It is not used in the permutation-reduced proof.",
        "This audit does not recalculate SHA-256 hashes of the historical source files."
    ]

    # All essential checks must pass, except the explicitly diagnostic LOWER Nxz sign issue.
    essential = [
        report["checks"]["determinant_rank_one_identity"],
        report["checks"]["determinant_invariant_under_six_permutations"],
        report["checks"]["Nxy_symmetric_in_x_y"],
        report["checks"]["Nxz_is_permuted_Nxy"],
        report["checks"]["Nyz_is_permuted_Nxy"],
        report["checks"]["F_all_zero_at_origin"],
        report["checks"]["F_all_zero_at_upper_corner_kc"],
        report["checks"]["u_all_zero_at_both_zero_points"],
    ]
    for item in report["certificates"].values():
        if item.get("interpretation"):
            continue
        essential.append(item["negative"] == 0)
        essential.append(item["exact_reconstruction"])
    report["conclusion"] = (
        "PASS_INDEPENDENT_EXACT_PERMUTATION_REDUCED_CERTIFICATE"
        if all(essential)
        else "FAIL"
    )
    print(json.dumps(report, indent=2, ensure_ascii=False, default=str))


if __name__ == "__main__":
    main()
