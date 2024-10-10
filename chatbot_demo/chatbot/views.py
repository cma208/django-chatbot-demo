from django.shortcuts import render

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .langchain_bot import retrieve_and_answer

@login_required
def chatbot_response(request):
    user = request.user
    question = request.GET.get('question')
    
    # Generate a response using the fine-tuned model and FAISS-based retrieval
    answer = retrieve_and_answer(user, question)
    
    return JsonResponse({'answer': answer})

