# jouerFlux

JouerFlux est une application Flask permettant de gérer des firewalls, leurs politiques de filtrage et les règles associées.
Elle expose une API REST documentée avec Swagger, utilise SQLite comme base de données, et est entièrement conteneurisée avec Docker Compose pour un déploiement simple.

# Prérequis

Avant de commencer, assurez-vous d’avoir installé :
- Docker
- Docker Compose

# Installation

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

# Commandes Makefile utiles:

| Commande            | Description                              |
| ------------------- | ---------------------------------------- |
| `make up`           | Lance l'application avec Docker Compose  |
| `make down`         | Arrête et supprime les conteneurs        |
| `make build`        | Reconstruit l'image Docker               |
| `make show_log`     | Affiche les logs                         |
| `make db_init`      | Initialise la base de données            |
| `make db_migrate`   | Crée une migration de la base de données |
| `make db_upgrade`   | Applique les migrations                  |
| `make db_downgrade` | Annule la dernière migration             |


# Les API

## firewall
    - `GET /firewalls` : Récupère la liste de tous les firewalls
        parametres:
            - name : le nom du firewall
            - page : le numéro de page
            - per_page : la limite de la page
    - `POST /firewalls` : Crée un nouveau firewall
    parametres:
        - name
    - `GET /firewalls/<firewall_id>` : Récupère les détails d'un firewall spécifique
    parametres:
        - firewall_id
    - `DELETE /firewalls/<firewall_id>` : Supprime un firewall

## policy
    - `GET /policies` : Récupère la liste de toutes les politiques
        parametres:
            - name : le nom du policy
            - page : le numéro de page
            - per_page : la limite de la page
    - `POST /policies` : Crée une nouvelle politique
        parametres:
            - name
    - `GET /policies/<policy_id>` : Récupère les détails d'une politique spécifique
        parametres:
            - policy_id
    - `DELETE /policies/<policy_id>` : Supprime une politique

## rules
    - `GET /rules/policy/<policy_id>` : Récupère la liste de toutes les règles d'une politique spécifique
        parametres:
            - policy_id
    - `POST /rules/policy/<policy_id>` : Crée une nouvelle règle pour une politique spécifique
        parametres:
            - action: ALLOW | DENY
            - protocol: TCP | UDP | ICMP | GRE | ESP | AH | ALL
            - source_ip : ipv4 | ipv6
            - destination_ip : ipv4 | ipv6
            - port : int | None (quand le protocol est TCT/UDP, il faut avoir un port, sinon, le port doit etre absent)
    - `DELETE /rules/<rule_id>` : Supprime une règle

## firewall policy
    - `GET /firewall-policy/<firewall_id>/policies` : Récupère la liste des politiques d'un firewall spécifique
    - `POST /firewall-policy/<firewall_id>/policies` : Crée une nouvelle politique pour un firewall spécifique
    - `DELETE /firewall-policy/<firewall_id>/policies/<policy_id>` : Supprime une politique spécifique d'un firewall
