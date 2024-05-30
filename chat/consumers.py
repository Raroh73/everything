import json
import uuid

import markdown
from channels.generic.websocket import AsyncWebsocketConsumer
from django.conf import settings
from django.template.loader import render_to_string
from openai import AsyncOpenAI

from . import models


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.openai_client = AsyncOpenAI(
            base_url=settings.OPENAI_URL,
            api_key=settings.OPENAI_KEY,
        )

        self.chat = models.Chat()
        await self.chat.asave()

        await self.accept()

    async def receive(self, text_data):
        self.chat.arefresh_from_db()

        message_text = json.loads(text_data)["message"]

        user_message_html = render_to_string(
            "message.html", {"message_text": message_text}
        )
        await self.send(text_data=user_message_html)

        self.chat.messages.append({"role": "user", "content": message_text})
        await self.chat.asave()

        message_id = f"message-{uuid.uuid4().hex}"

        system_message_html = render_to_string(
            "message.html",
            {
                "message_text": "",
                "message_id": message_id,
            },
        )

        await self.send(text_data=system_message_html)

        openai_response = await self.openai_client.chat.completions.create(
            messages=self.chat.messages,
            stream=True,
            model=settings.MODEL,
        )

        message = ""
        async for chunk in openai_response:
            message_chunk = chunk.choices[0].delta.content
            if message_chunk is not None:
                message += message_chunk
                await self.send(
                    text_data=f'<div id="{message_id}" hx-swap-oob="innerHTML">{markdown.markdown(message, extensions=["codehilite", "fenced_code"])}</div>'
                )

        self.chat.messages.append({"role": "assistant", "content": message})
        await self.chat.asave()
        print(self.chat.messages)
