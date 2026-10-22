# Vérification - TP 1 Git et GitHub

Exécution réelle le 22 octobre 2026, uniquement sur `127.0.0.1`.

## Version initiale

Port 80 : `Port is closed or unreachable`

## Ports demandés dans le TP

| Port TCP | Résultat observé |
| --- | --- |
| 80 | Port is closed or unreachable |
| 443 | Port is closed or unreachable |
| 8080 | Port is closed or unreachable |

Les résultats dépendent des services locaux actifs au moment du test.

## Contrôle des deux résultats possibles

- Écoute TCP temporaire sur le port local 53600 : `Enter port number: Port is open`.
- Socket local lié mais sans écoute sur le port 53602 : `Enter port number: Port is closed or unreachable`.
- Les sockets de contrôle ont été fermés à la fin des tests.

Aucune machine distante et aucun service externe n’ont été testés.
