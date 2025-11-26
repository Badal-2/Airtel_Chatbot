from django.contrib import admin
from django.urls import path

from .import views

urlpatterns = [
    path('', views.chat_page, name='chat_page'),
    path('api/chat/', views.get_llm_response, name='get_llm_response'),
    path('generate1/', views.generate_voice, name='generate_voice'),
]