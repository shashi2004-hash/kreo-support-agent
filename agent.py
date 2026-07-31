import os
from dotenv import load_dotenv
import chromadb
from chromadb.utils import embedding_functions
from groq import Groq
from logger import log_conversation

load_dotenv()

# Connect to the same ChromaDB we built with ingest.py
embedding_fn = embedding_functions.DefaultEmbeddingFunction()

client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(
    name="kreo_support",
    embedding_function=embedding_fn
)

# Groq client
groq_client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
def retrieve_context(question, n_results=3, distance_threshold=1.3):
    results = collection.query(
        query_texts=[question],
        n_results=n_results
    )
    chunks = results["documents"][0]
    distances = results["distances"][0]

    if not distances or distances[0] > distance_threshold:
        return None

    return "\n\n".join(chunks)

def ask_agent(question):
    context = retrieve_context(question)

    if context is None:
        answer = "I don't have that information. Please contact Kreo support on WhatsApp at +91-9611507877 for assistance."
        log_conversation(question, "NO MATCH (below confidence threshold)", answer)
        return answer

    prompt = f"""You are a helpful customer support agent for Kreo, a gaming and content-creator gear brand.
Answer the customer's question using ONLY the information in the context below.

The context may contain information about several different Kreo products. Use only the parts of the context that specifically relate to the product or topic the customer is asking about.

If the context includes relevant information about the specific product/topic asked, answer confidently and directly using it.

If the context does NOT mention the specific product or topic the customer asked about, say you don't have that information and suggest they contact Kreo support on WhatsApp at +91-9611507877.

Never borrow specs, warranty periods, or instructions from a different, unrelated product to answer the question.

Context:
{context}

Customer question: {question}

Answer:"""

    response = groq_client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    answer = response.choices[0].message.content

    log_conversation(question, context, answer)

    return answer

# Simple chat loop
# Simple chat loop
if __name__ == "__main__":
    print("Kreo Support Agent — type 'quit' to exit\n")
    while True:
        question = input("You: ")
        if question.lower() == "quit":
            break
        answer = ask_agent(question)
        print(f"\nAgent: {answer}\n")