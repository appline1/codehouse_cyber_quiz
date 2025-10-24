import random, requests, json, math
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress
from .config import API_QUESTIONS, SESSION_QUESTION_COUNT, REMOTE_TIMEOUT, API_TOP_USERS
from .fuzzy import is_fuzzy_match
from .utils import save_to_db, send_remote_log, timestamp
from .config import REMOTE_TIMEOUT

console = Console()

def load_questions():
    """
    Fetch questions from server. On network error, fallback to local file cyb/local_questions.json
    """
    try:
        r = requests.get(API_QUESTIONS, timeout=REMOTE_TIMEOUT)
        r.raise_for_status()
        data = r.json()
        # Expect a list
        return data
    except Exception as e:
        console.print(f"[yellow]Could not load questions from server: {e}[/yellow]")
        try:
            with open("cyber/local_questions.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e2:
            console.print(f"[red]Failed to load local questions: {e2}[/red]")
            return []

def format_option_line(index, text):
    return f"{index}. {text}"

def present_question(q, idx, total, sti, token, running_score):
    """
    q: dict with keys: question, options (list), maybe answer_index or answer
    returns True/False for correctness
    """
    qtext = q.get("question") or q.get("text") or "Question text missing"
    options = q.get("options") or q.get("choices") or []
    console.print(Panel.fit(f"[bold]{qtext}[/bold]\n", title=f"Question {idx}/{total}", style="cyan"))
    for i, opt in enumerate(options, start=1):
        console.print(format_option_line(i, opt))

    console.print(f"[grey50]Score: {running_score} / {idx-1} answered ({(running_score / max(1, idx-1))*100:.1f}%)[/grey50]" if idx>1 else "[grey50]No answers yet.[/grey50]")

    while True:
        ans = Prompt.ask("Type option number (or 'done' to finish, 'top' to view leaderboard, 'exit' to quit)").strip()
        if ans.lower() in ("done", "exit", "stop"):
            return None  # signals early exit
        if ans.lower() == "top":
            show_top_users()
            continue
        if not ans.isdigit():
            console.print("[red]Please enter a number corresponding to an option.[/red]")
            continue
        choice = int(ans) - 1
        if choice < 0 or choice >= len(options):
            console.print("[red]Option out of range.[/red]")
            continue

        # Determine correct answer from q
        correct_flag = False
        # Accept server-provided index
        if "answer_index" in q:
            correct_flag = (choice == q["answer_index"])
        elif "answer" in q:
            # either a string value or index
            if isinstance(q["answer"], int):
                correct_flag = (choice == q["answer"])
            else:
                # fuzzy-match string
                correct_flag = is_fuzzy_match(options[choice], q["answer"])
        else:
            # fallback: server might not include answer; accept local 'answer' key or 'correct'
            correct_flag = False

        # UI feedback
        if correct_flag:
            console.print("[green]✅ Correct[/green]")
        # else:
        #     # compute correct repr for display
        #     corr_repr = None
        #     if "answer_index" in q:
        #         corr_repr = options[q["answer_index"]]
        #     elif "answer" in q and isinstance(q["answer"], str):
        #         corr_repr = q["answer"]
        #     else:
        #         corr_repr = "(unknown)"
        #     console.print(f"[red]❌ Wrong — expected:[/red] {corr_repr}")

        # Save locally and send log remotely
        entry = dict(
            sti=sti,
            question=qtext,
            student_answer=options[choice],
            # correct_answer=corr_repr,
            is_correct=bool(correct_flag),
            # timestamp=timestamp()
        )
        save_to_db(**entry)
        send_remote_log(token, entry)
        return bool(correct_flag)

def show_top_users():
    try:
        r = requests.get(API_TOP_USERS, timeout=REMOTE_TIMEOUT)
        r.raise_for_status()
        tops = r.json()  # expect list like [{"name":"Joe", "score": 90}, ...]
        t = Table(title="Top 20")
        t.add_column("Rank")
        t.add_column("Name")
        t.add_column("Score", justify="right")
        for i, u in enumerate(tops[:20], start=1):
            t.add_row(str(i), u.get("name", "N/A"), str(u.get("score", "0")))
        console.print(t)
    except Exception as e:
        console.print(f"[yellow]Could not fetch leaderboard: {e}[/yellow]")

def run_quiz(sti, token=None):
    qs = load_questions()
    if not qs:
        console.print("[red]No questions available. Please check your network or local questions file.[/red]")
        return

    random.shuffle(qs)
    sel = qs[:SESSION_QUESTION_COUNT]
    score = 0
    answered = 0

    for idx, q in enumerate(sel, start=1):
        # show top scorer live (if available)
        try:
            r = requests.get(API_TOP_USERS, timeout=1)
            if r.status_code == 200:
                top = r.json()[0] if r.json() else None
                if top:
                    console.print(f"[magenta]Top Scorer: {top.get('name')} — {top.get('score')}[/magenta]")
        except Exception:
            # don't spam network errors
            pass

        res = present_question(q, idx, len(sel), sti, token, score)
        if res is None:  # user signaled 'done' or 'exit'
            break
        answered += 1
        if res:
            score += 1

        # Print progress table after each question
        percent = (score / answered) * 100 if answered else 0.0
        t = Table(title="Progress")
        t.add_column("Answered")
        t.add_column("Correct")
        t.add_column("Total")
        t.add_column("Percent")
        t.add_row(str(answered), str(score), str(len(sel)), f"{percent:.1f}%")
        console.print(t)

    # Summary
    t = Table(title="Summary")
    t.add_column("STI")
    t.add_column("Correct")
    t.add_column("Answered")
    t.add_column("Percent")
    pct = (score / max(1, answered)) * 100 if answered else 0.0
    t.add_row(sti, str(score), str(answered), f"{pct:.1f}%")
    console.print(t)

    # Send final summary to server (email/send)
    try:
        final_payload = {"sti": sti, "score": score, "answered": answered, "percent": pct}
        send_remote_log(token, final_payload)
    except Exception as e:
        console.print(f"[yellow]Failed to send final summary: {e}[/yellow]")

    console.print("[green]Quiz finished. Check your email for full results and learning links.[/green]")
