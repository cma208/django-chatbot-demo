from django.contrib import admin
from django.http import HttpResponse
from .models import *
from .langchain_bot import generate_faiss

@admin.action(description='Index documents with FAISS')
def index_faiss_action(modeladmin, request, queryset):
    # Get the theme ID and theme name from the queryset
    themes = queryset.values_list('theme', flat=True).distinct()
    
    if len(themes) == 1:
        # Only proceed if there is a single theme for the selected documents
        theme_id = themes[0]
        theme_name = DocThemes.objects.get(id=theme_id).theme
        
        # Run the FAISS indexing for the selected theme
        generate_faiss(theme_id, theme_name)
        return HttpResponse('FAISS indexing completed.')
    else:
        # If multiple themes are selected, show a message
        return HttpResponse('Please select documents with the same theme to run FAISS indexing.')

class DocumentAdmin(admin.ModelAdmin):
    actions = [index_faiss_action]

admin.site.register(Docs, DocumentAdmin)
admin.site.register(ChatSession)
admin.site.register(ChatMessage)
admin.site.register(DocThemes)
admin.site.register(PartitonPypes)