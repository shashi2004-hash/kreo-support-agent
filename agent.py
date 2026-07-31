import os
import pickle
from dotenv import load_dotenv
from sklearn.metrics.pairwise import cosine_similarity
from groq import Groq
from logger import log_conversation

load_dotenv()

with open("index.pkl", "rb") as f:
    index = pickle.load(f)
    vectorizer = index["vectorizer"]
    tfidf_matrix = index["matrix"]
    chunks = index["chunks"]

groq_client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def retrieve_context(question, n_results=3, score_threshold=0.15):
    query_vec = vectorizer.transform([question])
    sims = cosine_similarity(query_vec, tfidf_matrix)[0]
    top_idx = sims.argsort()[::-1][:n_results]

    if sims[top_idx[0]] < score_threshold:
        return None

    top_chunks = [chunks[i] for i in top_idx]
    return "\n\n".join(top_chunks)

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

if __name__ == "__main__":
    print("Kreo Support Agent — type 'quit' to exit\n")
    while True:
        question = input("You: ")
        if question.lower() == "quit":
            break
        answer = ask_agent(question)
        print(f"\nAgent: {answer}\n")