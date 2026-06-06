import os
import sys
import google.generativeai as genai
from dotenv import load_dotenv

# Load credentials
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("[ERROR] GEMINI_API_KEY is not set. Please set it in your .env file.")
    exit(1)
genai.configure(api_key=api_key)

# A sample vulnerable code snippet to scan by default if no file is provided
DEFAULT_VULNERABLE_CODE = """
import sqlite3
import hashlib

def authenticate_user(username, password):
    # Finding 1: Vulnerable to SQL Injection (Direct string formatting)
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute(query)
    user = cursor.fetchone()
    return user

def hash_user_password(password):
    # Finding 2: Using a weak, deprecated hash algorithm (MD5)
    hasher = hashlib.md5()
    hasher.update(password.encode('utf-8'))
    return hasher.hexdigest()

# Finding 3: Hardcoded API token / credentials in source file
STRIPE_API_KEY = "sk_live_51NABC12345XYZsecrettoken"
"""

def scan_code(code_content: str, filename: str):
    """
    Sends the code content to Gemini, acting as a Senior Security Engineer,
    and returns a vulnerability audit report.
    """
    model_name = "gemini-1.5-flash"
    
    system_instruction = (
        "You are an expert Security Engineer and Static Code Analyst. "
        "Your task is to review source code files for safety vulnerabilities, "
        "including SQL injections, hardcoded secrets, cross-site scripting (XSS), "
        "weak cryptography, and bad auth logic. "
        "Format your response in clear Markdown with the following sections:\n"
        "1. Executive Summary (Overall Risk Rating: LOW/MEDIUM/HIGH)\n"
        "2. Detailed Findings (Vulnerability name, Severity, Line context, Explanation, and Remediated Code)\n"
        "3. Security Best Practices Recommendations."
    )
    
    model = genai.GenerativeModel(
        model_name=model_name,
        system_instruction=system_instruction
    )
    
    prompt = f"Perform a security audit on the following source file: '{filename}'\n\nCode Contents:\n```python\n{code_content}\n```"
    
    print(f"Auditing code for '{filename}' using Gemini...")
    response = model.generate_content(
        prompt,
        generation_config=genai.types.GenerationConfig(temperature=0.1) # Low temperature for analytical response
    )
    
    print("\n========================================================")
    print(f"🔒 SECURITY AUDIT REPORT FOR: {filename}")
    print("========================================================")
    print(response.text)
    print("========================================================\n")

if __name__ == "__main__":
    # If a filename is passed as a CLI argument, scan that file.
    # Otherwise, scan the default vulnerable code snippet.
    if len(sys.argv) > 1:
        target_file = sys.argv[1]
        if not os.path.exists(target_file):
            print(f"[ERROR] Target file not found: {target_file}")
            sys.exit(1)
            
        print(f"Reading target file: {target_file}")
        with open(target_file, "r") as f:
            code_to_scan = f.read()
        filename_to_display = os.path.basename(target_file)
    else:
        print("No target file provided. Scanning default vulnerable mock code snippet...")
        code_to_scan = DEFAULT_VULNERABLE_CODE
        filename_to_display = "mock_auth_service.py"
        
    scan_code(code_to_scan, filename_to_display)
