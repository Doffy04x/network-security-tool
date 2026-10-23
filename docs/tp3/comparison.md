# TP 3 - Comparaison Trivy

| Image | HIGH | CRITICAL |
| --- | ---: | ---: |
| before | 625 | 30 |
| after | 0 | 0 |

## before

| Composant | Version | Gravité | CVE | Version corrigée |
| --- | --- | --- | --- | --- |
| libaom3 | 3.6.0-1+deb12u3 | CRITICAL | CVE-2023-6879 | Non disponible |
| libglib2.0-0 | 2.74.6-2+deb12u9 | CRITICAL | CVE-2026-58016 | Non disponible |
| libglib2.0-bin | 2.74.6-2+deb12u9 | CRITICAL | CVE-2026-58016 | Non disponible |

## after

| Composant | Version | Gravité | CVE | Version corrigée |
| --- | --- | --- | --- | --- |
| Aucun résultat HIGH/CRITICAL détecté | - | - | - | - |

Résultats issus des deux rapports JSON Trivy de ce run. Les bases Debian et Alpine contiennent des paquets différents : une entrée absente après changement de base ne prouve pas à elle seule qu'un correctif a été appliqué au même paquet.
