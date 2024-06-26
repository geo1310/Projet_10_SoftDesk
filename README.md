![image](./docs/images/SoftDesk_banniere.png)
# SoftDesk Support

![Python](https://img.shields.io/badge/python-3.11.x-green.svg)
![Django](https://img.shields.io/badge/django-5.0.3-green.svg)
![DjangoRestFramework](https://img.shields.io/badge/djangoRestFramework-3.12.4-green.svg)
![Swagger Icon](https://img.shields.io/badge/swagger_DRF-1.21.7-green.svg)
![Poetry](https://img.shields.io/badge/Poetry-1.8.2-green.svg)

[![PEP8](https://img.shields.io/badge/code%20style-pep8-orange.svg)](https://www.python.org/dev/peps/pep-0008/)
[![Flake8](https://img.shields.io/badge/flake8-checked-blueviolet)](https://flake8.pycqa.org/en/latest/)
[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

![Repo Size](https://img.shields.io/github/repo-size/geo1310/projet_10_SoftDesk)
![GitHub commit activity](https://img.shields.io/github/commit-activity/m/geo1310/projet_10_SoftDesk)

SoftDesk, une société d'édition de logiciels de collaboration, a décidé de publier une application permettant de remonter et suivre des problèmes techniques. Cette solution, SoftDesk Support, s’adresse à des entreprises en B2B (Business to Business). 

Développement d'une API RESTful

## Documents du Projet


1. __[Conception de la mise en œuvre](docs/Softdesk+-+Conception+de+la+mise+en+œuvre.pdf)__

    Contenant :
    * les modèles d'objets ; 
    * les principales fonctionnalités de l’application ; 
    * une liste des points de terminaison d'API requis et un exemple de réponse. 

2. __[Exigences de sécurité et d'optimisation](docs/Softdesk+-+Exigences+de+sécurité+et+d'optimisation.pdf)__

    Contenant :
    * Les spécifications OWASP répertorient les mesures de sécurité OWASP que le back-end doit respecter. L’API devra authentifier les utilisateurs à l’aide de Json Web Token (JWT) et définir des permissions d’accès aux ressources par groupe d’utilisateurs ;
    * Les spécifications RGPD appliquent les règles de protection de la donnée et la confidentialité de chaque utilisateur. L’API devra s’assurer que les utilisateurs puissent protéger leurs données et spécifier s’ils souhaitent ou non être contactés via un champ de formulaire spécifique ;
    * Les spécifications green code répertorient les mesures de conceptions « green », qui permettent d’optimiser et de simplifier le code, dans un but de sobriété énergétique. L’API devra tendre vers une utilisation optimisée des requêtes pour éviter la surconsommation des serveurs.


## Installation et activation de l'environnement Virtuel et des dépendances
Création de l'envireonnement virtuel : 
```bash
python -m venv .env-projet10-softdesk
```
Activation de l'environnement virtuel se placer dans le dossier **.env-projet10-softdesk/scripts** et taper : 
```bash
./activate
```
Installation des dependances necessaires au projet avec poetry : 
```bash
pip install poetry
poetry install

```
## Usage

* Le projet est fourni avec une base de données exemple avec 3 utilisateurs :
    * __Id :__ 19 __name :__ user1 __password :__ user1-pass
    * __Id :__ 20 __name :__ user2 __password :__ user2-pass
    * __Id :__ 21 __name :__ user3 __password :__ user3-pass
* Un super utilsateur : 
    *  __Id :__ 18 __name :__ superuser1 __password :__ softdesk

Se placer dans le dossier du projet Softdesk_API et exécuter la commande suivante pour lancer le serveur de développement :

```bash
python manage.py runserver
```
Le serveur de développement démarre à l'adresse http://127.0.0.1:8000/ et est redirigé vers le Swagger de l'API.
Toute la documentation de l'API se trouve sur le swagger ainsi que tous les Endpoints et les Modèles.

![image](./docs/images/API_SoftDesk_Support_Swagger.png)

## Vérification du Code : 

* Le code a été formaté et vérifié avec `black` et il respecte les recommandations pep8.

* Utilisation de `isort` pour l'organisation des imports et de `pycln` pour le pep8.

---
#### Procédure pour générer un rapport flake8 en HTML


Dans le terminal dans le dossier du projet , tapez la commande suivante pour afficher la politique d'exécution actuelle :
```
flake8 --format=html --htmldir=rapports_flake8 --exclude=.env-projet10-softdesk
```
Le rapport sera sauvegardé dans le dossier rapports_flake8, il suffira de lancer le fichier index.html

## Contribuer

Si vous souhaitez contribuer à ce projet, veuillez suivre ces étapes :

    Ouvrez un problème pour discuter de ce que vous souhaitez changer.
    Fork ce dépôt et créez une branche pour votre contribution.
    Soumettez une demande d'extraction avec vos modifications.
