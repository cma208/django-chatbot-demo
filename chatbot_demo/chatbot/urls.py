from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_document, name='document_upload'),
    path('chat/', views.chatbot_view, name='chatbot_view'),
]
