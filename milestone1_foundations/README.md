# Milestone 1: Foundations & API Mechanics

In this milestone, you will learn the core concepts of working with Large Language Models (LLMs) via the Google Gemini API using Python.

---

## 💡 Key Concepts

1. **System Instructions**: Guide the model's behavior, tone, style, or constraints throughout the conversation.
2. **Generation Configuration**:
   - **Temperature**: Controls randomness (lower = more deterministic, higher = more creative/random).
   - **Top-K / Top-P**: Controls token sampling pools.
   - **Max Output Tokens**: Limits the response length.
3. **Safety Settings**: Configure thresholds for blocking content related to harassment, hate speech, sexual content, or dangerous activities.
4. **Exception Handling**: Catching network problems, missing API keys, or HTTP errors (e.g. ResourceExhausted for rate limits).

---

## 🛠️ Files

- **[`gemini_client.py`](file:///Users/krishabhi/Downloads/AI/genai-backend-learning/milestone1_foundations/gemini_client.py)**: Boilerplate code that reads `.env` variables, configures the Gemini client, defines helper functions to talk to Gemini, and includes robust error handling.

---

## 🚀 Running the Exercise

Make sure you've completed the environment setup in the root `README.md` and created your `.env` file with `GEMINI_API_KEY`.

Run the client script:
```bash
python milestone1_foundations/gemini_client.py
```

---

## 🧠 Hands-on Challenges for You
Try modifying `gemini_client.py` to:
1. **Change the Temperature**: Set the temperature to `0.0` for highly structured answers (critical for JSON APIs) or `1.0` for creative brainstorming, and observe the difference in responses.
2. **Add a Custom System Instruction**: Change the system instruction to make Gemini behave like a specific persona (e.g. a terse, strict Unix systems administrator or a GCP Cloud Architect).
3. **Trigger Rate Limiting / Handle Errors**: Learn how API errors are caught by calling the model with invalid configurations or simulating API failures.
