import os
import glob
import numpy as np
import google.generativeai as genai
from dotenv import load_dotenv

# Load credentials
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("[ERROR] GEMINI_API_KEY is not set. Please set it in your .env file.")
    exit(1)
genai.configure(api_key=api_key)

class RAGEngine:
    def __init__(self, docs_dir: str):
        self.docs_dir = docs_dir
        self.chunks = []
        self.embeddings = []

    def load_and_chunk_documents(self):
        """Reads text files in docs_dir and splits them into logical paragraph chunks."""
        search_path = os.path.join(self.docs_dir, "*.txt")
        files = glob.glob(search_path)
        
        if not files:
            print(f"[WARNING] No text documents (.txt) found in {self.docs_dir}")
            return
            
        print(f"Reading documentation files from: {self.docs_dir}")
        for filepath in files:
            filename = os.path.basename(filepath)
            with open(filepath, "r") as f:
                content = f.read()
                
            # Split by double-newlines to keep paragraphs/sections together
            raw_chunks = content.split("\n\n")
            for chunk in raw_chunks:
                clean_chunk = chunk.strip()
                if len(clean_chunk) > 30: # Ignore short whitespace/headers
                    self.chunks.append({
                        "source": filename,
                        "text": clean_chunk
                    })
                    
        print(f"Successfully loaded and split documents into {len(self.chunks)} text chunks.")

    def generate_embeddings(self):
        """Generates embeddings for all text chunks using Gemini text-embedding-004."""
        if not self.chunks:
            print("[ERROR] No chunks to embed. Load documents first.")
            return

        print("Generating embeddings via Gemini API (models/text-embedding-004)...")
        texts = [chunk["text"] for chunk in self.chunks]
        
        # Batch embed contents to optimize API calls
        # Task type 'retrieval_document' is optimized for indexing documents
        result = genai.embed_content(
            model="models/text-embedding-004",
            content=texts,
            task_type="retrieval_document"
        )
        
        # Storing embeddings as a numpy array for easy matrix math
        self.embeddings = np.array(result["embedding"])
        print("Embeddings generation complete.")

    def retrieve_similar_chunks(self, query: str, k: int = 2):
        """
        Embeds the query and computes cosine similarity with document embeddings.
        Returns the top k matching chunks.
        """
        # Embed the search query
        # Task type 'retrieval_query' is optimized for search query strings
        query_embedding_result = genai.embed_content(
            model="models/text-embedding-004",
            content=query,
            task_type="retrieval_query"
        )
        query_vector = np.array(query_embedding_result["embedding"])
        
        # Normalize vectors for cosine similarity
        # Cosine similarity = dot(A, B) / (norm(A) * norm(B))
        dot_products = np.dot(self.embeddings, query_vector)
        chunk_norms = np.linalg.norm(self.embeddings, axis=1)
        query_norm = np.linalg.norm(query_vector)
        
        similarities = dot_products / (chunk_norms * query_norm)
        
        # Get indices of top k similarity scores
        top_k_indices = np.argsort(similarities)[::-1][:k]
        
        retrieved = []
        for index in top_k_indices:
            retrieved.append({
                "chunk": self.chunks[index],
                "score": float(similarities[index])
            })
            
        return retrieved

    def query_with_context(self, question: str):
        """Retrieves context and sends grounded prompt to Gemini."""
        # Retrieve the top 2 matching text chunks
        top_matches = self.retrieve_similar_chunks(question, k=2)
        
        print("\n--- RETRIEVED CONTEXT CHUNKS ---")
        for match in top_matches:
            print(f"Source: {match['chunk']['source']} (Score: {match['score']:.4f})")
            print(f"Content Preview: {match['chunk']['text'][:150]}...")
            print("-" * 30)
            
        # Build the context block
        context_block = "\n\n".join([match["chunk"]["text"] for match in top_matches])
        
        # Prompt engineering: ground the model's answer in the retrieved context
        system_instruction = (
            "You are a professional Google Cloud Solutions Architect. "
            "Answer the user's architectural questions relying ONLY on the provided Context. "
            "If the answer cannot be answered from the context, state: 'I cannot find the answer in the provided documents.'"
        )
        
        prompt = f"""Use the following Context to answer the Question.

Context:
{context_block}

Question: {question}

Answer:"""

        # Call the LLM
        model = genai.GenerativeModel("gemini-1.5-flash", system_instruction=system_instruction)
        response = model.generate_content(prompt, generation_config=genai.types.GenerationConfig(temperature=0.2))
        
        print("\n[Grounded Gemini Architecture Answer]:")
        print(response.text)
        print("=" * 60)

if __name__ == "__main__":
    docs_dir_path = os.path.join(os.path.dirname(__file__), "gcp_docs")
    
    # Initialize engine
    rag = RAGEngine(docs_dir=docs_dir_path)
    rag.load_and_chunk_documents()
    rag.generate_embeddings()
    
    # Test Query 1: Cloud SQL database limits
    query_db = "What is the maximum storage limit and scaling options for Cloud SQL?"
    print(f"\n==========================================")
    print(f"USER QUERY: {query_db}")
    print(f"==========================================")
    rag.query_with_context(query_db)
    
    # Test Query 2: Serverless compute options
    query_compute = "When should I choose Cloud Run instead of GKE for my backend APIs?"
    print(f"\n==========================================")
    print(f"USER QUERY: {query_compute}")
    print(f"==========================================")
    rag.query_with_context(query_compute)

    # Test Query 3: Information not in context
    query_missing = "How do I configure active-active database replication on GCP?"
    print(f"\n==========================================")
    print(f"USER QUERY: {query_missing}")
    print(f"==========================================")
    rag.query_with_context(query_missing)
