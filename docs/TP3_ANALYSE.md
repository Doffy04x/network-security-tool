# TP 3 - Docker et Trivy

Le dépôt reste `network-security-tool`, comme demandé pour la suite des TP. L'API réutilise les fonctions de `network_check.py` avec le serveur HTTP de la bibliothèque standard Python. Aucun nouveau projet Flask n'a été créé.

Le dépôt des TP 1 et 2 n'avait pas de Dockerfile ni de fichier Compose. La configuration `audit/before/` est donc la première mise en conteneur du même outil, conservée pour la comparaison. Le fichier `compose.yaml` à la racine contient la version durcie.

## Infrastructure

- NGINX reçoit les requêtes sur `127.0.0.1:8080` et les transmet à l'API.
- L'API écoute sur le port 8000 dans le conteneur et teste uniquement `127.0.0.1`, donc le loopback de son propre conteneur.
- NGINX rejoint frontend et backend. L'API rejoint seulement backend, déclaré `internal: true`.
- Seul le fichier de configuration NGINX est monté depuis l'hôte, en lecture seule. `/tmp` est temporaire en mémoire.
- Les variables règlent les sorties et la génération de bytecode Python ; aucun mot de passe ou token n'est nécessaire. Aucune base de données n'est utilisée.

## Changements appliqués

| Avant | Après | Intérêt |
| --- | --- | --- |
| Image Python Debian complète | Image Python Alpine maintenue, mise à jour lors du build | Réduire les paquets présents et appliquer les correctifs disponibles |
| API exécutée en root | UID/GID 10001 | Réduire les droits de l'application |
| NGINX avec un processus principal root | Image NGINX unprivileged et UID 101 | Fonctionner sans root sur le port 8080 |
| API publiée sur l'hôte | Accès par NGINX uniquement | Supprimer un accès direct inutile |
| API sur frontend et backend | API seulement sur backend interne | Réduire les communications possibles |
| Système de fichiers modifiable et capacités par défaut | `read_only`, `cap_drop: ALL`, `no-new-privileges` | Limiter les modifications et les privilèges |

Les images de base sont fixées par digest et les actions du nouveau workflow par SHA. Les versions vérifiées figurent dans `audit/versions.json`. Les dépendances de développement pytest/Bandit ne sont pas copiées dans l'image ; le service utilise seulement la bibliothèque standard. pip est retiré de l'image finale car il n'est pas nécessaire à l'exécution.

## Reproduction

Le workflow `NetSecure image security` construit les deux images, démarre chaque configuration, teste les communications NGINX/API et les paramètres de sécurité, puis sauvegarde les rapports Trivy JSON. Le contrôle final conserve `--exit-code 1 --severity HIGH,CRITICAL`, sans ignorer les vulnérabilités non corrigées.

Les commandes Docker et Trivy sont exécutées sur le runner GitHub Ubuntu 24.04. L'artefact `tp3-security-reports` contient les sorties Compose, les tests HTTP, les paramètres des conteneurs, les rapports et leur comparaison. Les deux scans utilisent la même base Trivy téléchargée au début du job.

Pour lancer la version durcie avec Docker :

```sh
docker compose up -d --build --wait
docker compose ps
docker compose config
curl http://127.0.0.1:8080/health
curl 'http://127.0.0.1:8080/api/check?port=8000'
trivy image --exit-code 1 --severity HIGH,CRITICAL netsecure-api:lab
docker compose down
```

La comparaison avec la configuration de départ s'exécute avec `docker compose -p tp3-before -f audit/before/compose.yaml up -d --build --wait`. Arrêter une configuration avant de démarrer l'autre car elles utilisent toutes deux le port 8080.

## Documentation consultée

- [Réseaux Docker Compose](https://docs.docker.com/compose/how-tos/networking/)
- [Sécurité Docker](https://docs.docker.com/engine/security/)
- [Action officielle Trivy](https://github.com/aquasecurity/trivy-action)
- [Image NGINX unprivileged](https://github.com/nginx/docker-nginx-unprivileged)

## Résultats du run de référence


Exécution GitHub : https://github.com/Doffy04x/network-security-tool/actions/runs/39955129026
Commit testé : `738fd453b9f6a3cbaeb95f776804883b6cb4254f`.

| Configuration API | HIGH | CRITICAL |
| --- | ---: | ---: |
| Avant : Python Debian complète | 625 | 30 |
| Après : Python Alpine durcie | 0 | 0 |

Ces nombres comptent les résultats paquet/CVE du rapport, pas nécessairement des identifiants CVE tous distincts.

### Trois résultats du scan initial

| Composant | Version installée | Gravité | CVE | Version corrigée disponible |
| --- | --- | --- | --- | --- |
| libaom3 | 3.6.0-1+deb12u3 | CRITICAL | CVE-2023-6879 | Non disponible |
| libglib2.0-0 | 2.74.6-2+deb12u9 | CRITICAL | CVE-2026-58016 | Non disponible |
| libglib2.0-bin | 2.74.6-2+deb12u9 | CRITICAL | CVE-2026-58016 | Non disponible |

Le passage de Debian complète à Alpine change les paquets installés. La baisse du nombre de résultats montre une réduction de la surface analysée ; elle ne signifie pas que chaque CVE de Debian a été corrigée dans le même paquet. Les mises à jour Alpine disponibles ont aussi été appliquées pendant le build.

Le test HTTP passe par NGINX, vérifie un port ouvert dans le conteneur API et contrôle le rejet des paramètres invalides. Les paramètres Docker observés confirment : API UID 10001, NGINX UID 101, fichiers racine en lecture seule, capacités supprimées, backend interne et absence de port API publié. Le service reste fonctionnel après le durcissement.

Le contrôle final Trivy a renvoyé **0** : aucun résultat HIGH ou CRITICAL n’a été détecté dans cette image à cette date avec cette base Trivy. Cela explique le pipeline vert, sans garantir l’absence de tout risque. Les étapes de création de rapports utilisent un code de sortie non bloquant pour conserver la comparaison ; seule la dernière étape applique la politique `--exit-code 1`.

Les résumés et paramètres observés sont conservés dans [docs/tp3](tp3/). Les deux rapports Trivy complets sont dans l’artefact `tp3-security-reports` du run lié ci-dessus et dans le ZIP du rendu.

La base, la version de Trivy et les dates du scan figurent dans `docs/tp3/trivy-version.json`. Un nouveau scan peut donner d’autres résultats si la base ou les dépôts de paquets ont évolué.
