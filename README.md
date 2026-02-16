# POC Bankin Simulation

Cette application est un **assistant d'analyse de dépenses fictif**, inspiré de Bankin, permettant à un utilisateur de poser des questions sur des transactions simulées et de recevoir des réponses via un LLM (Mistral). L'application est entièrement containerisée avec Docker et utilise **Streamlit** pour l'interface interactive.

---

## Table des matières

1. [Fonctionnalités](#fonctionnalités)
2. [Prérequis](#prérequis)
3. [Installation et démarrage](#installation-et-démarrage)
4. [Commandes Makefile](#commandes-makefile)
5. [Utilisation](#utilisation)
6. [Logger](#logger)
7. [Développement et tests](#développement-et-tests)

---

## Fonctionnalités

* Visualisation de la conversation entre l’utilisateur et le modèle LLM.
* Messages affichés à la manière de ChatGPT : utilisateur à droite, modèle à gauche, bulles colorées.
* Historique de conversation persistant dans la session Streamlit.
* Aperçu et résumé des données simulées (`monthly_summary.csv` et `sub_categories_stats.csv`) pour donner le contexte à l’utilisateur.
* Logs détaillés de toutes les actions dans le terminal via `logger`.

---

## Prérequis

* [Docker](https://www.docker.com/get-started) >= 20.x
* [Docker Compose](https://docs.docker.com/compose/install/) >= 2.x
* Accès à un LLM (Mistral dans notre cas) et token API dans `.env` :

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

5. **Run l'application streamlit**

```bash
make streamlit
```

6. **Accéder à l’interface** :

Ouvrir votre navigateur à l’adresse :
[http://localhost:8501](http://localhost:8501)

* Tous les logs (`logger.info`, `logger.debug`, `logger.error`) s’affichent dans le terminal où la commande est exécutée.

---

## Commandes Makefile

| Commande                          | Description                                                               |
| --------------------------------- | ------------------------------------------------------------------------- |
| `make install`                    | Vérifie le `.env`, construit les images Docker.                           |
| `make sh`                         | Ouvre un shell interactif dans le container Python.                       |
| `make download_dataset url=<url>` | Télécharge le dataset depuis une URL via le script `download_dataset.py`. |
| `make build_features`             | Génère les features à partir du dataset téléchargé.                       |
| `make run_streamlit`              | Lance l’interface Streamlit et expose le port 8501.                       |

**Remarque :** La commande `run_streamlit` utilise désormais `docker compose up streamlit` pour exposer correctement le port et permettre la visualisation de l’application.

---

## Utilisation

1. **Aperçu des données** :
   Lors du chargement, l’utilisateur voit un résumé des transactions et sous-catégories fictives.

2. **Interaction avec le LLM** :

    * Écrire votre question dans la barre fixe en bas.
    * Cliquer sur `Envoyer`.
    * Les messages apparaissent en bulles (utilisateur à droite, modèle à gauche).
    * L’historique est conservé pour cette session.

3. **Exemple de question** :

    * "Quel est le total de mes dépenses pour la catégorie `Alimentation` ce mois-ci ?"
    * "Quels sont mes postes de dépenses les plus élevés ?"

---

## Logger

* Tous les événements importants sont loggés dans le terminal.
* Configuration dans `src/logger/logger.py` :

```python
import logging

logger = logging.getLogger("bankin_llm")
logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

logger.info("Démarrage de l'application Streamlit")
```

* Les logs incluent : démarrage de l’application, requêtes utilisateur, réponses du modèle, erreurs éventuelles.

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
