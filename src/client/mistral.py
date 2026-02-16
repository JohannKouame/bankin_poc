import json
import logging
import os
import re
from src.utils.string_sanitizer import StringSanitizer

from mistralai import Mistral
import requests

LOGGING_VARIABLE = "[MISTRAL]"
class MistralClient:
    def __init__(self) -> None:
        self.token = os.environ["MISTRAL_TOKEN_API"]
        self.default_model = os.environ["MISTRAL_MODEL_NAME"]

    def request(self, prompt: str):
        with Mistral(
                api_key=self.token
        ) as mistral:

            res = mistral.chat.complete(model=self.default_model, messages=[
                {
                    "content": prompt,
                    "role": "user",
                },
            ], stream=False)

        # Handle response
        return res.model_dump()["choices"][0]["message"]["content"]



    def chat_completion(self, prompt: str):
        logging.debug(f"{LOGGING_VARIABLE} Sending request...")
        response = self.request(prompt)
        logging.debug(f"{LOGGING_VARIABLE} {response}")
        return response
