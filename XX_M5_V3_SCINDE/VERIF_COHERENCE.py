#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
QXY32_A — XX-M5 V3 SCINDE — CONTROLE DE COHERENCE
Relit les 7 certificats JSON du dossier et vérifie, pour chacun :
    1. JSON valide.
    2. En-tête conforme aux valeurs attendues (nom, variables, degrés,
     comptages, reconstruction_exact, faces nulles).
    3. count = nombre de coefficients = produit des (degré + 1).
    4. positive + zero + negative = count.
    5. Chaque sign cohérent avec value ("0" <=> sign 0, sinon sign 1).
    6. Indices complets : tout le pavé, sans trou, sans doublon,
     dans l'ordre lexicographique.
    7. Comptages recalculés depuis les signes conformes à l'en-tête.
Vérifie aussi le total global : 894 coefficients.
Ce script ne modifie aucun fichier. Code retour 0 si tout passe, 1 sinon.
"""

import itertools
import json
import math
import sys
from pathlib import Path

ATTENDU = {
    "XX_M5_V3_Mxx.json": {
        "name": "Mxx", "variables": ["X", "Y", "Z", "TT"],
        "degrees": [1, 1, 1, 1], "count": 16,
        "positive": 13, "zero": 3, "negative": 0,
        "zero_faces": [[0, 0, 0, None], [1, 1, 1, 1]],
    },
    "XX_M5_V3_Myy.json": {
        "name": "Myy", "variables": ["X", "Y", "Z", "TT"],
        "degrees": [1, 1, 1, 1], "count": 16,
        "positive": 13, "zero": 3, "negative": 0,
        "zero_faces": [[0, 0, 0, None], [1, 1, 1, 1]],
    },
    "XX_M5_V3_Mzz.json": {
        "name": "Mzz", "variables": ["X", "Y", "Z", "TT"],
        "degrees": [1, 1, 1, 1], "count": 16,
        "positive": 13, "zero": 3, "negative": 0,
        "zero_faces": [[0, 0, 0, None], [1, 1, 1, 1]],
    },
    "XX_M5_V3_LOWER_Nxy.json": {
        "name": "LOWER_Nxy", "variables": ["s", "q", "W", "T"],
        "degrees": [4, 2, 2, 2], "count": 135,
        "positive": 108, "zero": 27, "negative": 0,
        "zero_faces": [[0, None, 0, None]],
    },
    "XX_M5_V3_LOWER_DET.json": {
        "name": "LOWER_DET", "variables": ["s", "q", "W", "T"],
        "degrees": [5, 2, 3, 3], "count": 288,
        "positive": 216, "zero": 72, "negative": 0,
        "zero_faces": [[0, None, 0, None]],
    },
    "XX_M5_V3_UPPER_Nxy.json": {
        "name": "UPPER_Nxy", "variables": ["s", "q", "W", "T"],
        "degrees": [4, 2, 2, 2], "count": 135,
        "positive": 123, "zero": 12, "negative": 0,
        "zero_faces": [[1, None, 1, 1]],
    },
    "XX_M5_V3_UPPER_DET.json": {
        "name": "UPPER_DET", "variables": ["s", "q", "W", "T"],
        "degrees": [5, 2, 3, 3], "count": 288,
        "positive": 258, "zero": 30, "negative": 0,
        "zero_faces": [[1, None, 1, 1]],
    },
}

def controler(chemin, attendu):
    erreurs = []
    try:
        with open(chemin, encoding="utf-8") as f:
            doc = json.load(f)
    except (OSError, json.JSONDecodeError) as exc:
        return [f"JSON invalide ou illisible : {exc}"]

    for cle in ("name", "variables", "degrees", "count",
                "positive", "zero", "negative", "zero_faces"):
        if doc.get(cle) != attendu[cle]:
            erreurs.append(f"en-tête {cle} : {doc.get(cle)!r} != attendu {attendu[cle]!r}")
    if doc.get("reconstruction_exact") is not True:
        erreurs.append(f"reconstruction_exact : {doc.get('reconstruction_exact')!r} != True")

    coeffs = doc.get("coefficients")
    if not isinstance(coeffs, list):
        return erreurs + ["coefficients n'est pas une liste"]

    degres = attendu["degrees"]
    produit = math.prod(d + 1 for d in degres)
    if attendu["count"] != produit:
        erreurs.append(f"count attendu {attendu['count']} != produit {produit}")
    if len(coeffs) != attendu["count"]:
        erreurs.append(f"nombre de coefficients {len(coeffs)} != count {attendu['count']}")
    if attendu["positive"] + attendu["zero"] + attendu["negative"] != attendu["count"]:
        erreurs.append("positive + zero + negative != count")

    indices = []
    positifs = nuls = negatifs = 0
    for i, c in enumerate(coeffs):
        idx, valeur, signe = c.get("index"), c.get("value"), c.get("sign")
        indices.append(tuple(idx) if isinstance(idx, list) else idx)
        if signe == 1:
            positifs += 1
        elif signe == 0:
            nuls += 1
        elif signe == -1:
            negatifs += 1
        else:
            erreurs.append(f"coefficient {i} : sign inattendu {signe!r}")
        if (valeur == "0") != (signe == 0):
            erreurs.append(f"coefficient {i} (index {idx}) : value {valeur!r} incohérente avec sign {signe!r}")
        if not isinstance(valeur, str) or not valeur:
            erreurs.append(f"coefficient {i} (index {idx}) : value non valide")

    if (positifs, nuls, negatifs) != (attendu["positive"], attendu["zero"], attendu["negative"]):
        erreurs.append(
            f"comptages recalculés (pos={positifs}, zero={nuls}, neg={negatifs}) "
            f"!= en-tête (pos={attendu['positive']}, zero={attendu['zero']}, neg={attendu['negative']})"
        )

    pavé = set(itertools.product(*(range(d + 1) for d in degres)))
    if len(indices) != len(set(indices)):
        erreurs.append("indices en double")
    if set(indices) != pavé:
        manquants = sorted(pavé - set(indices))[:5]
        surplus = sorted(set(indices) - pavé)[:5]
        erreurs.append(f"indices incomplets : manquants {manquants}, surplus {surplus}")
    if indices != sorted(indices):
        erreurs.append("coefficients non rangés dans l'ordre lexicographique")

    return erreurs

def main():
    dossier = Path(__file__).resolve().parent
    total = 0
    echec = False
    for nom, attendu in ATTENDU.items():
        erreurs = controler(dossier / nom, attendu)
        total += attendu["count"]
        if erreurs:
            echec = True
            print(f"FAIL {nom}")
            for e in erreurs:
                print(f"  - {e}")
        else:
            print(f"PASS {nom} ({attendu['count']} coefficients)")
    print(f"TOTAL : {total} coefficients (attendu 894)")
    if total != 894:
        echec = True
        print("FAIL : total != 894")
    print("VERDICT : " + ("ECHEC" if echec else "TOUT PASSE"))
    return 1 if echec else 0

if __name__ == "__main__":
    sys.exit(main())
