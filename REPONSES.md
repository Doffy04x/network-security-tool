# Réponses - TP 1 Git et GitHub

## Question 1 : Quelle est la différence entre git add et git commit ?

`git add` sélectionne les modifications et les place dans l'index (zone de préparation) pour le prochain commit. Il ne crée pas de version dans l'historique. `git commit` enregistre un instantané des éléments préparés dans le dépôt local, avec un message, un auteur et un identifiant. Les modifications non ajoutées à l'index ne sont pas incluses dans ce commit.

## Question 2 : Que représente un commit dans Git ?

Un commit représente une version enregistrée du projet à un instant donné. Il contient une référence à l'instantané des fichiers suivis, des métadonnées (auteur, date, message) et une référence à son ou ses commits parents, sauf pour le premier commit. Son identifiant permet de retrouver précisément cette version, de la comparer et de suivre l'évolution du projet. Un commit reste local tant qu'il n'est pas publié avec `git push`.

## Question 3 : Pourquoi créer une branche plutôt que modifier directement la branche principale ?

Une branche permet de développer et de tester une fonctionnalité de façon isolée, tout en gardant une branche principale stable. Plusieurs personnes peuvent ainsi travailler en parallèle. Les changements peuvent être relus avant leur intégration ; si l'essai est abandonné, la branche principale n'est pas affectée. Ici, `feature/custom-port` contient l'ajout du choix du port.

## Question 4 : Quel est le rôle d'une Pull Request dans un projet collaboratif ?

Une Pull Request propose l'intégration des changements d'une branche dans une autre. Elle permet d'examiner les différences, de discuter des modifications, de demander des corrections et de consulter les vérifications automatiques lorsqu'elles sont configurées. Après validation, les changements peuvent être fusionnés dans la branche cible. Elle conserve une trace de la proposition et de sa revue. Dans ce TP, la branche source est `feature/custom-port` et la branche cible est `main`.
