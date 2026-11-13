QXY32_A — XX-M5 V3 — Certificats de Bernstein scindés
Ce dossier contient les 7 certificats de Bernstein de l'audit XX-M5 (V3),
scindés en un fichier JSON par polynôme certifié. Chaque fichier est
autonome : il porte son nom, ses variables, ses degrés, ses comptages,
ses faces d'annulation et la liste complète de ses coefficients.

Source : XX_M5_CONTRE_AUDIT_INDEPENDANT_V3.py — reconstruction indépendante
des 7 polynômes certifiés et recalcul de leurs coefficients de Bernstein
exacts dans Q(sqrt(5)).

Les 7 certificats
Fichier	Polynôme	Variables	Degrés	Coefficients	Positifs	Nuls	Négatifs
XX_M5_V3_Mxx.json	Mxx (diagonale)	X, Y, Z, TT	1, 1, 1, 1	16	13	3	0
XX_M5_V3_Myy.json	Myy (diagonale)	X, Y, Z, TT	1, 1, 1, 1	16	13	3	0
XX_M5_V3_Mzz.json	Mzz (diagonale)	X, Y, Z, TT	1, 1, 1, 1	16	13	3	0
XX_M5_V3_LOWER_Nxy.json	Nxy, carte LOWER	s, q, W, T	4, 2, 2, 2	135	108	27	0
XX_M5_V3_LOWER_DET.json	DET, carte LOWER	s, q, W, T	5, 2, 3, 3	288	216	72	0
XX_M5_V3_UPPER_Nxy.json	Nxy, carte UPPER	s, q, W, T	4, 2, 2, 2	135	123	12	0
XX_M5_V3_UPPER_DET.json	DET, carte UPPER	s, q, W, T	5, 2, 3, 3	288	258	30	0
Total				894	744	150	0
Note de correction (total)
Correction du 13 novembre 2026 : seule la ligne Total du tableau ci-dessus a été
corrigée, 741 → 744 positifs et 153 → 150 nuls. Les sept lignes par fichier
étaient déjà correctes : leur somme donne 13+13+13+108+216+123+258 = 744 positifs
et 3+3+3+27+72+12+30 = 150 nuls, pour 894 coefficients et 0 négatif. L'erreur
était donc une erreur d'addition dans la ligne Total, pas une erreur sur les
coefficients. Aucun coefficient ni résultat mathématique n'a été modifié.

Les totaux corrigés ont été recalculés à partir des fichiers (voir
VERIF_COHERENCE.py et RAPPORT_EXECUTION_TESTS.md), pas recopiés depuis
XX_M5_V3_ENTETE.json : l'en-tête n'est utilisée que comme valeur attendue,
jamais comme preuve.

Format d'un fichier
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
variables : ordre des coordonnées. degrees : degré de Bernstein
dans chaque coordonnée. count = produit des (degré + 1) :
par exemple (5+1)(2+1)(3+1)(3+1) = 288.
coefficients : un objet par multi-indice, dans l'ordre lexicographique
de index. Aucun indice manquant, aucun doublon.
value : expression exacte dans Q(sqrt(5)), sous forme de chaîne
("0", "5", "20 + 12*sqrt(5)", "1579/192 + 1211*sqrt(5)/192", ...).
Aucun flottant.
sign : 1 = coefficient strictement positif, 0 = coefficient nul.
Aucun coefficient négatif dans les 7 fichiers (negative: 0 partout).
reconstruction_exact: true : le polynôme reconstruit depuis ces
coefficients est exactement le polynôme certifié.
zero_faces : faces maximales sur lesquelles le polynôme s'annule.
null = coordonnée libre sur la face, un nombre = coordonnée fixée.
Faces d'annulation
Certificat	Face(s) nulle(s)
Mxx, Myy, Mzz	[0, 0, 0, null] et [1, 1, 1, 1]
LOWER_Nxy, LOWER_DET	[0, null, 0, null]
UPPER_Nxy, UPPER_DET	[1, null, 1, 1]
Lecture : pour LOWER, le polynôme s'annule sur la face s = 0, W = 0
(q et T libres). Pour UPPER, il s'annule sur la face
s = 1, W = 1, T = 1 (q libre). Pour les diagonales, l'annulation a
lieu à l'origine (0, 0, 0, TT libre) et au coin supérieur (1, 1, 1, 1).

Les deux systèmes de variables
Les 3 diagonales (Mxx, Myy, Mzz) sont exprimées en (X, Y, Z, TT).
Les 4 autres certificats sont exprimés en (s, q, W, T).
LOWER et UPPER sont les deux cartes géométriques du domaine ;
chacune porte son mineur Nxy et son déterminant DET.
Contrôles à refaire sur chaque fichier
JSON valide.
count = nombre d'objets dans coefficients = produit des (degré + 1).
positive + zero + negative = count.
Chaque sign cohérent avec value (0 si et seulement si value est "0").
index complets : tous les multi-indices du pavé, sans trou ni doublon.
zero_faces conformes au tableau ci-dessus.
Règle du dossier
Ne jamais écraser ces fichiers. Toute correction se fait dans un nouveau
fichier ou un nouveau dossier horodaté, jamais en place.

Correction des trois diagonales GitHub (fichiers erronés, remplacés)
Les trois fichiers diagonaux publiés sur GitHub étaient erronés et ne
pouvaient pas servir de certificats (voir RAPPORT_CORRECTION_DIAGONALES.md).
Ils sont remplacés ici par des fichiers régénérés depuis les formules
sources du script XX_M5_CONTRE_AUDIT_INDEPENDANT_V3.py (build_certificates),
sans aucune retouche manuelle des valeurs pour « faire correspondre » un
comptage. Les quatre autres certificats sont repris tels quels : ils étaient
déjà corrects et identiques à la régénération depuis les formules sources.

Fichiers GitHub remplacés (ne pas utiliser) :

Fichier	Blob SHA GitHub
XX_M5_V3_SCINDE/XX_M5_V3_Mxx.json	1053c6ec259aee9dd8c38e8fc63763d61a2ceec2
XX_M5_V3_SCINDE/XX_M5_V3_Myy.json	82aa1da09bda5cea16dfd5c43fd893f2360d5f28
XX_M5_V3_SCINDE/XX_M5_V3_Mzz.json	a4d4e1522979f6e06516a0b45628f5433fa54bf9
Totaux après correction (recalculés) : 894 coefficients, 744 positifs,
150 nuls, 0 négatif — inchangés, car les fichiers corrigés ont bien
13 positifs / 3 nuls chacun, comme l'annonçaient déjà les métadonnées
correctes des autres copies.

