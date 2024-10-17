from django.contrib import admin
from django.http import HttpResponse
from .models import *
from .langchain_bot import generate_faiss

@admin.action(description='Index documents with FAISS')
def index_faiss_action(modeladmin, request, queryset):
    generate_faiss()
    return HttpResponse('FAISS indexing completed.')

class DocumentAdmin(admin.ModelAdmin):
    actions = [index_faiss_action]

admin.site.register(Docs, DocumentAdmin)
admin.site.register(ChatSession)
admin.site.register(ChatMessage)