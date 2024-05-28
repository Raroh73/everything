from django.db import models


def messages_default():
    return [{"role": "system", "content": "You are Everything, a helpful chatbot."}]


class Chat(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    messages = models.JSONField(default=messages_default)
