import os
import pickle
import mimetypes
import faiss

from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from langchain_community.chat_models import ChatOpenAI
from chatbot_demo.settings import *
from .models import Docs
from openai import OpenAIError


from PyPDF2 import PdfReader
from docx import Document as DocxDocument

faiss_index = None  # Global FAISS index placeholder

# Generate response using LangChain and FAISS
def generate_response(user_query, faiss_index):

    # Generate the embedding for the user query
    embedding_model = OpenAIEmbeddings(api_key=OPENAI_API_KEY)
    query_embedding = embedding_model.embed_query(user_query)  # Converts plain text query to embedding

    # Retrieve relevant documents from FAISS
    relevant_docs = faiss_index.similarity_search(query_embedding)

    if not relevant_docs:
        return "No relevant documents found. Please try rephrasing your query."

    # Prepare prompt and context from retrieved documents
    context = '\n\n'.join([doc.page_content for doc in relevant_docs])

    prompt_template = ChatPromptTemplate.from_template(
        "Answer the question based on this context: {context}\nQuestion: {question}"
    )
    
    # Generate response using the OpenAI LLM
    llm = ChatOpenAI(api_key=OPENAI_API_KEY, temperature=0, model="gpt-3.5-turbo")
    chain = LLMChain(llm=llm, prompt=prompt_template)

    # Run the LangChain to get the response
    try:
        response = chain.run({"context": context, "question": user_query})
    except OpenAIError as e:
        response = "There was an issue connecting to the OpenAI API. Please try again."
    except Exception as e:
        response = f"An error occurred while generating a response: {str(e)}"
    
    return response

# Load FAISS index from file
def load_faiss():
    global faiss_index

    # If the FAISS index is already loaded, return it
    if faiss_index is not None:
        print("Using existing FAISS index.")
        return faiss_index

    # Check if FAISS index file exists
    if os.path.exists(FAISS_INDEX_FILE):
        # Load FAISS index from file
        index = faiss.read_index(FAISS_INDEX_FILE)
        embeddings = OpenAIEmbeddings(api_key=OPENAI_API_KEY)
        faiss_index = FAISS(index, embeddings)
        print("FAISS index loaded from file.")

    else:
        raise FileNotFoundError("FAISS index file not found. Please generate the index first.")

    return faiss_index

# Generate FAISS index and save it to file
def generate_faiss():
    docs = Docs.objects.all()
    texts = []
    
    # Split documents into manageable chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    
    for doc in docs:
        file_path = os.path.join(BASE_DIR, doc.file.name)
        
        # Extract the text based on file type
        content = extract_text(file_path)
        
        # Split the content into chunks
        chunks = text_splitter.split_text(content)
        texts.extend(chunks)
    
    # Create FAISS index with embeddings
    embeddings = OpenAIEmbeddings(api_key=OPENAI_API_KEY)
    faiss_index = FAISS.from_texts(texts, embeddings)
    
    # Save FAISS index to file
    faiss.write_index(faiss_index.index, FAISS_INDEX_FILE)
    print("FAISS index generated and saved to file.")

    return faiss_index

def extract_text(file_path):
    mime_type, _ = mimetypes.guess_type(file_path)
    
    if mime_type == 'application/pdf':
        # Extract text from PDF
        return extract_text_from_pdf(file_path)
    elif mime_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':  # .docx MIME type
        # Extract text from DOCX
        return extract_text_from_docx(file_path)
    elif mime_type.startswith('text'):  # Plain text files
        # Extract text from plain text file
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    else:
        raise ValueError(f"Unsupported file type: {mime_type}")

def extract_text_from_pdf(file_path):
    with open(file_path, 'rb') as f:
        reader = PdfReader(f)
        text = ''
        for page in reader.pages:
            text += page.extract_text()
        return text

def extract_text_from_docx(file_path):
    doc = DocxDocument(file_path)
    text = ''
    for para in doc.paragraphs:
        text += para.text
    return text
