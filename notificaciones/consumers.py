# # notificaciones/consumers.py
# import json
# from channels.generic.websocket import AsyncWebsocketConsumer

# class NotificacionConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         user = self.scope["user"]
#         await self.channel_layer.group_add("notificaciones", self.channel_name)
#         if user.is_authenticated:
#             self.user_group = f"user_{user.id}"
#             await self.channel_layer.group_add(self.user_group, self.channel_name)
#         await self.accept()

#     async def disconnect(self, close_code):
#         await self.channel_layer.group_discard("notificaciones", self.channel_name)
#         if hasattr(self, "user_group"):
#             await self.channel_layer.group_discard(self.user_group, self.channel_name)

#     async def enviar_notificacion(self, event):
#         await self.send(text_data=json.dumps({
#             "mensaje": event["mensaje"]
#         }))

import json
from channels.generic.websocket import AsyncWebsocketConsumer

class NotificacionConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope["user"]

        # Grupo global (todos los usuarios)
        await self.channel_layer.group_add("notificaciones_globales", self.channel_name)

        # Grupo personal por usuario
        if user.is_authenticated:
            self.user_group = f"user_{user.id}"
            await self.channel_layer.group_add(self.user_group, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("notificaciones_globales", self.channel_name)
        if hasattr(self, "user_group"):
            await self.channel_layer.group_discard(self.user_group, self.channel_name)

    async def enviar_notificacion(self, event):
        # event["mensaje"] contiene el mensaje
        await self.send(text_data=json.dumps({
            "mensaje": event["mensaje"],
            "tipo": event.get("tipo", "global")  # por defecto global
        }))
