__Airtel Chatbot with RAG__

An intelligent customer support chatbot for Airtel that uses Retrieval Augmented Generation (RAG) to provide accurate, context-aware responses about Airtel services.











__2nd flow__


1. FAISS + airtel_data.py
   ├─ Retrieves Airtel company data
   └─ Gives to LLM for answering

2. PostgreSQL + Conversation Table
   ├─ Saves user messages
   ├─ Saves bot responses
   ├─ Saves with user ID
   ├─ Saves with timestamp
   └─ Creates CONVERSATION HISTORY

3. LLM (GROQ)
   ├─ Gets Airtel data from FAISS
   ├─ Gets previous chat from PostgreSQL
   ├─ Generates response with context
   └─ Memory-aware answers






__CorrectFlow__

┌─────────────────────────────────────────┐
│ User Input: "Best plan?"                │
└──────────────┬──────────────────────────┘
               ↓
    ┌──────────────────────┐
    │ Convert to Vector    │ (Sentence Transformer)
    │ [0.3, 0.4, 0.9...]  │
    └────────────┬─────────┘
                 ↓
    ┌──────────────────────────────┐
    │ Search FAISS Index           │
    │ (Pre-made vectors from       │
    │  airtel_data.py)             │
    └────────────┬─────────────────┘
                 ↓
    ┌──────────────────────────────┐
    │ Get TOP-K Results            │
    │ from airtel_data.py vectors  │
    └────────────┬─────────────────┘
                 ↓
    ┌──────────────────────────────┐
    │ Pass Context to LLM          │
    └────────────┬─────────────────┘
                 ↓
    ┌──────────────────────────────┐
    │ LLM Generates Response       │
    └────────────┬─────────────────┘
                 ↓
    ┌──────────────────────────────┐
    │ Save to PostgreSQL           │
    │ ✅ User text                 │
    │ ✅ Bot response              │
    │ ✅ User ID                   │
    │ ❌ Vectors (NOT saved)       │
    └──────────────────────────────┘

User vectors are NOT saved - only USED for searching! 🔍






 👉👉👉  ALL THESE THINGS ARE VERY IMPORTANT __BADAL__



Why Convert User Text to Vector?
Because FAISS only understands VECTORS (numbers)!
User Text: "Best plan?"
    ↓
Convert to Vector: [0.25, 0.55, 0.85, ...]
    ↓
NOW FAISS can compare it with Airtel vectors!
    ↓
FAISS finds: "Which Airtel vector is closest to user vector?"
    ↓
Returns TOP-K similar results ✅


