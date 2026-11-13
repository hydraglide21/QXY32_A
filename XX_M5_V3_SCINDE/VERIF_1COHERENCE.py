#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
QXY32_A — XX-M5 V3 SCINDE — CONTROLE DE COHERENCE (CORRIGE, BI-FORMAT)

Relit les 7 certificats JSON du dossier et verifie, pour chacun, a partir
des coefficients eux-memes (jamais a partir des seules metadonnees) :
  1. JSON valide.
  2. En-tete conforme aux valeurs attendues (nom, variables, degres,
     comptages, reconstruction_exact, faces nulles).
  3. count = nombre de coefficients = produit des (degre + 1).
  4. positive + zero + negative = count.
  5. Chaque sign coherent avec value, verifie EXACTEMENT dans Q(sqrt(5))
     (parseur exact sans flottant, voir parse_qsqrt5).
  6. Indices complets : tout le pave, sans trou, sans doublon,
     dans l'ordre lexicographique.
  7. Comptages recalcules depuis les valeurs conformes a l'en-tete.
  8. Total global : 894 coefficients, 744 positifs, 150 nuls, 0 negatif.
Deux formats de "coefficients" sont acceptes :
  - FORMAT NORMALISE (format de reference) : liste d'objets
    {"index": [...], "value": "...", "sign": ...}.
  - FORMAT LEGACY TENSORIEL : listes imbriquees dont les feuilles sont
    les chaines "value", rangees en ordre lexicographique (l'indice est
    la position dans le tenseur). Accepte aussi {"tensor": <imbrique>}.
    Le nombre de feuilles DOIT etre exactement le produit des (degre+1).
    Un fichier a 24 feuilles pour des degres (1,1,1,1) est REJETE, de meme
    qu'un fichier au schema GitHub errone (champs total/positifs/nuls/negatifs/base,
    base "degre (2,2,2)") :
    24 n'est pas 2*2*2*2, et aucune convention de duplication n'est
    devinee. Voir RAPPORT_STRUCTURE_DIAGONALES.md.
Aucun certificat n'est ignore : un fichier manquant, illisible ou
invalide fait echouer la verification (code retour 1).
Ce script ne modifie aucun fichier. Code retour 0 si tout passe, 1 sinon.
"""
import itertools
import json
import math
import re
import sys
from fractions import Fraction
from pathlib import Path

ATTENDU = {
    "XX_M5_V3_Mxx.json": {"name": "Mxx", "variables": ["X", "Y", "Z", "TT"],
        "degrees": [1, 1, 1, 1], "count": 16,
        "positive": 13, "zero": 3, "negative": 0,
        "zero_faces": [[0, 0, 0, None], [1, 1, 1, 1]]},
    "XX_M5_V3_Myy.json": {"name": "Myy", "variables": ["X", "Y", "Z", "TT"],
        "degrees": [1, 1, 1, 1], "count": 16,
        "positive": 13, "zero": 3, "negative": 0,
        "zero_faces": [[0, 0, 0, None], [1, 1, 1, 1]]},
    "XX_M5_V3_Mzz.json": {"name": "Mzz", "variables": ["X", "Y", "Z", "TT"],
        "degrees": [1, 1, 1, 1], "count": 16,
        "positive": 13, "zero": 3, "negative": 0,
        "zero_faces": [[0, 0, 0, None], [1, 1, 1, 1]]},
    "XX_M5_V3_LOWER_Nxy.json": {"name": "LOWER_Nxy", "variables": ["s", "q", "W", "T"],
        "degrees": [4, 2, 2, 2], "count": 135,
        "positive": 108, "zero": 27, "negative": 0,
        "zero_faces": [[0, None, 0, None]]},
    "XX_M5_V3_LOWER_DET.json": {"name": "LOWER_DET", "variables": ["s", "q", "W", "T"],
        "degrees": [5, 2, 3, 3], "count": 288,
        "positive": 216, "zero": 72, "negative": 0,
        "zero_faces": [[0, None, 0, None]]},
    "XX_M5_V3_UPPER_Nxy.json": {"name": "UPPER_Nxy", "variables": ["s", "q", "W", "T"],
        "degrees": [4, 2, 2, 2], "count": 135,
        "positive": 123, "zero": 12, "negative": 0,
        "zero_faces": [[1, None, 1, 1]]},
    "XX_M5_V3_UPPER_DET.json": {"name": "UPPER_DET", "variables": ["s", "q", "W", "T"],
        "degrees": [5, 2, 3, 3], "count": 288,
        "positive": 258, "zero": 30, "negative": 0,
        "zero_faces": [[1, None, 1, 1]]},
}
TOTAL_ATTENDU = {"count": 894, "positive": 744, "zero": 150, "negative": 0}

# ---- Arithmetique exacte dans Q(sqrt(5)) : valeur = p + q*sqrt(5) ----
def _parse_rationnel(txt):
    txt = txt.strip()
    if "/" in txt:
        a, b = txt.split("/", 1)
        return Fraction(int(a.strip()), int(b.strip()))
    return Fraction(int(txt))

def parse_qsqrt5(valeur):
    """Renvoie (p, q) de Fractions avec valeur = p + q*sqrt(5).
    Accepte les formes presentes dans les fichiers : "0", "5",
    "1 + sqrt(5)", "2*sqrt(5) + 6", "18 + 25*sqrt(5)/2",
    "307/24 + 221*sqrt(5)/24", "sqrt(5)", "2 + 2*sqrt(5)", ..."""
    if not isinstance(valeur, str) or not valeur.strip():
        raise ValueError("value vide ou non textuelle")
    s = valeur.replace(" ", "")
    if s == "0":
        return Fraction(0), Fraction(0)
    p, q = Fraction(0), Fraction(0)
    # decoupe en termes signes : +... -... (le premier peut etre sans signe)
    if s[0] not in "+-":
        s = "+" + s
    for signe, terme in re.findall(r"([+-])([^+-]+)", s):
        mult = Fraction(1) if signe == "+" else Fraction(-1)
        if "sqrt(5)" in terme:
            avant, apres = terme.split("sqrt(5)", 1)
            avant = avant.rstrip("*")
            coef = _parse_rationnel(avant) if avant else Fraction(1)
            if apres:
                # apres est de la forme "/denominateur"
                assert apres.startswith("/"), apres
                coef = coef / Fraction(int(apres[1:]))
            q += mult * coef
        else:
            p += mult * _parse_rationnel(terme)
    return p, q

def signe_exact(valeur):
    p, q = parse_qsqrt5(valeur)
    if p == 0 and q == 0:
        return 0
    if q == 0:
        return 1 if p > 0 else -1
    # signe de p + q*sqrt(5) : comparer p^2 et 5*q^2 quand signes opposes
    if p == 0:
        return 1 if q > 0 else -1
    if (p > 0) == (q > 0):
        return 1 if p > 0 else -1
    # p et q de signes opposes : |p| vs sqrt(5)*|q|
    gauche = p * p
    droite = 5 * q * q
    if gauche == droite:
        return 0  # impossible pour p,q rationnels non nuls, sauf p=q=0
    plus_grand = "p" if gauche > droite else "q"
    if plus_grand == "p":
        return 1 if p > 0 else -1
    return 1 if q > 0 else -1

def aplatir_legacy(noeud, feuilles):
    if isinstance(noeud, list):
        for enfant in noeud:
            aplatir_legacy(enfant, feuilles)
    elif isinstance(noeud, str):
        feuilles.append(noeud)
    else:
        raise ValueError(f"feuille legacy inattendue : {noeud!r} (type {type(noeud).__name__})")

def normaliser_coefficients(brut, degres):
    """Renvoie (liste_normalisee, format, erreurs). Liste normalisee :
    [{"index": [...], "value": "...", "sign": ...}]."""
    produit = math.prod(d + 1 for d in degres)
    if isinstance(brut, dict) and "tensor" in brut:
        brut = brut["tensor"]
    if isinstance(brut, list) and brut and isinstance(brut[0], dict):
        return brut, "normalise", []
    if isinstance(brut, list):
        feuilles = []
        try:
            aplatir_legacy(brut, feuilles)
        except ValueError as exc:
            return [], "legacy", [f"format legacy invalide : {exc}"]
        if len(feuilles) != produit:
            erreurs = [f"format legacy : {len(feuilles)} feuilles, attendu {produit} "
                       f"= produit des (degre+1) pour degres {degres}. "
                       f"Aucune convention de duplication n'est devinee : "
                       f"si {len(feuilles)} > {produit}, le fichier est incoherent "
                       f"(feuilles en trop : {len(feuilles) - produit}) et doit etre "
                       f"regenere depuis le script V3, pas corrige a la main."]
            # Analyse d'aide au diagnostic : les 16 premieres / dernieres
            # feuilles donnent-elles les comptages attendus ? (diagnostic
            # seulement, jamais une validation.)
            for etiquette, tranche in (("16 premieres", feuilles[:produit]),
                                       ("16 dernieres", feuilles[-produit:])):
                try:
                    signes = [signe_exact(v) for v in tranche]
                    erreurs.append(f"  diagnostic (non validant) : {etiquette} feuilles "
                                   f"-> pos={signes.count(1)}, zero={signes.count(0)}, "
                                   f"neg={signes.count(-1)}")
                except ValueError:
                    pass
            return [], "legacy", erreurs
        indices = list(itertools.product(*(range(d + 1) for d in degres)))
        normalises = []
        for idx, valeur in zip(indices, feuilles):
            try:
                normalises.append({"index": list(idx), "value": valeur,
                                   "sign": signe_exact(valeur)})
            except ValueError as exc:
                return [], "legacy", [f"valeur legacy {valeur!r} illisible : {exc}"]
        return normalises, "legacy", []
    return [], "inconnu", ["coefficients n'est ni une liste d'objets ni des listes imbriquees"]

def controler(chemin, attendu):
    erreurs = []
    try:
        with open(chemin, encoding="utf-8") as f:
            doc = json.load(f)
    except (OSError, json.JSONDecodeError) as exc:
        return [f"JSON invalide ou illisible : {exc}"], None
    # Schema canonique : les champs GitHub non canoniques ("total", "positifs",
    # "nuls", "negatifs", "base") ne sont pas acceptes comme substituts.
    for champ_interdit in ("total", "positifs", "nuls", "negatifs", "base"):
        if champ_interdit in doc:
            erreurs.append(f"schema non canonique : champ {champ_interdit!r} = {doc.get(champ_interdit)!r} "
                           f"(utiliser count/positive/zero/negative ; pas de champ 'base')")
    for cle in ("name", "variables", "degrees", "count",
                "positive", "zero", "negative", "zero_faces"):
        if doc.get(cle) != attendu[cle]:
            erreurs.append(f"en-tete {cle} : {doc.get(cle)!r} != attendu {attendu[cle]!r}")
    if doc.get("reconstruction_exact") is not True:
        erreurs.append(f"reconstruction_exact : {doc.get('reconstruction_exact')!r} != True")
    coeffs, fmt, err_fmt = normaliser_coefficients(doc.get("coefficients"), attendu["degrees"])
    erreurs += err_fmt
    if fmt == "inconnu":
        return erreurs, None
    degres = attendu["degrees"]
    produit = math.prod(d + 1 for d in degres)
    if attendu["count"] != produit:
        erreurs.append(f"count attendu {attendu['count']} != produit {produit}")
    if len(coeffs) != attendu["count"]:
        erreurs.append(f"nombre de coefficients {len(coeffs)} != count {attendu['count']}")
    if attendu["positive"] + attendu["zero"] + attendu["negative"] != attendu["count"]:
        erreurs.append("positive + zero + negative != count")
    indices, positifs = [], 0
    nuls = negatifs = 0
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
        try:
            signe_reel = signe_exact(valeur)
        except ValueError as exc:
            erreurs.append(f"coefficient {i} (index {idx}) : value illisible {valeur!r} : {exc}")
            continue
        if signe_reel != signe:
            erreurs.append(f"coefficient {i} (index {idx}) : value {valeur!r} "
                           f"de signe exact {signe_reel} != sign declare {signe!r}")
        if (valeur == "0") != (signe == 0):
            erreurs.append(f"coefficient {i} (index {idx}) : value {valeur!r} "
                           f"incoherente avec sign {signe!r}")
        if not isinstance(valeur, str) or not valeur:
            erreurs.append(f"coefficient {i} (index {idx}) : value non valide")
    if (positifs, nuls, negatifs) != (attendu["positive"], attendu["zero"], attendu["negative"]):
        erreurs.append(f"comptages recalcules (pos={positifs}, zero={nuls}, neg={negatifs}) "
                       f"!= en-tete (pos={attendu['positive']}, zero={attendu['zero']}, "
                       f"neg={attendu['negative']})")
    pave = set(itertools.product(*(range(d + 1) for d in degres)))
    if len(indices) != len(set(indices)):
        erreurs.append("indices en double")
    if set(indices) != pave:
        manquants = sorted(pave - set(indices))[:5]
        surplus = sorted(set(indices) - pave)[:5]
        erreurs.append(f"indices incomplets : manquants {manquants}, surplus {surplus}")
    if indices != sorted(indices):
        erreurs.append("coefficients non ranges dans l'ordre lexicographique")
    return erreurs, {"format": fmt, "count": len(coeffs),
                     "positive": positifs, "zero": nuls, "negative": negatifs}

def main():
    dossier = Path(__file__).resolve().parent
    # Le verificateur controle les fichiers du dossier qui le contient.
    # En test, on peut passer un dossier en argument.
    if len(sys.argv) > 1:
        dossier = Path(sys.argv[1])
    total = {"count": 0, "positive": 0, "zero": 0, "negative": 0}
    echec = False
    for nom, attendu in ATTENDU.items():
        erreurs, resume = controler(dossier / nom, attendu)
        if resume is not None:
            for cle in total:
                total[cle] += resume[cle]
        if erreurs:
            echec = True
            print(f"FAIL {nom}")
            for e in erreurs:
                print(f"  - {e}")
        else:
            print(f"PASS {nom} ({resume['count']} coefficients, format {resume['format']})")
    print(f"TOTAL RECALCULE : {total['count']} coefficients, "
          f"{total['positive']} positifs, {total['zero']} nuls, {total['negative']} negatifs "
          f"(attendu {TOTAL_ATTENDU})")
    if total != TOTAL_ATTENDU:
        echec = True
        print("FAIL : total recalcule != total attendu")
    print("VERDICT : " + ("ECHEC" if echec else "TOUT PASSE"))
    return 1 if echec else 0

if __name__ == "__main__":
    raise SystemExit(main())
