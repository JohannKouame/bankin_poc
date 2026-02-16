# POC Bankin Simulation

Cette application est un **assistant d'analyse de dépenses fictif**, inspiré de Bankin, permettant à un utilisateur de poser des questions sur des transactions simulées et de recevoir des réponses via un LLM (Mistral). L'application est entièrement containerisée avec Docker et utilise **Streamlit** pour l'interface interactive.
[Cliquer ici pour aller vers le dashboard](https://bankinpoc-johannkouame.streamlit.app/)
---

## Table des matières

1. [Présentation](#présentation)
2. [Fonctionnalités](#fonctionnalités)
3. [Prérequis](#prérequis)
4. [Installation et démarrage](#installation-et-démarrage)
5. [Commandes Makefile](#commandes-makefile)
6. [Utilisation](#utilisation)
7. [Développement et tests](#développement-et-tests)

---

## Présentation
Ce PoC vise à illustrer une nouvelle fonctionnalité possible d'ajouter à l'application [Bankin](https://bankin.com/).

Pour créer ce PoC, j'ai utilisé des données open source de [Kaggle](https://www.kaggle.com/)
    [Voir dataset](https://www.kaggle.com/datasets/ismetsemedov/personal-budget-transactions-dataset?resource=download&select=budjet+%282%29.csv).

Ce modèle a été déployé via [Streamlit Cloud Community](https://streamlit.io/cloud)
Pour réaliser ce PoC, j'ai fait appel à mes compétences suivantes :
* **Python** pour développer le système
* **Streamlit** pour le rendu visuel
* **Docker** pour avoir un projet containerisé et facile à déployer
  * Un Dockerfile
  * Un docker-compose
* **API LLM** pour avoir accès à [Mistral](https://mistral.ai/) via l'API
* **Traitement de données** pour pouvoir analyser et mettre en place une logique de traitement de données
* **Programmation et bonnes pratiques** pour avoir un code organiser, segmenter et réutilisable ainsi qu'un repository github clean et clair
* **Git** et **Github** pour versionner et publier mon code
* **Monitoring** en ajoutant des logs afin de tracker le comportement de mon système

### Arborescence

```bash
bankin_poc/
│
├── data/
│   ├── processed/              # Données transformées / features
│   │
│   └── raw/                    # Données brutes (CSV initiaux)
│
├── infra/
│   └── docker/                 # Configuration Docker / infra locale
│       └── python/
│
├── src/
│   ├── client/                 # Clients API externes
│   │   └── mistral.py
│   │
│   ├── command/                # Scripts CLI / exécution
│   │   ├── build_features.py
│   │   ├── download_dataset.py
│   │   └── run_streamlit.py
│   │
│   ├── logger/                 # Configuration logging
│   │   └── logger.py
│   │
│   ├── pages/                  # Composants pages Streamlit
│   │   ├── chat.py
│   │   └── dashboard.py
│   │
│   ├── repository/             # Accès modèles / services
│   │   └── mistral_repository.py
│   │
│   └── utils/                  # Fonctions utilitaires
│       ├── loader.py
│       ├── preprocessing.py
│       └── string_sanitizer.py
│
├── .env.dist                   # Template de variables d’environnement
├── .gitignore
│
├── categories_mapping.json      # Mapping catégories des dépenses
├── docker-compose.yml           # Orchestration des services
├── Makefile
├── prompt_categories.json       # Types de prompts LLM
├── README.md
├── requirements.txt
│
└── streamlit_app.py             # Point d’entrée Streamlit

```
---

## Fonctionnalités

* Visualisation de la conversation entre l’utilisateur et le modèle LLM.
* Messages affichés à la manière des LLM avec des bulles colorées.
* Historique de conversation persistant dans la session Streamlit.
* Aperçu et résumé des données simulées (`monthly_summary.csv` et `sub_categories_stats.csv`) pour donner le contexte à l’utilisateur.
* Logs détaillés de toutes les actions dans le terminal via `logger`.

---

## Prérequis

* [Docker](https://www.docker.com/get-started) >= 20.x
* [Docker Compose](https://docs.docker.com/compose/install/) >= 2.x
* Accès à un LLM (Mistral dans notre cas) et token API 

```dotenv
MISTRAL_TOKEN_API=<votre_token_api>
```

---

## Installation et démarrage

1. **Cloner le projet** :

```bash
git clone <repo_url>
cd <project_folder>
```

2. **Générer le `.env` si nécessaire** :

```bash
cp .env.dist .env
```

3. **Installer les librairies** :

```bash
make install
```

4. **Télécharger le dataset** :

```bash
make download_dataset url="ismetsemedov/personal-budget-transactions-dataset"
```
5. **Preprocess le dataset et créer la knowledge base** :

```bash
make build_features
```

6. **Run l'application streamlit**

```bash
make run_streamlit
```

7. **Accéder à l’interface** :

Ouvrir votre navigateur à l’adresse :
[http://localhost:8501](http://localhost:8501)

* Tous les logs (`logger.info`, `logger.debug`, `logger.error`) s’affichent dans le terminal où la commande est exécutée en fonction du DEBUG_MODE (voir `.env`)

---

## Commandes Makefile

| Commande                          | Description                                                               |
| --------------------------------- | ------------------------------------------------------------------------- |
| `make install`                    | Vérifie le `.env`, construit les images Docker.                           |
| `make sh`                         | Ouvre un shell interactif dans le container Python.                       |
| `make download_dataset url=<url>` | Télécharge le dataset depuis une URL via le script `download_dataset.py`. |
| `make build_features`             | Génère les features à partir du dataset téléchargé.                       |
| `make run_streamlit`              | Lance l’interface Streamlit et expose le port 8501.                       |

---

## Utilisation

1. **Présentation** : 
    L'utilisateur voit un texte lui présentant l'application, son objectif et des exemples de questions à poser 
2. **Aperçu des données** :
   Lors du chargement, l’utilisateur voit un résumé des transactions et sous-catégories fictives.

2. **Interaction avec le LLM** :

    * Écrire votre question dans la barre fixe en bas.
    * Cliquer sur `Envoyer`.
    * Les messages apparaissent en bulles.
    * L’historique est conservé pour cette session.

3. **Exemple de question** :

    * "Quel est le total de mes dépenses pour la catégorie `Loisir` le mois dernier ?"
    * "Quels sont mes postes de dépenses les plus élevés ?"

---

## Développement et tests

* Ajouter de nouvelles fonctionnalités ou modèles dans `repository/` et `client/`.
* Pour tester les scripts Python individuellement :

```bash
docker compose run --rm -e PYTHONPATH=/app python python src/command/build_features.py
```

* Pour debug et inspection interactive :

```bash
docker compose run --rm -e PYTHONPATH=/app python sh
```
