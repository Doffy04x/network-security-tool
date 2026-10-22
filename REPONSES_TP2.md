# Réponses - TP 2 GitHub Actions

Auteur : Younes Ben Elhoms

## Question 1 : Pourquoi les tests ne dépendent-ils pas de l'ouverture réelle du port 443 ?

`test_valid_port` appelle uniquement `is_valid_port(443)`. Cette fonction vérifie le type et la plage du numéro de port ; elle n'ouvre aucune connexion. `test_invalid_port` vérifie également cette validation. Dans `test_reject_invalid_port`, le port 70000 provoque une exception avant la création du socket dans `check_port`. Les trois tests ne dépendent donc ni d'un service en écoute ni de l'état du réseau. Ils ne vérifient pas encore le résultat d'une connexion TCP réelle.

## Question 2 : Quelle différence entre push et pull_request ?

L'événement `push` déclenche le workflow quand des commits sont publiés sur une branche correspondant au filtre. Ici, il concerne `main` et les branches `feature/**`. L'événement `pull_request` déclenche notamment le workflow à l'ouverture d'une PR, à sa réouverture et lors de nouveaux commits sur sa branche source. Ici, son filtre `branches: [main]` porte sur la branche cible. Le contrôle d'une PR teste par défaut la fusion proposée avec la branche cible. Une même modification peut donc entraîner un run `push` et un run `pull_request`.

## Question 3 : Que se passe-t-il si pytest renvoie un code d'erreur ?

Un code de sortie non nul fait échouer l'étape `Run unit tests`, puis le job `quality-check` et le workflow. Les étapes suivantes, dont Bandit dans ce workflow, sont ignorées par défaut, car elles ne s'exécutent normalement que si les étapes précédentes ont réussi. Les logs identifient le test et l'assertion en échec. Une correction publiée déclenche un nouveau run ; elle ne transforme pas le run échoué en succès.

## Question 4 : Pourquoi est-il utile de bloquer l'intégration d'une PR lorsque les tests échouent ?

Cela évite d'intégrer une régression connue dans la branche principale et de la transmettre aux autres développeurs ou à une livraison. Les contrôles donnent un retour rapide et documenté avant la fusion. Pour rendre ce blocage obligatoire sur un projet réel, il faut configurer une règle de protection ou un ruleset imposant la réussite du contrôle : la simple présence du workflow ne garantit pas à elle seule l'interdiction de fusionner.

## Question 5 : Quelle différence entre le contrôle SAST Bandit et les tests fonctionnels pytest ?

Bandit examine statiquement le code Python pour repérer des constructions associées à des risques de sécurité, sans exécuter le programme ni sonder un port réseau. pytest exécute les tests et compare le comportement observé aux résultats attendus. Ici, les tests couvrent la validation des ports et le rejet d'un port invalide. Ces approches sont complémentaires : un test réussi ne prouve pas l'absence de vulnérabilité et une analyse Bandit sans alerte ne prouve pas que toutes les fonctions sont correctes. Bandit peut également produire des faux positifs ou manquer des problèmes.

## Bonus : Que vérifie compileall et pourquoi ne remplace-t-il ni pytest ni Bandit ?

L'étape `python -m compileall -q network_check.py` compile le fichier en bytecode, sans exécuter sa logique métier. Elle détecte notamment les erreurs de syntaxe et d'indentation. L'option `-q` limite les messages ordinaires. Elle ne vérifie ni les résultats fonctionnels, ni les erreurs qui n'apparaissent qu'à l'exécution, ni les schémas de code dangereux recherchés par Bandit. Elle complète donc les tests et l'analyse statique.
