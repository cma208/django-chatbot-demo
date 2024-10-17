from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Docs, ChatSession, ChatMessage
from .langchain_bot import load_faiss, generate_response
import uuid

# Initialize FAISS index once globally
faiss_index = None

@login_required
def upload_document(request):
    if request.method == 'POST':
        file = request.FILES['file']
        Docs.objects.create(file=file)
        return redirect('document_upload')
    
    return render(request, 'upload.html')

@login_required
def chatbot_view(request):
    global faiss_index
    if request.method == 'POST':
        user_query = request.POST.get('query')
        
        session_id = request.session.get('session_id', None)
        if not session_id:
            session_id = str(uuid.uuid4())
            request.session['session_id'] = session_id
        
        chat_session, created = ChatSession.objects.get_or_create(
            user=request.user, session_id=session_id
        )
        
        # Ensure FAISS index is initialized
        if faiss_index is None:
            faiss_index = load_faiss()

        # Generate response using FAISS and LangChain
        response = generate_response(user_query, faiss_index)
        
        ChatMessage.objects.create(session=chat_session, message=user_query, response=response)
        return JsonResponse({'response': response})
    
    return render(request, 'chat.html')
