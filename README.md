# Kreo Support Agent

A retrieval-augmented (RAG) customer support agent built for Kreo, an Indian gaming and content-creator gear brand. Answers customer questions using only information grounded in Kreo's actual product documentation — refuses to answer, rather than guess, when it can't find a confident match. Deployed as a web API (FastAPI) with a working browser chat frontend, and validated against an automated evaluation suite.

## How it works

1. **Ingestion** (`ingest.py`) — Kreo's product documentation (FAQ, shipping/refund policy, warranty, product-specific docs) is split into chunks using a custom QA-aware chunker: it detects question boundaries and section headers with regex, and merges any fragment that's too short to stand alone. Chunks are then vectorized with TF-IDF (`scikit-learn`) and saved to a local index (`index.pkl`).
2. **Retrieval** (`agent.py: retrieve_context`) — an incoming question is vectorized with the same TF-IDF model, then compared against every chunk using cosine similarity. The top 3 most similar chunks are pulled as context.
3. **Confidence gate** — if even the best-matching chunk scores below a similarity threshold (`0.15`), the agent does **not** attempt an answer. It returns a clear "I don't have that information" response and directs the customer to Kreo's WhatsApp support instead of guessing.
4. **Generation** (`agent.py: ask_agent`) — if a confident match is found, the retrieved context is passed to Llama 3.1 8B (via the Groq API) with an explicit instruction: answer only from the given context, and never borrow specs, warranty terms, or instructions from a different, unrelated Kreo product.
5. **Logging** (`logger.py`) — every conversation is logged to a local SQLite database, including cases where no confident match was found — so gaps in the knowledge base are visible over time, not silent.
6. **API layer** (`server.py`) — the agent is exposed as a FastAPI web service with a `POST /chat` endpoint. Includes a `GET /` health-check endpoint and CORS middleware for browser access.
7. **Frontend** (`index.html`) — a simple vanilla JS/HTML chat interface that calls the `/chat` endpoint and renders the conversation.

## Evaluation

`eval_questions.py` defines a 30-question test set spanning returns, shipping, warranty, payments, and specific products (Mirage controller, Chimera mouse, Hive keyboard) — plus deliberate out-of-scope questions ("what is Kreo's revenue?", "what's the weather today?") to test that the agent correctly refuses rather than hallucinates.

`run_eval.py` runs the full set against the live agent and reports a pass/fail score based on expected keyword matches, so retrieval and prompt changes can be checked against a consistent benchmark instead of eyeballing individual responses.

## Why the confidence threshold matters

The riskiest failure mode for a support agent isn't "I don't know" — it's confidently giving the wrong answer, especially by mixing up specs between two different products. The threshold check exists specifically to catch that: if the retrieval step isn't confident the right information was found, the agent refuses to answer rather than improvising. The evaluation suite includes explicit tests for this. This mirrors a broader principle I apply across my automation projects: AI systems should be designed to know when *not* to act alone.

## Tech stack

- Python
- FastAPI + Uvicorn (web API layer)
- scikit-learn (TF-IDF vectorization, cosine similarity)
- Groq API (Llama 3.1 8B Instant) for answer generation
- SQLite (conversation logging)
- Vanilla JS/HTML (frontend)

## Files

| File | Purpose |
|---|---|
| `ingest.py` | Custom QA-aware chunking + TF-IDF index builder |
| `agent.py` | Core retrieval + generation logic |
| `server.py` | FastAPI web server exposing the agent as a `/chat` API endpoint |
| `index.html` | Browser chat frontend |
| `logger.py` | SQLite conversation logging |
| `eval_questions.py` | 30-question evaluation set, including hallucination/refusal tests |
| `run_eval.py` | Automated evaluation harness — runs the eval set and reports a pass rate |
| `check_log.py` | Utility for spot-checking specific logged conversations |
| `requirements.txt` | Python dependencies |

**Note:** `check_distances.py` and `inspect_chunks.py` are exploratory scripts from an earlier prototype that used ChromaDB with sentence-transformer embeddings instead of TF-IDF. They're kept in the repo for reference but aren't part of the current pipeline (their dependencies aren't in `requirements.txt`).

## Run it

```bash
pip install -r requirements.txt
# set GROQ_API_KEY in a .env file
python ingest.py           # build the index (first run only)
uvicorn server:app --reload
```
Then open `index.html` in a browser, or send a request directly:
```bash
curl -X POST http://127.0.0.1:8000/chat -H "Content-Type: application/json" -d '{"message": "your question here"}'
```

To run the evaluation suite:
```bash
python run_eval.py
```

## What I'd improve next

- Add conversation memory so follow-up questions retain context (currently each question is answered independently)
- Revisit embedding-based retrieval (the earlier ChromaDB prototype) for better semantic matching on paraphrased questions, now benchmarked against the eval suite instead of judged by eye
- Tune the similarity threshold against a larger, labeled set of real customer questions
- Restrict CORS to a specific frontend origin instead of allowing all origins, before any real deployment


