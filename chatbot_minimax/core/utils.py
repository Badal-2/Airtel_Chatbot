import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq
from gtts import gTTS
import uuid
from .airtel_data import AIRTEL_DATA
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from .models import Conversation



load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)




# ➖ Load embedding model
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')


# Convert all Airtel data to vectors
airtel_embeddings = embedding_model.encode(AIRTEL_DATA)
print(f"✅ Created {len(airtel_embeddings)} vectors!")






airtel_embeddings_array = np.array(airtel_embeddings).astype('float32')
faiss_index = faiss.IndexFlatL2(airtel_embeddings_array.shape[1])
faiss_index.add(airtel_embeddings_array)



# ========== SEARCH FUNCTION ==========

def search_airtel_data(user_question):
    try:
        # Convert user question to vector
        question_vector = embedding_model.encode([user_question]).astype('float32')
        
        # Search FAISS for top 3 similar vectors
        distances, indices = faiss_index.search(question_vector, k=3)
        
        # Get the relevant text chunks
        relevant_data = []
        for idx in indices[0]:
            relevant_data.append(AIRTEL_DATA[idx])
        
        # Combine into context
        context = "\n".join(relevant_data)
        
        for data in relevant_data:
            print(f"   ✅ {data}")
        
        return context
    
    except Exception as e:
        print(f"❌ Search Error: {str(e)}")
        return ""



# ========== LLM FUNCTION ==========

def get_groq_response_with_rag(user_prompt):
    if not GROQ_API_KEY:
        return "GROQ API Key not configured"
    try:
        # Step 1: Search for relevant Airtel data
        context = search_airtel_data(user_prompt)
        
        # Step 2: Create enhanced prompt with context
        enhanced_prompt = f"""You are an Airtel customer support bot.

Here is relevant Airtel information:
{context}

Customer Question: {user_prompt}

Answer ONLY based on the Airtel information above. If the question is not about Airtel, politely decline and redirect to Airtel services."""
        
        # Step 3: Call GROQ LLM with context
        message = client.chat.completions.create(
            messages=[
                {"role": "user", "content": enhanced_prompt}
            ],
            model="llama-3.1-8b-instant",
            temperature=0.7,
            max_tokens=1024,
        )
        
        reply = message.choices[0].message.content
        return reply
    
    except Exception as e:
        # print(f"❌ GROQ Error: {str(e)}")
        return f"Error: {str(e)}"



# ========== VOICE FUNCTIONS ==========

def generate_voice_from_text(text):
    try:
        if not text or len(text.strip()) == 0:
            return None
        
        if len(text) > 500:
            text = text[:500]
        
        media_dir = Path('media')
        media_dir.mkdir(exist_ok=True)
        
        filename = f"media/{uuid.uuid4()}.mp3"
        
        tts = gTTS(text=text, lang='en', slow=False)
        tts.save(filename)
        
        voice_url = f"/{filename}"
        # print(f"✅ Voice generated: {voice_url}")
        return voice_url
    
    except Exception as e:
        print(f"❌ gTTS error: {str(e)}")
        return None
    



# ========== Conversation FUNCTIONS ==========

def save_conversation(user_id, user_message, bot_response, session_id="default"):
    """Save conversation to database for memory tracking"""
    try:
        conversation = Conversation(
            user_id=user_id,
            user_message=user_message,
            bot_response=bot_response,
            session_id=session_id
        )
        conversation.save()
        print(f"✅ Conversation saved! ID: {conversation.id}")
        return conversation.id
    except Exception as e:
        print(f"❌ Error saving conversation: {str(e)}")
        return None    