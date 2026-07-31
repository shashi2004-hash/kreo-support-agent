import chromadb
from chromadb.utils import embedding_functions

embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(
    name="kreo_support",
    embedding_function=embedding_fn
)

all_chunks = collection.get()
keywords = ["turbo", "mirage", "chimera", "hive", "battery", "switches", "bluetooth"]

for i, doc in enumerate(all_chunks["documents"]):
    source = all_chunks["metadatas"][i]["source"]
    if source == "faq" and any(kw in doc.lower() for kw in keywords):
        print(f"--- Chunk {i} (faq) ---")
        print(doc)
        print()