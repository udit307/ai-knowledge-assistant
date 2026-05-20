import json
from pathlib import Path
from datetime import datetime


LOG_FILE = Path("logs/query_logs.json")


def log_query(
    question,
    answer,
    latency,
    retrieved_chunks
):

    log_entry = {

        "timestamp": datetime.now().isoformat(),

        "question": question,

        "answer": answer,

        "latency_seconds": latency,

        "retrieved_chunks": retrieved_chunks
    }

    # Load existing logs
    if LOG_FILE.exists():

        with open(LOG_FILE, "r", encoding="utf-8") as f:

            logs = json.load(f)

    else:

        logs = []

    logs.append(log_entry)

    # Save updated logs
    with open(LOG_FILE, "w", encoding="utf-8") as f:

        json.dump(logs, f, indent=2)