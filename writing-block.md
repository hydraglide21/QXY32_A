# QXY32_A — Théorème de positivité globale

## Présentation

Ce dépôt rassemble l'énoncé mathématique, les calculs exacts et les scripts de vérification du théorème de positivité globale de la matrice spectrale \(M(x,y,z,k)\).

L'objectif est d'établir :

\[
\boxed{M(x,y,z,k)\succeq 0}
\]

sur le domaine :

\[
(x,y,z,k)\in[0,2]^3\times[0,k_c],
\qquad
k_c=\frac{1+2\sqrt5}{4}.
\]

Les calculs de signe sont effectués exactement dans le corps :

\[
\mathbb Q(\sqrt5),
\]

sans utiliser d'approximation flottante comme justification d'un signe.

## Structure mathématique

On pose :

\[
r=\sqrt5,\qquad
\phi=\frac{1+\sqrt5}{2},
\qquad
B=\frac{\phi+k}{2}.
\]

La fonction fondamentale est :

\[
F(a,b,c;k)
=
a\bigl(r-B(2-a)\bigr)
+
(\phi-ka)(b+c).
\]

On définit :

\[
F_x=F(x,y,z;k),\quad
F_y=F(y,x,z;k),\quad
F_z=F(z,x,y;k),
\]

et :

\[
u(a)=a(2-a),\qquad
s=(\sqrt{u(x)},\sqrt{u(y)},\sqrt{u(z)})^T.
\]

La matrice étudiée est :

\[
M=\operatorname{diag}(F_x,F_y,F_z)+Bss^T.
\]

## Résultat annoncé

Le certificat XX-M établit une preuve exacte de positivité semi-définie par réduction aux mineurs principaux, identités de permutation et certificats de Bernstein.

Les deux configurations où la matrice est nulle sont :

\[
Z_0=(0,0,0,k),\qquad 0\leq k\leq k_c,
\]

et :

\[
Z_1=(2,2,2,k_c).
\]

En dehors de ces configurations, le certificat conclut à la positivité définie.

## Script principal de vérification

Fichier :

`QXY32_A_AUDIT_INDEPENDANT_XX_M.py`

Ce script réalise notamment :

- la vérification de l'identité du déterminant de rang un ;
- la reconstruction exacte des mineurs principaux ;
- les contrôles des identités de permutation ;
- les certificats de Bernstein LOWER et UPPER ;
- l'analyse des faces où le déterminant s'annule ;
- le contrôle des deux matrices nulles ;
- le bilan des coefficients du certificat réduit.

## Installation et exécution

Prérequis : Python 3 et SymPy.

Installation de SymPy :

```bash
python -m pip install sympy
```

Exécution :

```bash
python QXY32_A_AUDIT_INDEPENDANT_XX_M.py
```

Le script affiche un rapport JSON contenant les contrôles, les certificats, les réserves et la conclusion.

Conclusion attendue :

```text
PASS_INDEPENDENT_EXACT_PERMUTATION_REDUCED_CERTIFICATE
```

Cette chaîne est la conclusion attendue de l'exécution ; elle ne remplace pas la conservation de la sortie effective obtenue lors de chaque exécution.

## Bilan du certificat XX-M

| Famille | Coefficients | Positifs | Nuls | Négatifs |
|---|---:|---:|---:|---:|
| Diagonales Mxx, Myy, Mzz | 48 | 39 | 9 | 0 |
| Nxy LOWER et UPPER | 270 | 231 | 39 | 0 |
| Déterminant LOWER et UPPER | 576 | 474 | 102 | 0 |
| **Total réduit** | **894** | **744** | **150** | **0** |

Les mineurs \(N_{xz}\) et \(N_{yz}\) sont couverts par les identités exactes de permutation à partir du représentant \(N_{xy}\).

## Tableau des statuts de vérification

| Élément | Statut | Précision |
|---|---|---|
| Identité du déterminant de rang un | Démontré dans XX-M | Reconstruction symbolique exacte |
| Invariance du déterminant par permutation | Démontré dans XX-M | Six permutations |
| Symétrie de Nxy | Démontré dans XX-M | Identité exacte |
| Transport de Nxz et Nyz | Démontré dans XX-M | Identités exactes |
| Diagonales | Certifié dans XX-M | Bernstein exact |
| Nxy LOWER et UPPER | Certifié dans XX-M | Bernstein exact |
| Déterminant LOWER et UPPER | Certifié dans XX-M | Bernstein exact |
| Deux configurations de matrice nulle | Vérifié dans XX-M | Entrées reconstruites exactement |
| Nxz LOWER en certificat direct | Réserve documentée | Un coefficient Bernstein négatif dans le chart fixe ; ce certificat n'est pas utilisé dans la preuve réduite |
| Sources physiques historiques XIX/XX | Non reproduites intégralement par XX-M | Reconstruction indépendante à partir des définitions |
| Hachages des sources historiques | Non recalculés par XX-M | À distinguer des résultats historiques rapportés |

## Réserve méthodologique importante

Un coefficient Bernstein négatif dans une représentation donnée ne démontre pas que le polynôme prend une valeur négative sur le domaine.

Le diagnostic LOWER de \(N_{xz}\) est conservé explicitement. Il n'est pas utilisé dans la démonstration réduite, qui repose sur les identités exactes de permutation et le certificat de \(N_{xy}\).

Les résultats historiques des scripts XIX et XX ne doivent pas être présentés comme ayant tous été réexécutés par XX-M.

## Reproductibilité et traçabilité

Chaque nouvelle vérification doit conserver :

1. le script exact exécuté ;
2. la sortie brute ;
3. la date et l'environnement d'exécution ;
4. le résultat des contrôles ;
5. le SHA-256 des fichiers effectivement présents ;
6. les éventuelles anomalies et corrections.

Les versions historiques doivent être conservées. Toute évolution doit être publiée sous un nouveau nom de fichier ou une nouvelle version.

## Fichiers du dépôt

Organisation recommandée :

```text
QXY32_A/
│
├── README.md
│
├── THEOREME/
│   └── QXY32_A_THEOREME.md
│
├── AUDITS/
│   └── QXY32_A_AUDIT_INDEPENDANT_XX_M.py
│
└── RAPPORTS/
    └── sorties_et_rapports_de_verification/
```

Les répertoires et rapports complémentaires seront ajoutés au fur et à mesure de leur création effective.

## Conclusion

Le dossier XX-M fournit une reconstruction indépendante et exacte du certificat réduit de positivité globale, avec 894 coefficients Bernstein recensés et aucune valeur négative dans les certificats utilisés.

Le présent README décrit le périmètre effectivement vérifié et conserve les réserves de provenance et de reproductibilité.

**Projet : QXY32_A**  
**Audit de référence : XX-M**  
**Corps de calcul : \(\mathbb Q(\sqrt5)\)**  
**Méthode : identités algébriques exactes et certificats de Bernstein**