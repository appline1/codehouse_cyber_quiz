import sqlite3, csv
from datetime import datetime
from pathlib import Path
import requests
from rich.console import Console
from .config import LOCAL_DB, API_LOG, REMOTE_TIMEOUT

console = Console()

def timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def init_db():
    conn = sqlite3.connect(LOCAL_DB)
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS results(
        sti TEXT, question TEXT, student_answer TEXT,
        correct_answer TEXT, is_correct INTEGER,
        timestamp TEXT
    )""")
    conn.commit()
    conn.close()

def save_to_db(sti, question, student_answer, correct_answer, is_correct):
    conn = sqlite3.connect(LOCAL_DB)
    c = conn.cursor()
    c.execute("INSERT INTO results VALUES (?, ?, ?, ?, ?, ?)",
              (sti, question, student_answer, correct_answer, int(is_correct), timestamp()))
    conn.commit()
    conn.close()

def export_csv(file_path: Path):
    conn = sqlite3.connect(LOCAL_DB)
    rows = conn.execute("SELECT * FROM results").fetchall()
    with open(file_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["STI", "Question", "Student Answer", "Correct Answer", "Correct", "Timestamp"])
        writer.writerows(rows)
    conn.close()
    console.print(f"[green]Exported to {file_path}[/green]")

def send_remote_log(token, payload):
    """
    Send result payload to remote server API_LOG. If offline, print a yellow message.
    """
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    try:
        requests.post(API_LOG, json=payload, headers=headers, timeout=REMOTE_TIMEOUT)
    except Exception as e:
        console.print(f"[yellow]Remote log failed: {e}[/yellow]")

def fetch_questions():
    """
    Returns questions list or raises exception on network error.
    """
    try:
        resp = requests.get(__import__(".".join([".config"]).lstrip(".")))
    except Exception:
        # We'll use direct import above in quiz file. Kept here as placeholder.
        raise
