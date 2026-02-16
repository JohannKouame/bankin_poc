import logging
import json

from src.client.mistral import MistralClient, LOGGING_VARIABLE
from src.utils.loader import Loader


class MistralRepository:
    def __init__(self, client: MistralClient) -> None:
        self.client = client
        self.budget_categories = Loader.json_loader("categories_mapping.json")
        self.prompt_categories = Loader.json_loader("prompt_categories.json")

    def detect_user_prompt_category(self, message: str) -> str:
        """
        Determine user prompt's type
        """
        prompt = f"""Analyse le texte de l'utilisateur. L'objectif est de détecter de quel 
                    type est ce prompt parmi les suivants:
                    {self.prompt_categories}
                    Répond avec uniquement la catégorie du prompt, pas le descriptif.
                    Un prompt ne peut avoir qu'une seule catégorie. Si le prompt est ambigüe, 
                    réponds avec la catégorie la plus proche 
            
                    Texte utilisateur :
                    {message}
                    """

        response = self.client.chat_completion(prompt)
        logging.debug(f"{LOGGING_VARIABLE} detecte_user_prompt_category: {response}")
        return response

    def detect_target_category(self, message) -> str:
        """
        Detect categories to focus one for achieve user goal
        :param message: str
                user message

        :return:
            model answer
        """
        prompt = f"""Analyse le texte utilisateur et extrais STRICTEMENT les informations suivantes :
                        1) categoru : UNE SEULE valeur parmi {self.budget_categories.keys()}
                        2) target_amount : valeur numérique uniquement, peut être explicite (ex: 600) ou % (ex: +20, -15)
                        3) duration : durée en mois, sans mentionner "mois"
                        Contraintes :
                        - Réponds UNIQUEMENT en JSON valide
                        - Aucun texte hors JSON
                        - Aucune devise
                        - Si info absente → "unspecified"
                        Texte utilisateur : {message}
                     """
        response = self.client.chat_completion(prompt)
        logging.info(f'{LOGGING_VARIABLE} {response}')
        return response

    def propose_optimisation_plan(self, message: str, stats: dict, stream: bool = True) -> str:
        """
        Propose an optimization plan to user
        :param message:
            user prompt
        :param stats: dict
            contain user transactions
        :param stream: bool
            'True' to make model answer on stream
            'False' to wait until model complete treatment before displaying answer

        :return:
            model answer
        """
        prompt = f"""
                Tu es un assistant financier. Données disponibles :
                Stats mensuelles: {json.dumps(stats)}
                Message utilisateur : "{message}"
                Instructions :
                1) Reste concis et synthétique. Ne mentionne pas toutes les catégories. 
                    Identifie les plus simple à optimiser (maximum 2 catégories)
                2) Utilise un tableau si nécessaire
                3) Donne un résumé clair avant les détails
                4) Ne pose aucune question
                5) Ajoute des emojis
                6) Traduis les catégories en français
                7) N'excède pas 20 phrases
                
                Répond uniquement avec le texte de réponse. Aucun décorateur ni élément autour 
                de la réponse comme "réponse" ou "voici la réponse"
                """

        if stream:
            response = self.client.chat_completion(prompt)
        else:
            response = self.client.chat_completion_stream(prompt)
        logging.debug(f"{LOGGING_VARIABLE} propose_optimisation_plan: {response}")

        return response

    def answer_to_greeting(self, message: str, stream: bool = True) -> str:
        """
        Answer to anny question about greeting
        :param message:
            user prompt
        :param stream: bool
            'True' to make model answer on stream
            'False' to wait until model complete treatment before displaying answer

        :return:
            model answer
        """
        prompt = f"""
                Réponds très brièvement au prompt de l'utilisateur.
                Répond uniquement avec le texte de réponse. Aucun décorateur ni élément autour 
                de la réponse comme "réponse" ou "voici la réponse"
                Ajoute des emojis pour être plus friendly.
                Texte utilisateur : {message}
                """
        if stream:
            response = self.client.chat_completion(prompt)
        else:
            response = self.client.chat_completion_stream(prompt)

        logging.debug(f"{LOGGING_VARIABLE} propose_optimisation_plan: {response}")

        return response

    def answer_to_generality(self, message: str, stream: bool = True) -> str:
        """
        Answer to anny question about generality and system presentation
        :param message:
            user prompt
        :param stream: bool
            'True' to make model answer on stream
            'False' to wait until model complete treatment before displaying answer

        :return:
            model answer
        """
        prompt = f"""
                Réponds très brièvement au prompt de l'utilisateur.
                Répond uniquement avec le texte de réponse. Aucun décorateur ni élément autour 
                de la réponse comme "réponse" ou "voici la réponse"
                Ajoute des emojis pour être plus friendly.
                N'oublie pas que tu es un PoC conçu pour permettre aux utilisateur de simuler l'incidence
                des décisions et de leurs actions sur leur budget et leurs finances
                Texte utilisateur : {message}
                """
        if stream:
            response = self.client.chat_completion(prompt)
        else:
            response = self.client.chat_completion_stream(prompt)

        logging.debug(f"{LOGGING_VARIABLE} propose_optimisation_plan: {response}")

        return response

    def display_summary(self, message: str, stats: dict, stream: bool = True) -> str:
        """
        Answer to any prompt about showing transaction summary
        :param message:
            user prompt
        :param stats: dict
            contain user transactions
        :param stream: bool
            'True' to make model answer on stream
            'False' to wait until model complete treatment before displaying answer

        :return:
            model answer
        """

        prompt = f"""
                Tu es un assistant financier. Les données suivantes sont disponibles :
                Stats mensuelles: {json.dumps(stats)}
                Message utilisateur : "{message}"
                Instructions :
                1) Reste concis et synthétique.
                2) Utilise un tableau si nécessaire
                3) Donne un résumé clair avant les détails
                4) Ne pose aucune question
                5) Ajoute des emojis
                6) Traduis les catégories en français
                7) N'excède pas 20 phrases
                
                Répond uniquement avec le texte de réponse. Aucun décorateur ni élément autour 
                de la réponse comme "réponse" ou "voici la réponse"
                """
        if stream:
            response = self.client.chat_completion(prompt)
        else:
            response = self.client.chat_completion_stream(prompt)

        logging.debug(f"{LOGGING_VARIABLE} propose_optimisation_plan: {response}")

        return response

    def chat(self, message: str) -> str:
        """
        To treat any user prompt without preprocessing the prompt
        :param message: str
            user prompt

        :return:
            model answer
        """

        response = self.client.chat_completion(message)
        logging.debug(f"{LOGGING_VARIABLE} chat: {response}")
        return response

    def preprocess_and_answer(self, message: str, stats: dict = None, stream: bool = True) -> str:

        """
        Analyse user prompt and detect the financial goal.
        :param message: str
            user prompt
        :param stats: dict
             user transactions
        :param stream: bool
            'True' to make model answer on stream
            'False' to wait until model complete treatment before displaying answer

        :return: str
            model answer
        """
        prompt_category = self.detect_user_prompt_category(message)
        match prompt_category:
            case "unspecified":
                return "Je n'ai pas compris. Pouvez être plus précis svp ?"
            case "greeting":
                return self.answer_to_greeting(message=message, stream=stream)
            case "generality":
                return self.answer_to_generality(message=message, stream=stream)
            case "optimization":
                return self.propose_optimisation_plan(message=message, stats=stats, stream=stream)
            case "summary":
                return self.display_summary(message=message, stats=stats, stream=stream)
            case _:
                return self.chat(message=message)

