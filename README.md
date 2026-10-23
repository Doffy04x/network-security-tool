# Network Security Tool

A simple Python project for network security students.

Author: Younes Ben Elhoms

## Utilisation

Prérequis : Python 3 et Git. Le script utilise uniquement la bibliothèque standard ; les outils de développement sont listés dans `requirements-dev.txt`.

```sh
python network_check.py
```

Saisir un numéro de port TCP entier entre 1 et 65535. Le point d'entrée teste uniquement `127.0.0.1`, avec un délai de deux secondes. Il affiche `Open` si une connexion TCP réussit, sinon `Closed`. La fonction `check_port(host, port, timeout=2)` est destinée aux usages autorisés ; dans ces TP, utiliser uniquement `127.0.0.1`.

Ce script pédagogique reprend le code demandé dans le TP 2 : une valeur hors plage est rejetée par `ValueError`, et la saisie doit être un entier. Il ne distingue pas un port fermé d'un port filtré ou inaccessible.

## Réponses et vérification

- [Réponses aux quatre questions du TP 1](REPONSES.md)
- [Résultats des tests locaux du TP 1](VERIFICATION.md)
- [Réponses aux cinq questions et au bonus du TP 2](REPONSES_TP2.md)

La branche `feature/custom-port` introduit la saisie du port.

## TP 2 : intégration continue et sécurité

```sh
python -m pip install -r requirements-dev.txt
python -m compileall -q network_check.py
python -m pytest -v
python -m bandit -r network_check.py
```

Le workflow [Python CI and Security](.github/workflows/ci.yml) s'exécute sur les pushes vers `main` et `feature/**`, et sur les PR ciblant `main`. Il utilise Ubuntu, Python 3.12 et la permission `contents: read`. Les trois tests unitaires n'effectuent aucune connexion réseau.

La branche `feature/ci-pipeline` conserve les commits de création du pipeline, de démonstration d'un test volontairement faux et de sa correction.

## TP 3 : Docker et Trivy

Le même outil est accessible derrière NGINX, avec une API Python sans Flask. Le Dockerfile et `compose.yaml` à la racine contiennent la configuration durcie.

```sh
docker compose up -d --build --wait
curl http://127.0.0.1:8080/health
curl 'http://127.0.0.1:8080/api/check?port=8000'
docker compose down
```

Le contrôle de port concerne le loopback du conteneur API. Seul NGINX est publié sur l'hôte, sur `127.0.0.1:8080`.

- [Analyse et commandes du TP 3](docs/TP3_ANALYSE.md)
- [Réponses aux huit questions](REPONSES_TP3.md)
- [Workflow Docker et Trivy](.github/workflows/security-scan.yml)

Les builds, les tests Compose et les scans avant/après s'exécutent dans GitHub Actions ; Docker n'est pas nécessaire sur le poste pour consulter les résultats. La première configuration se trouve dans `audit/before/` pour reproduire la comparaison.
