# jouerFlux

JouerFlux est une application Flask permettant de gérer des firewalls, leurs politiques de filtrage et les règles associées.
Elle expose une API REST documentée avec Swagger, utilise SQLite comme base de données, et est entièrement conteneurisée avec Docker Compose pour un déploiement simple.

Prérequis

Avant de commencer, assurez-vous d’avoir installé :
- Docker
- Docker Compose

Installation

1. Clonez le dépôt :
    - git clone https://github.com/yujunjie0603/jouerFlux.git
    - cd jouerflux

2. Construisez et démarrez les conteneurs :
    - make up

3. Initialisez la base de données :
    - make db_init
    - make db_migrate
    - make db_upgrade

4. Accédez à l'application :
    - Ouvrez votre navigateur et allez à l'adresse suivante : http://localhost:5000
    - Swagger UI sera disponible à l'adresse suivante : http://localhost:5000/apidocs

Commandes Makefile utiles:

| Commande            | Description                              |
| ------------------- | ---------------------------------------- |
| `make up`           | Lance l'application avec Docker Compose  |
| `make down`         | Arrête et supprime les conteneurs        |
| `make build`        | Reconstruit l'image Docker               |
| `make logs`         | Affiche les logs                         |
| `make db_init`      | Initialise la base de données            |
| `make db_migrate`   | Crée une migration de la base de données |
| `make db_upgrade`   | Applique les migrations                  |
| `make db_downgrade` | Annule la dernière migration             |

