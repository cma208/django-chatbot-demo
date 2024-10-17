from django.core.management.base import BaseCommand
from chatbot.langchain_bot import generate_faiss

class Command(BaseCommand):
    help = 'Indexes documents using FAISS'

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting FAISS indexing...")
        generate_faiss()
        self.stdout.write(self.style.SUCCESS('Successfully indexed documents with FAISS'))
