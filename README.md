# Network Security Tool

A simple Python project for network security students.

Author: Younes Ben Elhoms

## Utilisation

Prérequis : Python 3 et Git. Aucune bibliothèque externe n'est nécessaire.

```sh
python network_check.py
```

Saisir un numéro de port TCP entier entre 1 et 65535. Le programme teste uniquement `127.0.0.1`, avec un délai de deux secondes. Il affiche `Port is open` si une connexion TCP réussit, sinon `Port is closed or unreachable`.

Ce script pédagogique reprend le code demandé dans le TP : la saisie doit être un entier valide. Il ne distingue pas un port fermé d'un port filtré ou inaccessible.

## Réponses et vérification

- [Réponses aux quatre questions](REPONSES.md)
- [Résultats des tests locaux](VERIFICATION.md)

La branche `feature/custom-port` introduit la saisie du port.
