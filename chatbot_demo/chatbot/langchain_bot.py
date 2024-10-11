import os
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import ConversationChain
from langchain.memory import ConversationSummaryMemory
from .models import Chat

# Load environment variables
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# Load documents and create FAISS index
def load_and_index_documents():
    # Define the directory where the files are located
    files_dir = "files"  # The 'files' directory from your tree

    documents = []

    # Iterate through each file in the directory
    for filename in os.listdir(files_dir):
        file_path = os.path.join(files_dir, filename)
        
        if filename.endswith(".pdf"):
            # If the file is a PDF, load it using PyPDFLoader
            loader = PyPDFLoader(file_path)
            documents += loader.load_and_split()
        
        elif filename.endswith(".txt"):
            # If the file is a text file, load it using TextLoader
            loader = TextLoader(file_path)
            documents += loader.load()
    
    # Split documents into manageable chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    texts = text_splitter.split_documents(documents)

    # Create an embedding model and FAISS vector store
    embedding_model = OpenAIEmbeddings(api_key=openai_api_key)
    vectorstore = FAISS.from_documents(texts, embedding_model)
    
    return vectorstore

# Retrieve the chat summary for a user
def get_user_chat_summary(user):
    try:
        chat = Chat.objects.filter(user=user).latest('timestamp')
        return chat.summary
    except Chat.DoesNotExist:
        return ""

# Save updated chat summary to the database
def save_user_chat_summary(user, summary):
    chat = Chat(user=user, summary=summary)
    chat.save()

# Create a conversation chain with memory and FAISS-based retrieval
def create_conversation_chain(user):
    previous_summary = get_user_chat_summary(user)

    memory = ConversationSummaryMemory(llm=ChatOpenAI(api_key=openai_api_key), initial_summary=previous_summary)

    llm = ChatOpenAI(api_key=openai_api_key)
    conversation_chain = ConversationChain(llm=llm, memory=memory)
    
    return conversation_chain, memory

# Retrieve an answer from the fine-tuned model and FAISS index
def retrieve_and_answer(user, question):
    conversation_chain, memory = create_conversation_chain(user)

    vectorstore = load_and_index_documents()
    retriever = vectorstore.as_retriever()
    relevant_docs = retriever.get_relevant_documents(question)
    
    context = "\n\n".join([doc.page_content for doc in relevant_docs])
    final_question = f"Context: {context}\n\nQuestion: {question}"

    response = conversation_chain.run(final_question)

    save_user_chat_summary(user, memory.load_memory_variables({})['summary'])
    
    return response
