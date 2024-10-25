from django.urls import path
from .views import *

urlpatterns = [    
    # Only get and post
    path('chat/', Chat.as_view(), name='chat'),
    path('messages/', Messages.as_view(), name='messages'),
    path('session/', Session.as_view(), name='sessions'),
    path('themes/', Themes.as_view(), name='themes'),
    path('partitions/', Partitions.as_view(), name='partitions'),
]
