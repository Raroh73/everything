import json

import markdown
import nh3
import ollama
from channels.generic.websocket import WebsocketConsumer
from django.conf import settings

from . import models


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.chat = models.Chat()
        self.chat.save()

        self.accept()

    def receive(self, text_data):
        self.chat.refresh_from_db()

        message_text = json.loads(text_data)["message"]

        id = f"message-{len(self.chat.messages)}"

        self.send(
            text_data=json.dumps(
                {
                    "id": id,
                    "content": nh3.clean(message_text),
                }
            )
        )

        self.chat.messages.append({"role": "user", "content": message_text})
        self.chat.save()

        response = ollama.chat(
            messages=self.chat.messages,
            stream=True,
            model=settings.MODEL,
        )

        id = f"message-{len(self.chat.messages)}"
        message = ""
        for chunk in response:
            message_chunk = chunk["message"]["content"]
            if message_chunk is not None:
                message += message_chunk
                self.send(
                    text_data=json.dumps(
                        {
                            "id": id,
                            "content": nh3.clean(
                                markdown.markdown(message, extensions=["fenced_code"])
                            ),
                        }
                    )
                )

        self.chat.messages.append({"role": "assistant", "content": message})
        self.chat.save()
        print(self.chat.messages)
