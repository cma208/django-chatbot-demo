from django.core.management.base import BaseCommand
from chatbot.langchain_bot import get_answer_from_index

class Command(BaseCommand):
    help = "Test question-answer functionality using FAISS"

    def add_arguments(self, parser):
        # Add command-line arguments for question and index_name
        parser.add_argument('question', type=str, help='The question to ask the system')
        parser.add_argument('index_name', type=str, help='Name of the theme index')

    def handle(self, *args, **kwargs):
        # Retrieve command-line arguments
        question = kwargs['question']
        index_name = kwargs['index_name']

        self.stdout.write("Starting question-answer test...")

        try:
            # Call the get_answer_from_index function with the provided arguments
            response = get_answer_from_index(question, index_name)
            self.stdout.write(self.style.SUCCESS(f"Response: {response}"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Failed to get a response: {e}"))

# Copy this for testing purposes
# python manage.py test "hablame sobre el perfil resumido" "Pruebas"
