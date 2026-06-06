# Applied GenAI for Backend Systems Learning Workspace

Welcome to your hands-on workspace for building applied GenAI capabilities in backend systems! This repository is organized step-by-step to match your IDP roadmap and target goals: improving logging/alerting, designing better cloud architecture (via RAG), and auditing security.

---

## 🚀 Environment Setup

Follow these steps to set up your local development environment:

### 1. Create a Virtual Environment
Run the following in your terminal to isolate your dependencies:
```bash
python3 -m venv .venv
```

### 2. Activate the Virtual Environment
* **macOS / Linux:**
  ```bash
  source .venv/bin/activate
  ```
* **Windows (Command Prompt):**
  ```cmd
  .venv\Scripts\activate.bat
  ```
* **Windows (PowerShell):**
  ```powershell
  .venv\Scripts\Activate.ps1
  ```

### 3. Install Dependencies
Install the required libraries:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure your Gemini API Key
1. Go to [Google AI Studio](https://aistudio.google.com/) and create a free API Key.
2. Copy `.env.template` to a new file named `.env`:
   ```bash
   cp .env.template .env
   ```
3. Open `.env` in your editor and paste your API key:
   ```env
   GEMINI_API_KEY=your-actual-api-key-here
   ```

---

## 📂 Repository Structure

The workspace is organized into individual milestone folders:

1. **[`milestone1_foundations/`](file:///Users/krishabhi/Downloads/AI/genai-backend-learning/milestone1_foundations/)**: Learn the mechanics of the Gemini API, prompt parameters, system instructions, error handling, and rate limiting.
2. **[`milestone2_log_triage/`](file:///Users/krishabhi/Downloads/AI/genai-backend-learning/milestone2_log_triage/)**: Practice structured output schema by feeding backend application logs into Gemini to output structured JSON alerts.
3. **[`milestone3_rag_gcp/`](file:///Users/krishabhi/Downloads/AI/genai-backend-learning/milestone3_rag_gcp/)**: Build a Retrieval-Augmented Generation (RAG) tool using Gemini Embeddings and vector similarity to answer GCP architecture questions.
4. **[`milestone4_security_audit/`](file:///Users/krishabhi/Downloads/AI/genai-backend-learning/milestone4_security_audit/)**: Write a static analyzer tool that scans source code files using safety prompts to find vulnerabilities (e.g. SQL injections, hardcoded keys).

---

## 📘 Course Tracking (KPI 1)
You can track your progress for the **Google Cloud Skills Boost: Generative AI Learning Path** in [learning_roadmap.md](file:///Users/krishabhi/Downloads/AI/genai-backend-learning/learning_roadmap.md).
