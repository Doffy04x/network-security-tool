# TP 3 - Réponses

## Q1. Code source et image Docker

Un scan du code cherche des problèmes dans les fichiers du projet. Un scan d'image examine aussi ce qui sera livré dans le conteneur : système de base, paquets installés et bibliothèques. Un code correct peut donc être livré dans une image contenant des composants vulnérables.

## Q2. Port exposé et port publié

`EXPOSE 8000` dans le Dockerfile indique le port utilisé par l'application ; cela ne crée pas de port sur l'hôte et ne constitue pas un pare-feu. `ports` dans Compose publie un port de l'hôte vers le conteneur. Ici, seul NGINX est publié sur `127.0.0.1:8080`, tandis que l'API reste accessible par le réseau Docker backend.

## Q3. Isoler une base sur backend

Cela évite de rendre la base directement accessible depuis l'extérieur et limite les services qui peuvent la joindre. L'API peut y accéder sans publier son port sur l'hôte. Ce projet ne stocke pas de données : aucune base n'a été ajoutée pour ce TP.

## Q4. Conteneur exécuté en root

Si l'application est compromise, l'attaquant dispose de davantage de droits dans le conteneur et sur les volumes accessibles. Une mauvaise configuration ou une faille du noyau peut aggraver l'impact sur l'hôte. Root dans un conteneur ne signifie toutefois pas automatiquement root sur l'hôte. L'API et NGINX fonctionnent ici avec des utilisateurs non-root.

## Q5. HIGH, CRITICAL, CVE et version corrigée

HIGH et CRITICAL désignent des niveaux de gravité élevés, CRITICAL étant le plus élevé. Une CVE est un identifiant public de vulnérabilité. La version corrigée indique une version du composant qui contient un correctif ; elle peut être absente si aucun correctif n'est publié. Il faut aussi tenir compte du contexte et de l'exposition du service.

## Q6. Utilité de --exit-code 1

Avec le filtre `--severity HIGH,CRITICAL`, cette option fait échouer la commande si Trivy trouve une vulnérabilité de ces niveaux. GitHub Actions marque alors l'étape en échec et les étapes suivantes sont normalement ignorées. Les rapports sont conservés avec `if: always()` pour pouvoir comprendre le résultat. Une erreur technique du scanner doit également être examinée dans les logs.

## Q7. Image sans CVE détectée

Le résultat dépend des composants reconnus, de la base de vulnérabilités et de la date du scan. Une faille récente, un problème de configuration ou un défaut de logique applicative peut ne pas être détecté. Zéro CVE détectée ne signifie donc pas zéro risque.

## Q8. Risques après mise à jour

Il peut rester des défauts du code, des erreurs d'authentification, des ports trop accessibles, des secrets divulgués ou des permissions excessives. Le noyau et le moteur Docker ont aussi leur propre surface d'attaque. Il faut maintenir les images, limiter les privilèges et relancer les contrôles régulièrement.
