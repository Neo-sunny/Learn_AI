# Milestone 4: Code Auditing & Anomaly Detection (Security)

In this milestone, you will build a security scanner that uses Gemini to analyze source code files for potential security vulnerabilities (such as OWASP Top 10 risks, hardcoded credentials, and SQL injection vulnerabilities).

---

## 💡 Key Security Concepts

1. **Semantic Code Analysis**: Traditional static application security testing (SAST) tools rely on regex or Abstract Syntax Trees (AST) to find patterns. They often produce high false positive rates and struggle with logical security flaws.
2. **LLM Security Scanning**: LLMs can understand the semantic intent of code. They are highly effective at finding:
   - **SQL Injection**: Detecting where variables are directly concatenated into query strings instead of parameterized.
   - **Hardcoded Secrets**: Spotting passwords, API tokens, and credentials in the source code.
   - **XSS & Unvalidated Input**: Spotting where user input is rendered directly without sanitization.
   - **Unsafe Libraries/Algorithms**: Flagging the use of deprecated cryptographic functions (like MD5 or SHA1 for passwords).

---

## 🛠️ Files

- **[`security_scanner.py`](file:///Users/krishabhi/Downloads/AI/genai-backend-learning/milestone4_security_audit/security_scanner.py)**: The python security auditor. It reads a source file, constructs a security audit prompt, queries Gemini, and outputs a formatted security audit report.

---

## 🚀 Running the Exercise

Activate your virtual environment and run the scanner on its own file or create a vulnerable file to test:
```bash
python milestone4_security_audit/security_scanner.py
```

---

## 🧠 Hands-on Challenges for You

1. **Test with Unsafe Code**: Create a file named `vulnerable_api.py` with the following contents:
   ```python
   import sqlite3
   
   def login_user(username, password):
       # VULNERABLE: Direct string interpolation (SQL Injection)
       query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
       conn = sqlite3.connect("users.db")
       return conn.execute(query).fetchall()
       
   # VULNERABLE: Hardcoded API Key
   API_SECRET = "sk_live_51NzABC123XYZ"
   ```
   Run the scanner against this file:
   ```bash
   python milestone4_security_audit/security_scanner.py vulnerable_api.py
   ```
   Verify that Gemini flags both the SQL injection and the hardcoded secret.
2. **Structured JSON Security Audit**: Rewrite the script to return a structured JSON report (similar to Milestone 2) outlining the list of vulnerabilities found, their severity, line numbers, and proposed safe refactoring code.
