# chatbot.py
import ollama

def chat_with_bot(user_query, context_text):
    """
    Ollama-powered chatbot using lecture transcription as context
    """
    try:
        prompt = f"""
You are an intelligent lecture assistant. Use the lecture transcript to answer the user's question concisely.

Lecture transcript:
{context_text}

User question:
{user_query}

Answer:
"""

        # Use ollama.chat directly
        response = ollama.chat(
    model="gemma:2b",
    messages=[{"role": "user", "content": prompt}]
)
        return response["message"]["content"]


        

    except Exception as e:
        print("Ollama API error:", e)
        return "Sorry, I couldn't generate an answer at this moment."