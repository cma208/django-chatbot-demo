# Chatbot Demo with Session Management and Information Retrieval in Django

RAGBot is an advanced chatbot system that combines Retrieval-Augmented Generation (RAG) with language models to provide accurate, document-based responses. Developed using Django, and integrating technologies like LangChain, OpenAI, and FAISS, this project enables seamless integration of language models with specific data sources, maintaining coherent context across chat sessions.

## Features
- **Information Retrieval**: Uses FAISS to index documents and find relevant information.
- **Response Generation**: Utilizes language models (OpenAI GPT) to generate precise, natural responses.
- **Session Management**: Supports the creation and management of chat sessions by user.
- **REST API**: Provides an API to interact with the chatbot and manage sessions via HTTP requests.
- **Custom Management Commands**: Special commands to handle tasks like document indexing and testing.

## Technologies Used
- **Django**: Web framework for backend development.
- **Django REST Framework**: To build the REST API.
- **LangChain**: For integrating language models and information retrieval.
- **OpenAI**: For generating responses using GPT models.
- **FAISS**: For indexing and retrieving information from documents.
- **Swagger**: Automatic API documentation.

## Installation

### Prerequisites
- Python 3.8+
- OpenAI API Key
- Virtual Environment (recommended)

### Instructions
1. **Clone the repository**:
    ```bash
    git clone https://github.com/cma208/django-chatbot-demo.git
    cd django-chatbot-demo
    ```

2. **Create a virtual environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate   # On Windows use: venv\Scripts\activate
    ```

3. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Configure environment variables**:
    Create a `.env` file in the root directory of the project with the following variables:
    ```env
    OPENAI_API_KEY=your_openai_api_key_here
    ```

5. **Run database migrations**:
    ```bash
    python manage.py migrate
    ```

6. **Create an admin (superuser) account**:
    ```bash
    python manage.py createsuperuser
    ```
    Follow the prompts to set up a username, email, and password for your admin account.

7. **Start the development server**:
    ```bash
    python manage.py runserver
    ```
