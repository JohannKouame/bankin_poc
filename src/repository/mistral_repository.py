import logging
import json

from src.client.mistral import MistralClient, LOGGING_VARIABLE
from src.utils.loader import Loader


class MistralRepository:
    def __init__(self, client: MistralClient) -> None:
        self.client = client
        self.categories = Loader.json_loader("categories_mapping.json")

    def what_is_user_goal(self, message: str) -> dict:
        """
        Analyse le texte utilisateur pour extraire l'objectif financier.
        """
        prompt = f"""Analyse le texte utilisateur et extrais STRICTEMENT les informations suivantes :
        1) categorie_depense (une seule valeur parmi {list(self.categories.keys())})
        2) montant_cible (valeur numérique, peut être un montant ou pourcentage)
        3) horizon (en mois)

        Contraintes :
        - Réponds UNIQUEMENT en JSON valide
        - Si information absente → "unprecised"

        Texte utilisateur :
        {message}
        """

        response = self.client.chat_completion(prompt)
        logging.debug(f"{LOGGING_VARIABLE} what_is_user_goal: {response}")
        return response

    def propose_optimisation_plan(self, user_goal: dict, stats: dict, message: str) -> str:
        """
        Génère un plan ou une analyse synthétique selon les données et l'objectif.
        """
        prompt = f"""
        Tu es un assistant financier. Les données suivantes sont disponibles :
        Stats mensuelles: {json.dumps(stats)}

        Message utilisateur : "{message}"
        Objectif utilisateur : {user_goal}

        Instructions :
        1) Reste concis et synthétique, max 1 ligne par section
        2) Utilise un tableau si nécessaire
        3) Donne un résumé clair avant les détails
        4) Ne pose **aucune question à l'utilisateur**
        5) Ajoute des emojis pour rendre agréable
        6) Traduis les catégories en français
        7) N'excède pas 20 phrases
        """
        response = self.client.chat_completion(prompt)
        logging.debug(f"{LOGGING_VARIABLE} propose_optimisation_plan: {response}")
        return response

    def chat(self, message: str) -> str:
        """
        Répond à tout message utilisateur en adaptant la réponse au type de message.
        """
        # Catégorisation simple
        message_lower = message.lower()
        salutations = ["hello", "hi", "bonjour", "salut"]
        analyse_keywords = ["dépense", "budget", "mois", "catégorie", "augmentent", "réduire"]
        optimisation_keywords = ["économiser", "plan", "objectif", "montant"]

        if any(word in message_lower for word in salutations):
            return "Bonjour ! Que puis-je faire pour toi ?"
        elif any(word in message_lower for word in optimisation_keywords + analyse_keywords):
            # Charger les données pour l'analyse
            monthly_summary = Loader.csv_loader("data/processed/monthly_summary.csv")
            sub_categories_stats = Loader.csv_loader("data/processed/sub_categories_stats.csv")

            monthly_summary_dict = monthly_summary.to_dict(orient='records')
            sub_categories_stats_dict = sub_categories_stats.to_dict(orient='records')

            prompt = f"""
            Tu es un assistant financier intelligent.
            Monthly Summary: {monthly_summary_dict}
            Sub-category Stats: {sub_categories_stats_dict}
            Question utilisateur : {message}

            Instructions :
            - Sois clair et synthétique
            - Utilise tableaux si nécessaire
            - Ne pose **aucune question à l'utilisateur**
            - Traduis les catégories en français
            """
            response = self.client.chat_completion(prompt)
            logging.debug(f"{LOGGING_VARIABLE} chat: {response}")
            return response
        else:
            return "Je n'ai pas compris, peux-tu reformuler ta question ?"
