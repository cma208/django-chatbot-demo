from django.contrib.auth.models import User
from django.db import models

class DocThemes(models.Model):
    id = models.AutoField(primary_key=True)
    theme = models.CharField(max_length=255, null=False, blank=False)

class PartitonPypes(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=20, null=False)

class Docs(models.Model):
    id = models.AutoField(primary_key=True)
    file = models.FileField(upload_to='faiss_data/docs/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    author = models.CharField(max_length=255, null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    theme = models.ForeignKey(DocThemes, on_delete=models.PROTECT)
    partition = models.ForeignKey(PartitonPypes, on_delete=models.PROTECT) # TODO: In case of implement different partition ratios
    faiss_loaded = models.BooleanField(default=False, null=False, blank=False)
    
    def __str__(self):
        return self.title or self.file.name

class ChatSession(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class ChatMessage(models.Model):
    id = models.AutoField(primary_key=True)
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE)
    message = models.TextField()
    response = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)