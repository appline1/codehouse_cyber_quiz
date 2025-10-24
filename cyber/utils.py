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
    c.execute("DROP TABLE IF EXISTS results")
    c.execute("""
        CREATE TABLE results(
            sti TEXT,
            question TEXT,
            student_answer TEXT,
            is_correct INTEGER
        )
    """)
    conn.commit()
    conn.close()


def save_to_db(sti, question, student_answer,  is_correct):
    conn = sqlite3.connect(LOCAL_DB)
    c = conn.cursor()
    c.execute("INSERT INTO results VALUES (?, ?, ?, ?)",
              (sti, question, student_answer,  int(is_correct)))
            #   (sti, question, student_answer, correct_answer, int(is_correct), timestamp()))
    conn.commit()
    conn.close()

def export_csv(file_path: Path):
    conn = sqlite3.connect(LOCAL_DB)
    rows = conn.execute("SELECT * FROM results").fetchall()
    with open(file_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["STI", "Question", "Student Answer", "Correct"])
        writer.writerows(rows)
    conn.close()
    console.print(f"[green]Exported to {file_path}[/green]")

import os

def send_remote_log(token, payload):
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    try:
        # if os.environ.get("LOCAL_MODE") == "true":
        #     response = requests.post(API_LOG, json=payload, headers=headers, timeout=REMOTE_TIMEOUT)
        # else:
        response = requests.post(API_LOG, data=payload, headers=headers, timeout=REMOTE_TIMEOUT)

        if response.status_code == 200:
            console.print("[green]Remote log successful[/green]")
        else:
            console.print()
    except Exception as e:
        console.print(f"[yellow]Remote log failed: {e}[/yellow]")

# def send_remote_log(token, payload):
#     """
#     Send result payload to remote server API_LOG. If offline, print a yellow message.
#     """
#     headers = {"Authorization": f"Bearer {token}"} if token else {}
#     try:
#         response = requests.post(API_LOG, data=payload, headers=headers, timeout=REMOTE_TIMEOUT)
#         if response.status_code == 200:
#             console.print("[green]Remote log successful[/green]")
#         else:
#             console.print(f"[red]Remote log failed: {response.status_code} [/red]")
#     except Exception as e:
#         console.print(f"[yellow]Remote log failed: {e}[/yellow]")

def fetch_questions():
    """
    Returns questions list or raises exception on network error.
    """
    try:
        resp = requests.get(__import__(".".join([".config"]).lstrip(".")))
    except Exception:
        # We'll use direct import above in quiz file. Kept here as placeholder.
        raise
