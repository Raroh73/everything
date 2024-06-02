import json
import uuid

import markdown
from channels.generic.websocket import WebsocketConsumer
from django.conf import settings
from django.template.loader import render_to_string
from openai import OpenAI

from . import models


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.openai_client = OpenAI(
            base_url=settings.OPENAI_URL,
            api_key=settings.OPENAI_KEY,
        )

        self.chat = models.Chat()
        self.chat.save()

        self.accept()

    def receive(self, text_data):
        self.chat.refresh_from_db()

        message_text = json.loads(text_data)["message"]

        user_message_html = render_to_string(
            "message.html", {"message_text": message_text}
        )
        self.send(text_data=user_message_html)

        self.chat.messages.append({"role": "user", "content": message_text})
        self.chat.save()

        message_id = f"message-{uuid.uuid4().hex}"

        system_message_html = render_to_string(
            "message.html",
            {
                "message_text": "",
                "message_id": message_id,
            },
        )

        self.send(text_data=system_message_html)

        openai_response = self.openai_client.chat.completions.create(
            messages=self.chat.messages,
            stream=True,
            model=settings.MODEL,
        )

        message = ""
        for chunk in openai_response:
            message_chunk = chunk.choices[0].delta.content
            if message_chunk is not None:
                message += message_chunk
                self.send(
                    text_data=f'<div id="{message_id}" hx-swap-oob="innerHTML">{markdown.markdown(message, extensions=["codehilite", "fenced_code"])}</div>'
                )

        self.chat.messages.append({"role": "assistant", "content": message})
        self.chat.save()
        print(self.chat.messages)
