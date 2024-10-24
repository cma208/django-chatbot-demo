from django.core.management.base import BaseCommand
from chatbot.langchain_bot import get_answer_from_index_with_memory

class Command(BaseCommand):
    help = "Test question-answer functionality using FAISS with chat memory"

    def add_arguments(self, parser):
        # Add command-line arguments for question, index_name, session_id, and max_context_messages
        parser.add_argument('question', type=str, help='The question to ask the system')
        parser.add_argument('index_name', type=str, help='Name of the theme index')
        parser.add_argument('session_id', type=str, help='The ID of the chat session')
        parser.add_argument(
            '--max_context_messages', 
            type=int, 
            default=10, 
            help='Maximum number of previous messages to use for context (default: 10)'
        )

    def handle(self, *args, **kwargs):
        # Retrieve command-line arguments
        question = kwargs['question']
        index_name = kwargs['index_name']
        session_id = kwargs['session_id']
        max_context_messages = kwargs['max_context_messages']

        self.stdout.write("Starting question-answer test with chat memory...")

        try:
            # Call the get_answer_from_index_with_memory function with the provided arguments
            response = get_answer_from_index_with_memory(
                question, 
                index_name, 
                session_id, 
                max_context_messages=max_context_messages
            )
            self.stdout.write(self.style.SUCCESS(f"Response: {response}"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Failed to get a response: {e}"))
