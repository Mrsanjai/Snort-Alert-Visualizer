import os
import re
from datetime import datetime
from app.config import Config

LOG_ROOT = Config.LOG_ROOT_DIR  # Use configured Snort log folder

def parse_snort_logs():
    all_logs = []

    for root, dirs, files in os.walk(LOG_ROOT):
        for file in files:
            if file.lower().endswith(('.log', '.ids')):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    for line in f:
                        parsed = parse_log_line(line.strip())
                        if parsed:
                            all_logs.append(parsed)

    return all_logs

def parse_log_line(line):
    """
    Parses a Snort log line and returns a dictionary with fields:
    timestamp, severity, message, src_ip, dest_ip
    """
    try:
        # Use current timestamp (Snort logs often don't have timestamps)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Extract severity (priority <= 2 = high)
        severity_match = re.search(r'\[Priority: (\d+)\]', line)
        severity = 'high' if severity_match and int(severity_match.group(1)) <= 2 else 'low'

        # Extract alert message
        msg_match = re.search(r'\[\*\*\] \[.*?\] (.*?) \[\*\*\]', line)
        message = msg_match.group(1).strip() if msg_match else "Unrecognized alert"

        # Extract IP addresses
        ip_match = re.search(r'(\d{1,3}(?:\.\d{1,3}){3})\s*->\s*(\d{1,3}(?:\.\d{1,3}){3})', line)
        src_ip = ip_match.group(1) if ip_match else "Unknown"
        dest_ip = ip_match.group(2) if ip_match else "Unknown"

        return {
            "timestamp": timestamp,
            "severity": severity,
            "message": message,
            "src_ip": src_ip,
            "dest_ip": dest_ip
        }

    except Exception:
        return None
