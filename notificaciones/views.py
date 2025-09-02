from django.shortcuts import render
from django.http import JsonResponse
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

def index(request):
    return render(request, 'notificaciones/index.html')


def enviar_global(request):
    if (request.user.is_authenticated):
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "notificaciones_globales",
            {"type": "enviar_notificacion", "mensaje": "Hola a todos! 🌍", "tipo": "global"},
        )
        return JsonResponse({"status": "ok"})
    else:
        return JsonResponse({"status": "Unauthorized"})

@login_required
def enviar_a_usuario(request, user_id):
    mensaje = request.GET.get("mensaje", "Hola")
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return JsonResponse({"status": "error", "mensaje": "Usuario no encontrado"}, status=404)

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"user_{user.id}",
        {
            "type": "enviar_notificacion",
            "mensaje": f"{mensaje}",
            "tipo": "personal",
        }
    )
    return JsonResponse({"status": "ok", "mensaje": f"Notificación enviada a {user.username}"})