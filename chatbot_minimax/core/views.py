import json
import logging
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .utils import get_groq_response_with_rag, generate_voice_from_text



logger = logging.getLogger(__name__)




def chat_page(request):
    return render(request, 'index.html')



@csrf_exempt
def get_llm_response(request):
    """Handle chat requests with RAG"""
    print("🔵 /api/chat/ endpoint called!")
    
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST allowed'}, status=405)
    
    try:
        data = json.loads(request.body)
        user_message = data.get('response', '').strip()
        
        print(f"👤 User message: {user_message}")
        
        if not user_message:
            return JsonResponse({'error': 'Empty message'}, status=400)
        
        # Get LLM response with RAG
        reply = get_groq_response_with_rag(user_message)
        print(f"🤖 Bot reply: {reply}")
        
        # NEW: Save conversation to database
        user_id = data.get('sender', 'user_default')
        session_id = data.get('number', 'session_default')
        from .utils import save_conversation
        save_conversation(user_id, user_message, reply, session_id)
        
        return JsonResponse({'response': reply, 'status': 'success'})
    
    except json.JSONDecodeError:
        print("❌ Invalid JSON received")
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        print(f"❌ Error in get_llm_response: {str(e)}")
        logger.error(f"Error: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)






@csrf_exempt
def generate_voice(request):
    print("🔵 /generate1/ endpoint called!")
    
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST allowed'}, status=405)
    
    try:
        # Get message from request
        text = request.POST.get('message', '').strip()
        
        
        if not text:
            return JsonResponse({'error': 'No message provided'}, status=400)
        
        # Generate voice (from utils.py)
        voice_url = generate_voice_from_text(text)
        
        if not voice_url:
            return JsonResponse({'error': 'Failed to generate voice'}, status=500)
        
        return JsonResponse({'voice_url': voice_url, 'status': 'success'})
    
    except Exception as e:
        print(f"❌ Error in generate_voice: {str(e)}")
        logger.error(f"Error: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)