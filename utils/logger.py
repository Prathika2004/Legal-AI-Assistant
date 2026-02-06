import json
import os
from datetime import datetime

LOG_FILE = "data/audit_logs/contract_logs.json"

class AuditLogger:
    @staticmethod
    def save_log(filename, contract_type, risk_score, issues):
        # Ensure directory exists
        os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
        
        log_entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "file_name": filename,
            "contract_type": contract_type,
            "risk_score": risk_score,
            "top_issues": issues[:3] # Store top 3 risks for the knowledge base
        }

        logs = []
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, "r") as f:
                try:
                    logs = json.load(f)
                except json.JSONDecodeError:
                    logs = []

        logs.append(log_entry)
        
        with open(LOG_FILE, "w") as f:
            json.dump(logs, f, indent=4)

    @staticmethod
    def get_logs():
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, "r") as f:
                return json.load(f)
        return []