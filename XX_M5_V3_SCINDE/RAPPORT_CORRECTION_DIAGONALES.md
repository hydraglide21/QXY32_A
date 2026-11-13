Rapport — Correction des trois diagonales GitHub (Mxx, Myy, Mzz)
1. Ce que contiennent les fichiers GitHub (d'après les références fournies)
Fichier	Blob SHA GitHub
XX_M5_V3_SCINDE/XX_M5_V3_Mxx.json	1053c6ec259aee9dd8c38e8fc63763d61a2ceec2
XX_M5_V3_SCINDE/XX_M5_V3_Myy.json	82aa1da09bda5cea16dfd5c43fd893f2360d5f28
XX_M5_V3_SCINDE/XX_M5_V3_Mzz.json	a4d4e1522979f6e06516a0b45628f5433fa54bf9
Dans chacun, d'après les références fournies :

coefficients a la forme 3 × 2 × 2 × 2, donc 24 valeurs scalaires ;
total vaut 16 ;
positifs vaut 13, nuls vaut 3, negatifs vaut 0 ;
dans Mxx, le champ base indique « Bernstein tensorielle, degré (2, 2, 2) » ;
en recomptant les feuilles de Mxx : 8 valeurs positives et 16 zéros,
et non 13 positives et 3 zéros.
2. La contradiction, point par point
Ces fichiers sont incohérents à quatre niveaux à la fois, et chaque
niveau contredit les autres :

(a) Forme contre total. 24 feuilles ≠ 16. Un tenseur de Bernstein
doit satisfaire nombre de feuilles = ∏ (degré_i + 1). La forme
3×2×2×2 correspondrait à des degrés (2,1,1,1) (à permutation près),
jamais à un total de 16.

(b) Degré déclaré contre forme. Le champ base annonce un degré
(2,2,2), c'est-à-dire 3 variables et (2+1)³ = 27 coefficients. Or la
forme a 4 dimensions (3×2×2×2) et 24 feuilles, et la diagonale a
4 variables (X, Y, Z, TT). Le degré (2,2,2) ne correspond ni à la
forme, ni au nombre de variables, ni au total.

(c) Comptages déclarés contre contenu. Les métadonnées annoncent
13 positifs / 3 nuls, mais le recomptage des feuilles donne
8 positifs / 16 zéros. Les métadonnées ne décrivent donc pas le
contenu du fichier.

(d) Contenu contre les formules sources. La diagonale vraie,
recalculée depuis les formules sources (voir §3), donne :

en degré (1,1,1,1) : 16 coefficients, 13 positifs / 3 nuls / 0 négatif ;
en degré élevé (2,1,1,1) : 24 coefficients, 21 positifs / 3 nuls ;
le polynôme F seul (sans le terme de compensation bb·u(a)),
en degré (2,1,1,1) : 24 coefficients, 18 positifs / 3 nuls / 3 négatifs.
Aucune représentation de Bernstein correcte de Mxx ne donne 8/16.
Le contenu GitHub ne représente donc pas Mxx dans aucun degré testé.
3. La représentation correcte, retrouvée depuis les formules sources
Depuis XX_M5_CONTRE_AUDIT_INDEPENDANT_V3.py :

Mxx = diagonal(2X, 2Y, 2Z, KC·TT), avec diagonal(a,b,c,kk) = F(a,b,c,kk) + bb·u(a),
u(a) = a(2-a), bb = (PHI+kk)/2.
Le polynôme développé a 5 monômes et degree_list = (1,1,1,1) :
le terme en a² de F se compense exactement avec bb·u(a).
La base de Bernstein tensorielle correcte est donc le degré (1,1,1,1),
soit 16 coefficients, un par multi-indice (i,j,k,l) ∈ {0,1}⁴.
Reconstruction vérifiée : Σ b_i·B_i(X,Y,Z,TT) = Mxx exactement
(reconstruction_exact: true, recalculé par le script V3).
Les fichiers corrigés de ce dossier sont la sortie de
build_certificates() du script V3, sans retouche manuelle :
aucune valeur n'a été modifiée pour faire correspondre un comptage.
Ils sont d'ailleurs identiques, octet pour octet (à la mise en forme
près), aux certificats déjà calculés dans les autres copies.

4. Signes exacts et faces nulles recalculés
Pour chaque diagonale, signes recalculés depuis les value elles-mêmes
(parseur exact dans Q(√5), sans flottant) :

Fichier	Coefficients	Positifs	Nuls	Négatifs	Faces nulles
Mxx	16	13	3	0	[0,0,0,null], [1,1,1,1]
Myy	16	13	3	0	[0,0,0,null], [1,1,1,1]
Mzz	16	13	3	0	[0,0,0,null], [1,1,1,1]
Les 3 nuls sont exactement les indices [0,0,0,0], [0,0,0,1]
(face origine) et [1,1,1,1] (coin supérieur) — cohérent avec
« matrice nulle à l'origine et au coin supérieur » du script V3.
Les 13 autres coefficients sont strictement positifs, vérifiés un par un.
Les 7 valeurs distinctes par diagonale sont :
0, 1 + sqrt(5), 2*sqrt(5), 1 + 3*sqrt(5), sqrt(5),
2 + 2*sqrt(5), 2 + 4*sqrt(5).

Totaux des 7 certificats après correction : 894 = 744 + 150 + 0.

5. Fichiers erronés ou représentation mal exportée ? — verdict
Verdict : fichiers erronés en tant que certificats, et l'erreur
provient de l'export, pas des mathématiques. Les formules sources
(script V3) sont correctes et régénèrent les bons certificats ;
c'est la version publiée sur GitHub qui est fausse (mauvais schéma :
champs total/positifs/nuls/negatifs/base au lieu de
count/positive/zero/negative ; mauvaise forme 3×2×2×2 ;
mauvais degré (2,2,2) ; contenu qui ne correspond à aucune
représentation correcte du polynôme).

Le mécanisme précis de l'export fautif ne peut pas être certifié
sans le code de l'exporteur : il n'est donc pas affirmé ici.
Ce qui est établi, c'est que le contenu ne peut pas être « réparé »
en devinant une convention (par exemple en supprimant 8 feuilles) :
toute « réparation » à la main serait arbitraire. La seule correction
valide est la régénération depuis les formules sources, qui est ce
que contient ce dossier.

Conduite à tenir : ne pas utiliser les trois blobs GitHub ci-dessus.
Remplacer les trois fichiers GitHub par les fichiers corrigés de ce
dossier, et ne jamais corriger un certificat à la main.

6. Ce qui n'a pas été refait
Les calculs XX-M5 V3 n'ont pas été modifiés : les fichiers corrigés
sont une régénération, pas une retouche.
La reconstruction polynomiale est recalculée par le script V3
(reconstruction_exact), mais la dérivation des formules sources
elles-mêmes n'est pas re-validée ici.
Ce rapport ne valide pas le théorème global : il valide la
cohérence des 7 certificats.
