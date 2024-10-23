from django.core.management.base import BaseCommand
from chatbot.langchain_bot import generate_faiss_with_retry

class Command(BaseCommand):
    help = 'Indexes documents using FAISS'

    def add_arguments(self, parser):
        # Add command-line arguments for index_id and index_name
        parser.add_argument('index_id', type=int, help='ID of the theme index')
        parser.add_argument('index_name', type=str, help='Name of the theme index')

    def handle(self, *args, **kwargs):
        # Retrieve command-line arguments
        index_id = kwargs['index_id']
        index_name = kwargs['index_name']

        self.stdout.write("Starting FAISS indexing...")

        try:
            # Call the generate_faiss function with the provided arguments
            file_names = generate_faiss_with_retry(index_id, index_name)
            self.stdout.write(self.style.SUCCESS(f'Successfully indexed documents: {file_names}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Failed to index documents: {e}'))
