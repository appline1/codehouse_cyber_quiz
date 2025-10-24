import time
import requests
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from .config import API_LOGIN,API_VERIFY_TOKEN, API_REGISTER_USER, REMOTE_TIMEOUT, TEMP_TOKEN_EXPIRY_SECONDS, MAX_LOGIN_ATTEMPTS

console = Console()

def register_flow():
    """
    Register a new participant on the website by collecting fullname, email and phone.
    The website is expected to send back a temporary token or accept that it will email a token.
    """
    console.print(Panel.fit("Registration — Create a participant (Fullname, Email, Phone)", title="Register", style="green"))
    fullname = Prompt.ask("Full name").strip()
    email = Prompt.ask("Email").strip()
    phone = Prompt.ask("Phone number").strip()

    payload = {"fullname": fullname, "email": email, "phone": phone}
    try:
        resp = requests.post(API_REGISTER_USER, json=payload, timeout=REMOTE_TIMEOUT)
    except Exception as e:
        console.print(f"[yellow]Network/Registration error:[/yellow] {e}")
        return None, None

    if resp.status_code not in (200, 201):
        console.print(f"[red]Registration failed:[/red] {resp.status_code} {resp.text}")
        return None, None

    data = resp.json()
    # Expected server: returns temp_token (but server may email it instead).
    temp_token = data.get("temp_token")
    console.print("[green]Registration request received. Check your email for a temporary token.[/green]")
    if temp_token:
        console.print("[cyan]Server also returned a temporary token (useful for testing).[/cyan]")
    return email, temp_token

def verify_temp_token_flow(email):
    """
    Verifies the temporary token via API instead of local match.
    """
    start = time.time()
    attempts = 0
    while attempts < MAX_LOGIN_ATTEMPTS and (time.time() - start) < TEMP_TOKEN_EXPIRY_SECONDS:
        tok = Prompt.ask("Enter temporary token (from email) — or type 'cancel'").strip()
        if tok.lower() in ("cancel", "exit", "stop"):
            return False
        
        try:
            resp = requests.post(API_VERIFY_TOKEN, json={"email": email, "token": tok}, timeout=REMOTE_TIMEOUT)
            print(f"[yellow]Debug: response code {resp.status_code}[/yellow]")
            if resp.status_code == 200:
                console.print("[green]Token verified successfully.[/green]")
                return True
            else:
                console.print("[red]Invalid or expired token.[/red]")
        except Exception as e:
            console.print(f"[yellow]Network error: {e}[/yellow]")
            return False

        attempts += 1

    console.print("[bold red]Too many attempts or expired token.[/bold red]")
    return False


def login_with_sti():
    attempts = 0
    while attempts < MAX_LOGIN_ATTEMPTS:
        sti = Prompt.ask("Enter Student Task ID (STI)").strip()
        password = Prompt.ask("Enter Password", password=True).strip()
        try:
            resp = requests.post(API_LOGIN, json={"sti": sti, "password": password}, timeout=REMOTE_TIMEOUT)
        except Exception as e:
            console.print(f"[yellow]Network error during login:[/yellow] {e}")
            attempts += 1
            continue

        if resp.status_code == 200:
            token = resp.json().get("token")
            console.print(f"[green]Welcome {sti}![/green]")
            return sti, token
        else:
            console.print("[red]Invalid credentials[/red]")
            attempts += 1

    console.print("[bold red]Too many failed attempts. Access denied.[/bold red]")
    raise SystemExit(1)
