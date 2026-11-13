
# QXY32_A — Démonstration du théorème : M PSD et dégénérescences exactes

Contre-expertise indépendante. Le théorème démontré ici :

> Pour `(x, y, z) ∈ [0,2]³` et `k ∈ [0, KC]`, avec `R = √5`, `PHI = (1+R)/2`,
> `KC = (1+2R)/4`, `B(k) = (PHI+k)/2`,
> `F(a,b,c;k) = a·(R − B(k)(2−a)) + (PHI − k·a)(b+c)`, `u(a) = a(2−a)`,
> `h = (√u(x), √u(y), √u(z))ᵀ` et `M = diag(Fx, Fy, Fz) + B(k)·h·hᵀ` :
>
> **M est positive semidéfinie (PSD) sur tout le domaine, et M = 0 si et
> seulement si `(x,y,z) = (0,0,0)` pour tout `k`, ou `(x,y,z) = (2,2,2)` avec
> `k = KC`.**

## Exécution

```bash
python3 QXY32_A_CERTIFICAT_MAITRE_THEOREME.py
