import re

class StringSanitizer:
    @staticmethod
    def remove_json_tags(message: str) -> str:
        cleaned_message = re.sub(r"json\s*(\{.*?\})\s*", message, flags=re.DOTALL)
        return cleaned_message

    @staticmethod
    def remove_html_tags(message: str) -> str:
        cleaned_message = re.sub(r'<a[^>]*>.*?</a>', '', message, flags=re.DOTALL)
        cleaned_message = re.sub(r'<[^>]+>', '', cleaned_message)
        return cleaned_message

    @staticmethod
    def remove_lines_break(message: str) -> str:
        return message.replace("\n", "")

