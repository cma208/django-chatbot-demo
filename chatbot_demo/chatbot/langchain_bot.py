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
    # Load documents (e.g., PDF and TXT)
    pdf_loader = PyPDFLoader("example.pdf")
    txt_loader = TextLoader("example.txt")
    
    documents = pdf_loader.load_and_split() + txt_loader.load()

    # Split documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    texts = text_splitter.split_documents(documents)

    # Create FAISS index with OpenAI embeddings
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
