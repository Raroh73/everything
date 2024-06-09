import ollama
from django.apps import AppConfig
from django.conf import settings


class ChatConfig(AppConfig):
    name = "chat"

    def ready(self):
        ollama.pull(settings.MODEL)
