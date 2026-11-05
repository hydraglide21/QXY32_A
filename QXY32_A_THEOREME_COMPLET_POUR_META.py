#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
QXY32_A — DOSSIER MAITRE DU THEOREME — POUR META / GITHUB
========================================================

Objet
-----
Rassembler dans un seul fichier :
  * l'énoncé cible du théorème QXY32_A ;
  * les définitions exactes de la matrice ;
  * les identités algébriques retrouvées pour le Bloc 2 ;
  * la réduction du déterminant et sa base de Bernstein (Bloc 3) ;
  * les formules des diagonales et mineurs (Bloc 4) ;
  * l'inventaire des certificats des Blocs 1 à 7B ;
  * les statuts historiques, les anomalies et les instructions de
    contre-expertise indépendante.

IMPORTANT — INTÉGRITÉ SCIENTIFIQUE
----------------------------------
Ce dossier maître ne prétend PAS remplacer les scripts sources historiques
des Blocs 1, 3, 4, 5A, 5B et 6A V2, ni leurs sorties brutes.
Les comptages historiques sont enregistrés comme RAPPORTÉS, et non comme
reproduits par ce fichier. L'exécution des contrôles symboliques ci-dessous
ne certifie pas à elle seule la positivité globale ni le théorème complet.

Les anciennes versions doivent être archivées, jamais écrasées.
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from math import comb
import sympy as sp

# ============================================================================
# PARTIE 0 — CONSTANTES EXACTES ET DOMAINE
# ============================================================================

SQ5 = sp.sqrt(5)
PHI = (1 + SQ5) / 2
KC = (1 + 2 * SQ5) / 4

x, y, z, k = sp.symbols("x y z k", real=True)
B = (PHI + k) / 2

DOMAIN = {
    "x": "[0, 2]",
    "y": "[0, 2]",
    "z": "[0, 2]",
    "k": "[0, (1+2*sqrt(5))/4]",
}

def exact_zero(name: str, expression) -> None:
    """Échoue si l'expression n'est pas identiquement nulle."""
    residual = sp.simplify(sp.expand(expression))
    if residual != 0:
        raise AssertionError(f"[FAIL] {name}\nRésidu exact : {residual}")
    print(f"[PASS] {name}")

# ============================================================================
# PARTIE 1 — MODÈLE : FONCTIONS, VECTEUR ET MATRICE
# ============================================================================

def u(a):
    return a * (2 - a)

def F(a, b, c):
    return sp.expand(
        a * (SQ5 - B * (2 - a))
        + (PHI - k * a) * (b + c)
    )

Fx = F(x, y, z)
Fy = F(y, x, z)
Fz = F(z, x, y)

ux, uy, uz = u(x), u(y), u(z)

# M = diag(Fx,Fy,Fz) + B*s*s^T, avec s_i=sqrt(u_i).
# Pour éviter des racines symboliques inutiles, les entrées sont données
# sous la forme exacte équivalente ci-dessous.
Mxx = sp.expand(Fx + B * ux)
Myy = sp.expand(Fy + B * uy)
Mzz = sp.expand(Fz + B * uz)

# ============================================================================
# PARTIE 2 — MINEURS PRINCIPAUX ET DÉTERMINANT
# ============================================================================

Nxy = sp.expand(Fx * Fy + B * (ux * Fy + uy * Fx))
Nxz = sp.expand(Fx * Fz + B * (ux * Fz + uz * Fx))
Nyz = sp.expand(Fy * Fz + B * (uy * Fz + uz * Fy))

DET_RANK_ONE = sp.expand(
    Fx * Fy * Fz
    + B * (ux * Fy * Fz + uy * Fx * Fz + uz * Fx * Fy)
)

DET_DIRECT = sp.expand(
    Mxx * Myy * Mzz
    - B**2 * (Mxx * uy * uz + Myy * ux * uz + Mzz * ux * uy)
    + 2 * B**3 * ux * uy * uz
)

# ============================================================================
# PARTIE 3 — RÉDUCTIONS SYMÉTRIQUES EXACTES DU BLOC 2
# ============================================================================

S, Delta = sp.symbols("S Delta", real=True)
P = (S**2 - Delta) / 4

T = sp.expand(S * (SQ5 - k) + B * S**2 - 2 * (B + k) * P)
J = sp.expand(SQ5 - 2 * PHI - k + B * S)
X = sp.expand(2 * S - S**2 + 2 * P)
Y = sp.expand(2 * PHI - k * S)

R0 = sp.expand((T**2 - Delta * J**2) / 4)
R1 = sp.expand((T * Y + k * Delta * J) / 2)
R2 = sp.expand((Y**2 - k**2 * Delta) / 4)

S0 = sp.expand((X * T - Delta * (2 - S) * J) / 2)
S1 = sp.expand((X * Y + k * Delta * (2 - S)) / 2)

E = sp.expand(R0 + B * S0)
L = sp.expand(R1 + B * S1)

def verify_block2_identities():
    """Vérifie les identités A+C, A-C, U+V, U-V et produits associés."""
    xx, yy = sp.symbols("xx yy", real=True)
    SS = xx + yy
    DD = (xx - yy)**2
    PP = xx * yy

    BB = B
    AA = xx * (SQ5 - 2 * BB) + BB * xx**2 + PHI * yy - k * xx * yy
    CC = yy * (SQ5 - 2 * BB) + BB * yy**2 + PHI * xx - k * xx * yy
    alpha = PHI - k * xx
    beta = PHI - k * yy
    UU, VV = xx * (2 - xx), yy * (2 - yy)

    substitutions = {S: SS, Delta: DD}
    exact_zero("Bloc 2 : A+C=T",
               (AA + CC) - T.subs(substitutions))
    exact_zero("Bloc 2 : A-C=(x-y)J",
               (AA - CC) - ((xx - yy) * J).subs(substitutions))
    exact_zero("Bloc 2 : U+V=X",
               (UU + VV) - X.subs(substitutions))
    exact_zero("Bloc 2 : U-V=(x-y)(2-S)",
               (UU - VV) - ((xx - yy) * (2 - S)).subs(substitutions))
    exact_zero("Bloc 2 : AC=R0",
               AA * CC - R0.subs(substitutions))
    exact_zero("Bloc 2 : A*beta+alpha*C=R1",
               (AA * beta + alpha * CC) - R1.subs(substitutions))
    exact_zero("Bloc 2 : alpha*beta=R2",
               alpha * beta - R2.subs(substitutions))
    exact_zero("Bloc 2 : U*C+V*A=S0",
               (UU * CC + VV * AA) - S0.subs(substitutions))
    exact_zero("Bloc 2 : U*beta+V*alpha=S1",
               (UU * beta + VV * alpha) - S1.subs(substitutions))

# ============================================================================
# PARTIE 4 — DÉTERMINANT CUBIQUE EN z ET BERNSTEIN (BLOC 3)
# ============================================================================

c0 = PHI * S
c1 = SQ5 - 2 * B - k * S

d0 = sp.expand(c0 * E)
d1 = sp.expand(c0 * L + c1 * E + 2 * B * R0)
d2 = sp.expand(c0 * R2 + c1 * L + B * E + 2 * B * R1 - B * R0)
d3 = sp.expand((c1 + 2 * B) * R2 + B * (L - R1))

BERNSTEIN_Z = [
    sp.expand(d0),
    sp.expand(d0 + 2 * d1 / 3),
    sp.expand(d0 + 4 * d1 / 3 + 4 * d2 / 3),
    sp.expand(d0 + 2 * d1 + 4 * d2 + 8 * d3),
]

def verify_bernstein_cubic():
    """Vérifie la reconstruction sur t=z/2."""
    t = sp.symbols("t", real=True)
    b0, b1, b2, b3 = BERNSTEIN_Z
    bernstein_form = (
        b0 * (1-t)**3
        + 3*b1*t*(1-t)**2
        + 3*b2*t**2*(1-t)
        + b3*t**3
    )
    power_form = d0 + 2*d1*t + 4*d2*t**2 + 8*d3*t**3
    exact_zero("Bloc 3 : reconstruction Bernstein cubique",
               bernstein_form - power_form)

# ============================================================================
# PARTIE 5 — CONVERSION BERNSTEIN TENSORIELLE
# ============================================================================

def tensor_bernstein_coefficients(polynomial, variables, degrees):
    """
    Convertit un polynôme en coefficients Bernstein sur [0,1]^n.
    Retourne un dictionnaire index -> coefficient exact SymPy.
    """
    poly = sp.Poly(sp.expand(polynomial), *variables)
    result = {}
    ranges = [range(n + 1) for n in degrees]

    from itertools import product
    for index in product(*ranges):
        value = sp.Integer(0)
        for monomial, coefficient in poly.terms():
            if all(monomial[j] <= index[j] for j in range(len(index))):
                factor = sp.Integer(1)
                for j, degree in enumerate(degrees):
                    factor *= sp.Rational(
                        comb(index[j], monomial[j]),
                        comb(degree, monomial[j])
                    )
                value += coefficient * factor
        result[index] = sp.simplify(value)
    return result

s, q, w = sp.symbols("s q w", real=True)

LOWER_RECTANGLE = {S: 2*s, Delta: 4*s**2*q, k: KC*w}
UPPER_RECTANGLE = {S: 2+2*s, Delta: 4*(1-s)**2*q, k: KC*w}

# ============================================================================
# PARTIE 6 — FORMULES DU BLOC 4 : DIAGONALES ET MINEURS
# ============================================================================

def diagonal_formula(a, b, c):
    return sp.expand(
        SQ5*a + (PHI-k*a)*(b+c)
    )

DIAGONAL_X = diagonal_formula(x, y, z)
DIAGONAL_Y = diagonal_formula(y, x, z)
DIAGONAL_Z = diagonal_formula(z, x, y)

# ============================================================================
# PARTIE 7 — ÉNONCÉ CIBLE DU THÉORÈME
# ============================================================================

THEOREM_STATEMENT = r"""
Soient r=sqrt(5), phi=(1+sqrt(5))/2, kc=(1+2sqrt(5))/4,
0 <= k <= kc et (x,y,z) dans [0,2]^3.
Posons B=(phi+k)/2, u_i=x_i(2-x_i),
F(a,b,c)=a(r-B(2-a))+(phi-ka)(b+c), et
M=diag(F(x,y,z),F(y,x,z),F(z,x,y))+B*s*s^T,
où s=(sqrt(u_x),sqrt(u_y),sqrt(u_z))^T.

THÉORÈME CIBLE À CERTIFIER :
(i) M est positive semi-définie sur tout le domaine.
(ii) det(M)=0 exactement à l'origine (pour tout k admissible)
     et au sommet (2,2,2) lorsque k=kc.
(iii) Sur ces lieux, M est la matrice nulle et son rang vaut 0.
(iv) Partout ailleurs, le rang vaut 3 ; il n'existe pas de cas
     singulier de rang 1 ou 2.
"""

# ============================================================================
# PARTIE 8 — INVENTAIRE HISTORIQUE DES BLOCS
# ============================================================================

BLOCK_REGISTER = {
    "BLOC_1": {
        "artifact": "QXY32_A_CERTIFICAT_GLOBAL_V6.py",
        "historical_status": "source mentionnée dans les travaux antérieurs",
        "execution_in_this_file": False,
    },
    "BLOC_2": {
        "artifact": "reductions_symetriques_exactes",
        "historical_status": "identités exactes retrouvées et encodées ici",
        "execution_in_this_file": True,
    },
    "BLOC_3": {
        "artifact": "CONTRE_EXPERTISE_BLOC3_QXY32_A.py",
        "historical_status": "comptages Bernstein rapportés : 540 au total, 447 positifs, 93 nuls, 0 négatif",
        "execution_in_this_file": False,
    },
    "BLOC_4": {
        "artifact": "diagonales_et_mineurs",
        "historical_status": "formules et comptages rapportés ; source complète/sortie brute à joindre",
        "execution_in_this_file": False,
    },
    "BLOC_5A": {
        "artifact": "certificat_diagonales_V6_1",
        "historical_status": "16 coefficients rapportés : 13 positifs, 3 nuls, 0 négatif",
        "execution_in_this_file": False,
    },
    "BLOC_5B": {
        "artifact": "certificat_mineurs_V6_1",
        "historical_status": "comptages historiques rapportés ; conserver source et sortie brute",
        "execution_in_this_file": False,
    },
    "BLOC_6A_V2": {
        "artifact": "QXY32_A_BLOC_6A_DETERMINANT_V2.py",
        "historical_status": "576 coefficients et 162 strates rapportés ; anomalie du test de signe à corriger/auditer",
        "execution_in_this_file": False,
    },
    "BLOC_7A": {
        "artifact": "implication_PSD_et_classification_du_rang",
        "historical_status": "argument de critère PSD et classification rapportés",
        "execution_in_this_file": False,
    },
    "BLOC_7B_V2": {
        "artifact": "QXY32_A_BLOC_7B_CERTIFICAT_FINAL_V2.py",
        "historical_status": "architecture de manifeste et audit rédigée ; exécution finale non établie",
        "execution_in_this_file": False,
    },
}

HISTORICAL_RESULTS = {
    "BLOC3": {
        "total_coefficients": 540,
        "positive": 447,
        "zero": 93,
        "negative": 0,
        "status": "REPORTED_NOT_REPRODUCED_BY_THIS_MASTER",
    },
    "BLOC4": {
        "diagonal_Mxx": {"positive": 13, "zero": 3, "negative": 0},
        "minor_Nxy": {"positive": 231, "zero": 39, "negative": 0},
        "status": "REPORTED_NOT_REPRODUCED_BY_THIS_MASTER",
    },
    "BLOC5A": {
        "coefficients": 16,
        "positive": 13,
        "zero": 3,
        "negative": 0,
        "status": "REPORTED_NOT_REPRODUCED_BY_THIS_MASTER",
    },
    "BLOC6A_V2": {
        "coefficients": 576,
        "strata": 162,
        "status": "REPORTED_NOT_REPRODUCED_BY_THIS_MASTER",
    },
}

KNOWN_AUDIT_ISSUES = [
    "Bloc 6A V2 : le test exact du signe dans Q(sqrt(5)) doit traiter le cas a=0,b!=0.",
    "Bloc 4 : joindre le script source complet et les sorties brutes historiques.",
    "Blocs 3, 5A, 5B, 6A V2 : joindre les sources exactes et sorties brutes pour reproduction.",
    "Bloc 7B V2 : exécuter le manifeste après intégration effective de tous les fichiers.",
    "Ne pas confondre cohérence symbolique locale et preuve globale de positivité.",
]

# ============================================================================
# PARTIE 9 — STATUTS ET MANIFESTE
# ============================================================================

STATUSES = (
    "RETRIEVED",
    "DRAFTED",
    "EXECUTED",
    "REPRODUCED",
    "INDEPENDENTLY_VERIFIED",
    "REPORTED",
    "CONDITIONAL",
    "NOT_AVAILABLE",
)

def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()

def build_manifest(root: Path):
    files = []
    for path in sorted(root.rglob("*")):
        if path.is_file() and path.name != "manifest_sha256.json":
            files.append({
                "path": str(path.relative_to(root)),
                "sha256": sha256_file(path),
                "bytes": path.stat().st_size,
            })
    return {
        "project": "QXY32_A",
        "manifest_version": "1.0",
        "files": files,
        "warning": (
            "L'intégrité SHA-256 ne prouve ni l'exactitude mathématique "
            "ni la reproductibilité d'un résultat."
        ),
    }

# ============================================================================
# PARTIE 10 — CONTROLES EXÉCUTABLES DE CE FICHIER
# ============================================================================

def run_local_symbolic_checks():
    print("=" * 78)
    print("QXY32_A — CONTROLES SYMBOLIQUES DU DOSSIER MAITRE")
    print("=" * 78)

    exact_zero(
        "Déterminant direct = déterminant formule rang-un",
        DET_DIRECT - DET_RANK_ONE
    )

    verify_block2_identities()
    verify_bernstein_cubic()

    # Vérification des paramètres de rectangles : contrôle des substitutions.
    exact_zero(
        "Rectangle inférieur : S=2s",
        (S - 2*s).subs(LOWER_RECTANGLE)
    )
    exact_zero(
        "Rectangle inférieur : Delta=4s²q",
        (Delta - 4*s**2*q).subs(LOWER_RECTANGLE)
    )
    exact_zero(
        "Rectangle inférieur : k=kc*w",
        (k - KC*w).subs(LOWER_RECTANGLE)
    )
    exact_zero(
        "Rectangle supérieur : S=2+2s",
        (S - 2 - 2*s).subs(UPPER_RECTANGLE)
    )
    exact_zero(
        "Rectangle supérieur : Delta=4(1-s)²q",
        (Delta - 4*(1-s)**2*q).subs(UPPER_RECTANGLE)
    )
    exact_zero(
        "Rectangle supérieur : k=kc*w",
        (k - KC*w).subs(UPPER_RECTANGLE)
    )

    print("\n[INFO] Contrôles locaux exécutés avec SymPy.")
    print("[INFO] Les certificats globaux des blocs historiques ne sont pas exécutés ici.")
    print("[INFO] Les comptages historiques restent au statut RAPPORTÉ.")

# ============================================================================
# PARTIE 11 — DIRECTIVES DE CONTRE-EXPERTISE POUR META
# ============================================================================

META_AUDIT_INSTRUCTIONS = r"""
MISSION DE META — CONTRE-EXPERTISE QXY32_A

1. Lire intégralement le théorème, les définitions et chaque script source.
2. Ne supprimer ni remplacer aucune version historique.
3. Reconstituer les dépendances entre Blocs 1, 2, 3, 4, 5A, 5B, 6A V2,
   7A et 7B V2.
4. Vérifier les identités exactes dans Q(sqrt(5)), sans flottants.
5. Vérifier indépendamment le déterminant direct et le déterminant de rang un.
6. Vérifier les réductions symétriques S, Delta, les formules R0,R1,R2,
   S0,S1,E,L et la réduction cubique en z.
7. Recalculer les conversions Bernstein, les degrés, les coefficients,
   les signes exacts et les strates frontières.
8. Vérifier séparément intérieur, faces, arêtes et sommets.
9. Examiner explicitement l'anomalie a=0,b!=0 du test de signe du Bloc 6A V2.
10. Produire pour chaque script : sortie brute, code de vérification indépendant,
    sortie du vérificateur et rapport d'audit.
11. Calculer SHA-256 de chaque source et sortie réellement présente.
12. Distinguer strictement :
      - identité symbolique vérifiée ;
      - script exécuté ;
      - résultat reproduit ;
      - audit indépendant réussi ;
      - théorème global certifié.
13. Ne pas conclure à une erreur mathématique sur la seule base d'une
    erreur de programmation ; isoler et expliquer chaque cas.
14. Ne pas conclure à la certification globale tant que toutes les
    obligations logiques et les certificats de positivité requis ne sont
    pas vérifiés.
15. Préserver le travail historique et documenter toute correction comme
    une nouvelle version.
"""

# ============================================================================
# PARTIE 12 — RAPPORT
# ============================================================================

def print_report():
    print("\nÉNONCÉ CIBLE")
    print(THEOREM_STATEMENT)
    print("\nINVENTAIRE DES BLOCS")
    for name, item in BLOCK_REGISTER.items():
        print(f"- {name}: {item['artifact']}")
        print(f"  statut historique: {item['historical_status']}")
    print("\nANOMALIES / PIÈCES À JOINDRE")
    for issue in KNOWN_AUDIT_ISSUES:
        print(f"- {issue}")
    print("\nSTATUT GLOBAL DE CE FICHIER : DOSSIER MAÎTRE / BASE DE CONTRE-EXPERTISE")
    print("Ce fichier ne déclare pas à lui seul le théorème global certifié.")

def main():
    run_local_symbolic_checks()
    print_report()

if __name__ == "__main__":
    main()
