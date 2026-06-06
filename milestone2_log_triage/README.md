# Milestone 2: Intelligent Alert Triaging & Debugging

In this milestone, you will learn how to make Gemini return **Structured Outputs** (JSON conforming to a strict schema). This is one of the most critical techniques for integrating AI models into backend workflows, APIs, and microservices.

---

## 💡 Key Concept: Structured Outputs

When building backend systems, you cannot rely on free-form text because:
- Regex parsing of text is brittle and breaks when the LLM modifies its tone or output structure.
- You need structured keys (e.g., `{ "severity": "ERROR" }`) to route alerts, write to databases, or trigger downstream actions.

By using Gemini's **Structured Output** feature, we can pass a **Pydantic model** to the SDK. The model guarantees that the response from the LLM will be valid JSON that parses exactly into our schema.

---

## 🛠️ Files

- **[`sample_logs.log`](file:///Users/krishabhi/Downloads/AI/genai-backend-learning/milestone2_log_triage/sample_logs.log)**: A log file containing various backend system entries: stack traces, DB timeouts, authentication failures, and standard info logs.
- **[`triage_service.py`](file:///Users/krishabhi/Downloads/AI/genai-backend-learning/milestone2_log_triage/triage_service.py)**: The python service that reads this log file, calls Gemini with a Pydantic schema constraint, and prints out a structured summary of triaged incidents.

---

## 🚀 Running the Exercise

Activate your virtual environment and run:
```bash
python milestone2_log_triage/triage_service.py
```

---

## 🧠 Hands-on Challenges for You
1. **Extend the Schema**: Open `triage_service.py` and modify the `LogTriageAlert` Pydantic class. Add a new field: `estimated_resolution_effort` (an Enum: `LOW`, `MEDIUM`, `HIGH`) and see how Gemini categorizes it.
2. **Filter & Route**: Add logic in python to filter alerts (e.g., only trigger a simulated Slack webhook/alert if the returned `severity` is `CRITICAL` or `HIGH`).
3. **Analyze Multi-line Stack Traces**: Look at `sample_logs.log` and add a new multi-line traceback (e.g. an OutOfMemoryError in Java or RecursionError in Python) to see how the model generalizes to different programming languages.
