from django.contrib.auth.models import User
from django.db import models

class Chat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    summary = models.TextField()  # Store conversation summary
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Chat summary for {self.user.username} at {self.timestamp}"

