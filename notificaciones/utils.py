from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

def enviar_notificacion_a_usuario(user_id, mensaje):
    """
    Envía una notificación a un usuario específico por su ID.
    """
    channel_layer = get_channel_layer()
    grupo = f"user_{user_id}"  

    async_to_sync(channel_layer.group_send)(
        grupo,
        {
            "type": "enviar_notificacion",  # Debe coincidir con el handler del consumer
            "mensaje": mensaje,
            "tipo": "personal"
        }
    )
