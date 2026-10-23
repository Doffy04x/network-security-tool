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
