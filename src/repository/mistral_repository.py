import logging
from unicodedata import category

from src.client.mistral import MistralClient, LOGGING_VARIABLE
from src.utils.string_sanitizer import StringSanitizer
from src.utils.loader import Loader
import json


class MistralRepository:
    def __init__(self, client: MistralClient) -> None:
        self.client = client
        self.categories = Loader.json_loader("categories_mapping.json")

    def clean_message(self, message) -> str:
        # Clean message
        cleaned_message = StringSanitizer.remove_html_tags(message)
        cleaned_message = StringSanitizer.remove_lines_break(cleaned_message)
        return cleaned_message

    def what_is_user_goal(self, message: str) -> dict:
        cleaned_message = self.clean_message(message)

        categories = Loader.json_loader("categories_mapping.yml")

        prompt = (f"""Analyse le texte utilisateur et extrais STRICTEMENT les informations suivantes :
                    1) categorie_depense  
                       - Doit être UNE SEULE valeur parmi :
                         {self.categories.keys()}
                    
                    2) montant_cible  
                       - Valeur numérique uniquement
                       - Sans devise
                       - Peut être :
                            • un montant explicite (ex: 600)
                            • un pourcentage (ex: +20 ou -15)
                    
                    3) horizon  
                       - Durée normalisée en mois, ne mentionne pas le mot "mois" (ex: 3, 6, 14)
                    
                    Contraintes importantes :
                    
                    - Réponds UNIQUEMENT en JSON valide
                    - Aucun texte hors JSON
                    - Aucune devise
                    - Aucune explication
                    - Si une information est absente → utiliser "unprecised"
                    
                    Texte utilisateur :
                    {cleaned_message}
                    """
                  )

        response = self.client.chat_completion(prompt)
        #json_response = StringSanitizer.remove_json_tags(response)
        logging.info(f'{LOGGING_VARIABLE} {response}')
        return response

    def propose_optimisation_plan(self, user_goal: dict, stats: dict, message: str) -> str:
        cleaned_message = self.clean_message(message)
        prompt = (f"""
                    Le JSON suivant contient un résumé des dépenses de l'utilisateur sur les derniers mois :
                    {json.dumps(stats)}
                    L'utilisateur souhaite atteindre l'objectif suivant :
                        - Categorie ciblée hors utilisateur : {self.categories.keys()}
                        - Catégories ciblée par l'utilisateur : {user_goal["categories"]}
                        - Montant cible : {user_goal["target_amount"]}
                        - Horizon : {user_goal["duration"]}
                    En utilisant les informations du JSON, propose **3 plans distincts** qui permettraient à l'utilisateur d'atteindre cet objectif.
                    Chaque plan doit inclure :
                    1. Les catégories ciblées
                    2. Le montant à économiser par catégorie (en euros)
                    3. Une brève justification basée sur les habitudes de dépense (opérations fréquentes, montant moyen, volatilité)
                    4. Horizon (en fonction de l'horizon souhaitée par l'utilisateur)
                    N'oublie pas de traduire les catégories en français"""

                  )

        response = self.client.chat_completion(prompt)
        logging.info(f'{LOGGING_VARIABLE} {response}')
        return response

    def chat(self, message: str) -> str:
        # --- Charger les données ---
        monthly_summary = Loader.csv_loader("data/processed/monthly_summary.csv")
        sub_categories_stats = Loader.csv_loader("data/processed/sub_categories_stats.csv")

        logging.debug(f"{LOGGING_VARIABLE} Aperçu de monthly_summary:\n{monthly_summary.head()}")
        logging.debug(f"{LOGGING_VARIABLE} Aperçu de sub_categories_stats:\n{sub_categories_stats.head()}")

        # --- Convertir en dictionnaire pour faciliter l’inclusion dans le prompt ---
        monthly_summary_dict = monthly_summary.to_dict(orient='records')
        sub_categories_stats_dict = sub_categories_stats.to_dict(orient='records')

        # --- Construire le prompt contextuel ---
        prompt = f"""
            Tu es un assistant financier. Tu disposes des données suivantes pour l'utilisateur :
            
            Monthly Summary:
            {monthly_summary_dict}
            
            Sub-category Statistics:
            {sub_categories_stats_dict}
            
            Réponds à l'utilisateur de façon claire et précise en tenant compte de ces données.
            
            Question de l'utilisateur : {message}
            """

        logging.debug(f"{LOGGING_VARIABLE} Prompt envoyé au modèle:\n{prompt}")

        # --- Appel au modèle ---
        response = self.client.chat_completion(prompt)

        logging.info(f"{LOGGING_VARIABLE} Réponse du modèle:\n{response}")
        return response