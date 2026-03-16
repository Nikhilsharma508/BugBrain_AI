"""
src/preprocessing/log_parser.py — Extract Technical Signals
------------------------------------------------------------
PURPOSE:
    Extracts structured technical signals from the filtered text.
    These signals help the LLM focus on the most important parts.

WHAT IT EXTRACTS:
    - Exception/error class names (e.g. java.lang.NullPointerException)
    - Error messages (the text after the exception name)
    - Key stack frames (top 5 lines of each stack trace)
    - Timestamps from log entries

CAPABILITIES (can be extended later):
    - Python traceback parsing
    - JavaScript error parsing
    - Log level detection (ERROR, WARN, INFO)
    - File path + line number extraction
    - Error code extraction (HTTP status, exit codes)

CONNECTS TO:
    preprocessing/__init__.py → runs after noise_filter.filter_noise()
"""

import re

EXCEPTION_PATTERN = re.compile(
    r"(?:(?:Caused by|Exception in thread \".*?\"):\s+)?([\w.]*(?:Exception|Error|Fault|Failure|Panic|ts|TypeMismatch))\s*:?\s*(.*)", 
    re.IGNORECASE
)

STACK_FRAME_PATTERNS = [
    re.compile(r"^\s*\"?\s*at\s+([\w.<>$ ]+)\s*(?:\(|in\s+)?\"?([\w./\\-]+\.[a-z]{2,4}:?\d*:?\d*)\"?\)?", re.MULTILINE | re.IGNORECASE),
    re.compile(r"File\s+\"(.+?)\",\s+line\s+(\d+),\s+in\s+(\w+)", re.IGNORECASE),
    re.compile(r"^([\w./\\-]+\.[a-z]{2,4}):(\d+)", re.MULTILINE),
    re.compile(r"^\s*\"?\s*([\w.$]+)\.([\w$<>]+)\"?\s*\(([\w.]+:\d+)\)", re.MULTILINE)
]

TIMESTAMP_PATTERN = re.compile(
    r"(\d{4}[-/]\d{2}[-/]\d{2}[\sT]\d{2}:\d{2}:\d{2}(?:\.\d+)?)|"
    r"([A-Z][a-z]{2}\s+[A-Z][a-z]{2}\s+\d+\s+\d{2}:\d{2}:\d{2}\s+[\w+:]+\s+\d{4})",
    re.IGNORECASE
)
def extract_signals(text: str) -> dict:
    if not text: return {"exceptions": [], "error_messages": [], "key_stack_frames": [], "timestamps": [], "has_stack_trace": False}

    exceptions, error_messages = [], []
    for match in EXCEPTION_PATTERN.finditer(text):
        name, msg = match.group(1).strip(), match.group(2).strip().replace('"', '')
        if name and name not in exceptions: exceptions.append(name)
        if msg and msg not in error_messages: error_messages.append(msg)

    stack_frames = []
    for pattern in STACK_FRAME_PATTERNS:
        for match in pattern.finditer(text):
            groups = match.groups()
            frame = f"{groups[0]}:{groups[1]}" if len(groups) == 2 else (f"{groups[0]}:{groups[1]} in {groups[2]}" if "line" in match.group(0).lower() else f"{groups[0]}.{groups[1]}({groups[2]})")
            if frame not in stack_frames: stack_frames.append(frame)
            if len(stack_frames) >= 15: break

    return {
        "exceptions": exceptions,
        "error_messages": error_messages,
        "key_stack_frames": stack_frames,
        "timestamps": list(set(TIMESTAMP_PATTERN.findall(text))),
        "has_stack_trace": len(stack_frames) > 0,
    }

if __name__ == "__main__":
    print("--- LOG PARSER TEST ---")
    js_log = "Error: Click failed at submit (button.js:10:5)"
    time = "Log: Fri May 10 11:46:52 GMT+03:00 2002 2 org.eclipse.core.resources 2 Problems oc"
    py_log = 'File "app.py", line 42, in run'
    go_log = "main.go:15: panic: runtime error"
    
    for log in [js_log, time, py_log, go_log]:
        print(f"Input: {log} -> {extract_signals(log)['timestamps']}")