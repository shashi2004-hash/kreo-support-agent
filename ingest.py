import re
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer

def chunk_by_qa(text):
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

def load_all_chunks():
    files = [
        ("data/faq.txt", "faq"),
        ("data/shipping_refund.txt", "shipping_refund"),
        ("data/warranty.txt", "warranty"),
        ("data/chair_warranty.txt", "chair_warranty"),
    ]
    all_chunks = []
    all_sources = []
    for filepath, source in files:
        with open(filepath, "r", encoding="utf-8") as f:
            text = f.read()
        chunks = chunk_by_qa(text)
        all_chunks.extend(chunks)
        all_sources.extend([source] * len(chunks))
        print(f"Ingested {len(chunks)} chunks from {source}")
    return all_chunks, all_sources

if __name__ == "__main__":
    chunks, sources = load_all_chunks()

    vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
    tfidf_matrix = vectorizer.fit_transform(chunks)

    with open("index.pkl", "wb") as f:
        pickle.dump({
            "vectorizer": vectorizer,
            "matrix": tfidf_matrix,
            "chunks": chunks,
            "sources": sources
        }, f)

    print(f"Done! Total chunks indexed: {len(chunks)}")