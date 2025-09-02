from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('enviar-global/', views.enviar_global),
    path('enviar/<int:user_id>/', views.enviar_a_usuario),
]
