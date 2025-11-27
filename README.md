Airtel Chatbot with RAG
An intelligent customer support chatbot for Airtel that uses Retrieval Augmented Generation (RAG) to provide accurate, context-aware responses about Airtel services.
🎯 Features

RAG Technology: FAISS vector search + sentence-transformers for accurate information retrieval
Conversation Memory: PostgreSQL database stores chat history for context-aware responses
Voice Support:

Speech-to-text (Web Speech API)
Text-to-speech (gTTS)


LLM Integration: GROQ API for natural language generation
Responsive UI: Works on mobile, tablet, and desktop
Airtel Branding: Beautiful red-themed interface matching Airtel brand

🏗️ Architecture
User Input (Text/Voice)
    ↓
FAISS Vector Search (airtel_data.py)
    ↓
Retrieve TOP-K Similar Results
    ↓
PostgreSQL Conversation History
    ↓
GROQ LLM (Generate Response)
    ↓
Bot Output (Text + Voice)
🛠️ Tech Stack

Backend: Django 5.2.8
LLM: GROQ API (llama-3.1-8b-instant)
Vector Search: FAISS + sentence-transformers
Database: PostgreSQL
Text-to-Speech: gTTS
Frontend: HTML/CSS/JavaScript
Voice Input: Web Speech API

📋 Prerequisites

Python 3.10+
PostgreSQL 12+
pip (Python package manager)

🚀 Installation
1. Clone Repository
bashgit clone https://github.com/yourusername/airtel-chatbot-rag.git
cd airtel-chatbot-rag
2. Create Virtual Environment
bashpython -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
3. Install Dependencies
bashpip install -r requirements.txt
4. Create .env File
bash# Create file in project root
GROQ_API_KEY=your_groq_api_key_here
5. Install & Setup PostgreSQL
bash# Windows: Download from https://www.postgresql.org/download/
# Mac: brew install postgresql
# Linux: sudo apt-get install postgresql
6. Create Database
bashcreatedb airtel_db
7. Run Migrations
bashpython manage.py makemigrations
python manage.py migrate
8. Start Server
bashpython manage.py runserver
Visit: http://127.0.0.1:8000/
📁 Project Structure
chatbot_minimax/
├── chatbot_minimax/          # Project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── core/                     # Main app
│   ├── models.py            # Conversation model
│   ├── views.py             # API endpoints
│   ├── utils.py             # RAG logic
│   ├── airtel_data.py       # Company data
│   └── urls.py
├── templates/
│   └── index.html           # Chat UI
├── requirements.txt
└── manage.py








py
🧠 How RAG Works

Data Preparation: Airtel company data stored in airtel_data.py
Embedding: Text converted to vectors using sentence-transformers
Indexing: Vectors stored in FAISS index (in-memory)
Search: User query converted to vector, FAISS finds TOP-K similar results
Context: Retrieved results passed to GROQ LLM
Generation: LLM generates natural response with context
Memory: Chat saved in PostgreSQL for future context

💬 Usage
Text Chat

Type message in input field
Click send button or press Enter
Bot responds with voice + text

Voice Chat

Click microphone button
Speak your question
Bot responds automatically

Example Queries

"What's the best Airtel plan?"
"How do I recharge?"
"What's your customer support number?"
"Tell me about 5G plans"
"Who developed you?"






    <img width="1918" height="1079" alt="image" src="https://github.com/user-attachments/assets/df83fbd7-1730-4614-a04f-c5f5f772531a" />

