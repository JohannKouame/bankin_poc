# ./src/client/mistral_client.py

import os
from mistralai import Mistral
from typing import Generator

LOGGING_VARIABLE = "[MISTRAL]"

class MistralClient:
    def __init__(self) -> None:
        self.token = os.environ["MISTRAL_TOKEN_API"]
        self.default_model = os.environ["MISTRAL_MODEL_NAME"]

    def request(self, prompt: str) -> str:
        """
        Request model in stream mode
        :param prompt: str
            user prompt

        :return:
            model response
        """
        with Mistral(api_key=self.token) as mistral:
            res = mistral.chat.complete(
                model=self.default_model,
                messages=[{"role": "user", "content": prompt}],
                stream=False,
                max_tokens=1000,
                temperature=0
            )

        return res.model_dump()["choices"][0]["message"]["content"]

    def request_stream(self, prompt: str) -> Generator:
        """
        Request model in stream mode
        :param prompt: str
            user prompt

        :return: Generator
            stream response
        """
        with Mistral(api_key=self.token) as mistral:
            stream_response = mistral.chat.stream(
                model=self.default_model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1000,
                temperature=0
            )

            for chunk in stream_response:
                delta = chunk.data.choices[0].delta

                if delta.content:
                    yield delta.content

    def chat_completion(self, prompt: str) -> str:
        """
        Method to chat with model
        :param prompt: str
            user prompt

        :return: str
            model answer
        """
        return self.request(prompt)

    def chat_completion_stream(self, prompt: str) -> Generator :
        """
        Method to chat with model in stream mode
        :param prompt: str
            user prompt

        :return: Generator
            model answer
        """
        return self.request_stream(prompt)
