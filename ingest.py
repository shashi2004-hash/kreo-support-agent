import re
import chromadb
from chromadb.utils import embedding_functions

embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

client = chromadb.PersistentClient(path="./chroma_db")

# Delete old collection so we don't mix old bad chunks with new good ones
try:
    client.delete_collection("kreo_support")
except Exception:
    pass

collection = client.get_or_create_collection(
    name="kreo_support",
    embedding_function=embedding_fn
)

def chunk_by_qa(text):
    """Groups each question with its answer into one chunk, instead of
    cutting text every N characters."""
    lines = [l.rstrip() for l in text.split("\n")]
    chunks = []
    current = []

    def is_question_start(line):
        s = line.strip()
        if not s:
            return False
        if s.endswith("?"):
            return True
        if re.match(r"^\d+\.\s", s):
            return True
        return False

    def is_section_header(line):
        s = line.strip()
        if not s:
            return False
        return len(s.split()) <= 5 and not s.endswith((".", "?", ":")) and not re.match(r"^\d+\.", s)

    for line in lines:
        s = line.strip()
        if not s:
            continue
        if is_question_start(s):
            if current:
                chunks.append("\n".join(current).strip())
            current = [s]
        elif is_section_header(s) and current and not is_question_start(current[0]):
            if current:
                chunks.append("\n".join(current).strip())
            current = [s]
        else:
            current.append(s)

    if current:
        chunks.append("\n".join(current).strip())

    # merge tiny fragments (like lone headers) into the next chunk
    merged = []
    buffer = ""
    for c in chunks:
        if len(c) < 30:
            buffer = c
            continue
        if buffer:
            c = buffer + "\n" + c
            buffer = ""
        merged.append(c)
    if buffer:
        merged.append(buffer)

    return merged

def ingest_file(filepath, source_name):
    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()

    chunks = chunk_by_qa(text)
    ids = [f"{source_name}_{i}" for i in range(len(chunks))]
    metadatas = [{"source": source_name} for _ in chunks]

    collection.add(
        documents=chunks,
        ids=ids,
        metadatas=metadatas
    )
    print(f"Ingested {len(chunks)} chunks from {source_name}")

ingest_file("data/faq.txt", "faq")
ingest_file("data/shipping_refund.txt", "shipping_refund")
ingest_file("data/warranty.txt", "warranty")
ingest_file("data/chair_warranty.txt", "chair_warranty")

print("Done! Total chunks in DB:", collection.count())