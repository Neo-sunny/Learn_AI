# Milestone 3: RAG (Retrieval-Augmented Generation) for GCP Cloud Architecture

In this milestone, you will build a lightweight **Retrieval-Augmented Generation (RAG)** pipeline. This pattern is essential when you want an LLM to answer questions using private documents, internal guidelines, or the latest cloud documentation that the model wasn't trained on.

---

## 💡 Key RAG Concepts

1. **Knowledge Gap**: LLMs have training cutoffs and cannot know your private enterprise designs or dynamic cloud guides.
2. **Retrieval**: Instead of fine-tuning the model (which is expensive and slow), we retrieve relevant text chunks from a database based on a user's question.
3. **Embeddings**: High-dimensional vectors representing the semantic meaning of text. We use the Gemini API's `text-embedding-004` model.
4. **Vector Similarity**: We use cosine similarity (via `numpy`) to find which document chunks are closest in meaning to the user's search query.
5. **Grounding (Augmented Generation)**: We inject the retrieved text chunks as context in the prompt, instructing the LLM: *"Answer the question using ONLY the provided context."* This reduces hallucinations dramatically.

---

## 📂 Folder Structure

- **[`gcp_docs/`](file:///Users/krishabhi/Downloads/AI/genai-backend-learning/milestone3_rag_gcp/gcp_docs/)**: Place text files here with database comparisons, architectural rules, and serverless guides.
- **[`rag_engine.py`](file:///Users/krishabhi/Downloads/AI/genai-backend-learning/milestone3_rag_gcp/rag_engine.py)**: The Python pipeline that chunks files, generates vectors using Gemini, calculates similarity, retrieves matches, and queries Gemini.

---

## 🚀 Running the Exercise

Make sure you have text files in the `gcp_docs/` folder. Activate your virtual environment and run:
```bash
python milestone3_rag_gcp/rag_engine.py
```

---

## 🧠 Hands-on Challenges for You

1. **Add Custom Documents**: Add a new text file to `gcp_docs/` describing your company's own microservices stack or cloud network configuration. Run the engine and ask questions about it.
2. **Tune Retrieve Parameters (`K`)**: In `rag_engine.py`, change the value of `k` (the number of retrieved text chunks). Observe how retrieving more or fewer chunks impacts the quality and detail of the final answer.
3. **Evaluate Embeddings**: Modify `rag_engine.py` to embed two short sentences (e.g. "Cloud SQL is a relational database" and "Postgres runs on GCP") and compare their cosine similarity score against two unrelated sentences.
