# QXY32_A — XX-M5 V3 — Certificats de Bernstein scindés

Ce dossier contient les 7 certificats de Bernstein de l'audit XX-M5 (V3),
scindés en un fichier JSON par polynôme certifié. Chaque fichier est
autonome : il porte son nom, ses variables, ses degrés, ses comptages,
ses faces d'annulation et la liste complète de ses coefficients.

Source : `XX_M5_CONTRE_AUDIT_INDEPENDANT_V3.py` — reconstruction indépendante
des 7 polynômes certifiés et recalcul de leurs coefficients de Bernstein
exacts dans Q(sqrt(5)).

## Les 7 certificats

| Fichier | Polynôme | Variables | Degrés | Coefficients | Positifs | Nuls | Négatifs |
|---|---|---|---|---|---|---|---|
| `XX_M5_V3_Mxx.json` | Mxx (diagonale) | X, Y, Z, TT | 1, 1, 1, 1 | 16 | 13 | 3 | 0 |
| `XX_M5_V3_Myy.json` | Myy (diagonale) | X, Y, Z, TT | 1, 1, 1, 1 | 16 | 13 | 3 | 0 |
| `XX_M5_V3_Mzz.json` | Mzz (diagonale) | X, Y, Z, TT | 1, 1, 1, 1 | 16 | 13 | 3 | 0 |
| `XX_M5_V3_LOWER_Nxy.json` | Nxy, carte LOWER | s, q, W, T | 4, 2, 2, 2 | 135 | 108 | 27 | 0 |
| `XX_M5_V3_LOWER_DET.json` | DET, carte LOWER | s, q, W, T | 5, 2, 3, 3 | 288 | 216 | 72 | 0 |
| `XX_M5_V3_UPPER_Nxy.json` | Nxy, carte UPPER | s, q, W, T | 4, 2, 2, 2 | 135 | 123 | 12 | 0 |
| `XX_M5_V3_UPPER_DET.json` | DET, carte UPPER | s, q, W, T | 5, 2, 3, 3 | 288 | 258 | 30 | 0 |
| **Total** | | | | **894** | **741** | **153** | **0** |

## Format d'un fichier

```json
{
  "name": "LOWER_DET",
  "variables": ["s", "q", "W", "T"],
  "degrees": [5, 2, 3, 3],
  "count": 288,
  "positive": 216,
  "zero": 72,
  "negative": 0,
  "reconstruction_exact": true,
  "zero_faces": [[0, null, 0, null]],
  "coefficients": [
    {"index": [0, 0, 0, 0], "value": "18 + 25*sqrt(5)/2", "sign": 1}
  ]
}
