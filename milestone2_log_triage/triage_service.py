import os
import json
import re
from typing import List
from enum import Enum
from pydantic import BaseModel, Field
import google.generativeai as genai
from dotenv import load_dotenv

# Load credentials
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))

# Configure Gemini
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("[ERROR] GEMINI_API_KEY is not set. Please set it in your .env file.")
    exit(1)
genai.configure(api_key=api_key)

# 1. Define the Structured Output Schema using Pydantic
class SeverityLevel(str, Enum):
    INFO = "INFO"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

class LogTriageAlert(BaseModel):
    is_incident: bool = Field(
        description="True if this log represents an actionable system error, security threat, or critical failure. False for informational messages or routine actions."
    )
    severity: SeverityLevel = Field(
        description="Assessed urgency/severity level based on operational impact."
    )
    category: str = Field(
        description="Category of the log (e.g., DATABASE, CACHE, AUTHENTICATION, NETWORK, RUNTIME_EXCEPTION, SECURITY, GENERAL)."
    )
    root_cause_explanation: str = Field(
        description="Clear explanation of the underlying problem. If is_incident is False, briefly state that it is normal operation."
    )
    suggested_fix: str = Field(
        description="Actionable, step-by-step guidance to resolve the issue for backend developers or SREs. If not an incident, leave blank."
    )

def parse_log_file(filepath: str) -> List[str]:
    """
    Parses a log file and groups multi-line stack traces into single operational events.
    """
    events = []
    current_event = []
    
    # Matches starting timestamp like [2026-06-06 10:15:30]
    log_start_pattern = re.compile(r"^\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\]")
    
    if not os.path.exists(filepath):
        print(f"[ERROR] Log file not found: {filepath}")
        return []

    with open(filepath, "r") as f:
        for line in f:
            if log_start_pattern.match(line):
                if current_event:
                    events.append("".join(current_event).strip())
                    current_event = []
                current_event.append(line)
            else:
                current_event.append(line)
                
        if current_event:
            events.append("".join(current_event).strip())
            
    return events

def triage_log_event(log_event: str) -> LogTriageAlert:
    """
    Sends a log event to Gemini and forces it to respond according to the LogTriageAlert schema.
    """
    model_name = "gemini-1.5-flash"
    
    system_instruction = (
        "You are an AI SRE Copilot running in a production Kubernetes namespace. "
        "Your task is to analyze application log entries, determine if they constitute an incident "
        "requiring developer attention, assign a severity level, explain the root cause, and provide a clear fix."
    )
    
    # We pass the Pydantic schema in the generation config.
    # Gemini will inspect the BaseModel fields and enforce that the output JSON conforms exactly to this structure.
    model = genai.GenerativeModel(
        model_name=model_name,
        system_instruction=system_instruction
    )
    
    prompt = f"Analyze the following log entry:\n\n{log_event}"
    
    response = model.generate_content(
        prompt,
        generation_config=genai.types.GenerationConfig(
            response_mime_type="application/json",
            response_schema=LogTriageAlert,
            temperature=0.0 # Force deterministic output to strictly follow schema
        )
    )
    
    # Parse the response text as JSON and load it into our Pydantic model
    try:
        data = json.loads(response.text)
        return LogTriageAlert(**data)
    except Exception as e:
        print(f"[ERROR] Failed to parse structured JSON from Gemini. Raw text: {response.text}")
        raise e

if __name__ == "__main__":
    log_path = os.path.join(os.path.dirname(__file__), "sample_logs.log")
    print(f"Parsing log file: {log_path}")
    log_events = parse_log_file(log_path)
    
    print(f"Found {len(log_events)} log events. Triaging with Gemini...")
    
    incidents_count = 0
    for i, event in enumerate(log_events, 1):
        print(f"\n--- Event #{i} Analysis ---")
        # Print a short preview of the log line
        first_line = event.split('\n')[0]
        print(f"Log Preview: {first_line}...")
        
        triage_report = triage_log_event(event)
        
        if triage_report.is_incident:
            incidents_count += 1
            print(f"🚨 ACTION REQUIRED: Incident Detected!")
            print(f"   Severity: {triage_report.severity.value}")
            print(f"   Category: {triage_report.category}")
            print(f"   Root Cause: {triage_report.root_cause_explanation}")
            print(f"   Suggested Fix:\n{triage_report.suggested_fix}")
        else:
            print(f"✅ Normal Log: {triage_report.root_cause_explanation}")
            
    print(f"\n==========================================")
    print(f"Triage Complete: Triaged {len(log_events)} logs. Found {incidents_count} active incidents.")
    print(f"==========================================")
