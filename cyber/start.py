from .quiz_engine import run_quiz
from rich.console import Console
from .auth import register_flow, verify_temp_token_flow, login_with_sti
from .utils import init_db
from .config import MAX_LOGIN_ATTEMPTS

console = Console()
# 66258497
def main():
    console.print("[bold cyan]Welcome to CodeHouse Cloud Cyber Quiz[/bold cyan]")
    init_db()

    # Ask user whether they have STI or want to register
    choice = console.input("Do you already have an STI (Student Tasks ID)? (press Enter to create one or type y to login) [y/N to register] ").strip()
    if choice.lower() in ("n", "no", "") and choice != "y" and choice != "Y":
        # user wants to register
        email, returned_temp_token = register_flow()
        if not email:
            console.print("[red]Registration failed — aborting.[/red]")
            return
        ok = verify_temp_token_flow(email)
        if not ok:
            console.print("[red]Token verification failed — aborting.[/red]")
            return
        console.print("[green]Token verified. Check your email — you should receive your STI. Use it to login.[/green]")

    # now prompt for STI and password to login
    try:
        sti, token = login_with_sti()
    except SystemExit:
        return

    # Run quiz
    run_quiz(sti, token)

if __name__ == "__main__":
    main()
