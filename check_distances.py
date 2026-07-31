import chromadb
from chromadb.utils import embedding_functions

embedding_fn = embedding_functions.DefaultEmbeddingFunction()
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(
    name="kreo_support",
    embedding_function=embedding_fn
)
test_questions = [
    "do you charge for shipping",
    "is warranty valid if I bought from a third-party seller",
    "how do I pair the chimera in bluetooth mode",
    "where is kreo located",         # bad match, for comparison
    "what is the capital of india",  # bad match, for comparison
]   
for q in test_questions:
    results = collection.query(query_texts=[q], n_results=1)
    distance = results["distances"][0][0]
    doc_preview = results["documents"][0][0][:60]
    print(f"Q: {q}")
    print(f"   distance: {distance:.4f}")
    print(f"   top chunk: {doc_preview}...")
    print()