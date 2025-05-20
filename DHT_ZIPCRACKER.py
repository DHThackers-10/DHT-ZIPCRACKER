import os
import time
import string
import itertools
import zipfile
import rarfile
import subprocess
import pyfiglet
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.live import Live
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
from rich.prompt import Prompt

# Initialize
console = Console()
clear = lambda: os.system('cls' if os.name == 'nt' else 'clear')

# Banner with Rich UI
def show_banner(text, style):
    clear()
    banner = pyfiglet.figlet_format(text)
    console.print(f"[{style}]{banner}[/{style}]")

def dht_hackers_banner():
    show_banner("DHT-HACKERS", "red")
    console.print(Panel.fit(
        "[cyan]────────────────────────────────────────────────────────────[/cyan]\n"
        "[green] THIS TOOL IS PAID! TO USE IT FOR FREE:\n"
        "[magenta] SUBSCRIBE TO OUR CHANNEL FOR ETHICAL HACKING TUTORIALS!\n"
        "[blue] https://youtube.com/@dht-hackers_10?si=lsdJ-naJvp7ql-QT\n"
        "[cyan]────────────────────────────────────────────────────────────[/cyan]",
        title="[bold yellow]Information[/bold yellow]",
        border_style="magenta"
    ))
    time.sleep(2)
    os.system("termux-open-url https://youtube.com/@dht-hackers_10?si=lsdJ-naJvp7ql-QT")
    Prompt.ask("[yellow]Press Enter after subscribing to continue...[/yellow]")
    clear()

def dht_cracker_banner():
    show_banner("DHT-CRACKER", "blue")
    console.print(Panel.fit(
        "[cyan]────────────────────────────────────────────────────────────[/cyan]\n"
        "[green] FAST & POWERFUL ARCHIVE PASSWORD CRACKER\n"
        "[yellow] Developed by: DHT-HACKERS TEAM | Multi-threaded | High Performance\n"
        "[cyan]────────────────────────────────────────────────────────────[/cyan]",
        title="[bold green]About[/bold green]",
        border_style="cyan"
    ))

# Archive Extraction
def extract_file(file_path, password):
    try:
        if file_path.endswith(".zip"):
            with zipfile.ZipFile(file_path) as zf:
                zf.extractall(pwd=password.encode())
        elif file_path.endswith(".rar"):
            with rarfile.RarFile(file_path) as rf:
                rf.extractall(pwd=password)
        elif file_path.endswith(".7z"):
            result = subprocess.run(["7z", "t", file_path, f"-p{password}"],
                                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            if result.returncode == 0:
                subprocess.run(["7z", "x", file_path, f"-p{password}", "-y"])
                return True
            return False
        else:
            return False
        return True
    except:
        return False

# Attempt Table
def generate_table(attempts, password_guess):
    table = Table(title="Password Attempts", expand=True)
    table.add_column("Attempt #", justify="center", style="cyan")
    table.add_column("Current Guess", justify="center", style="magenta")
    table.add_row(str(attempts), password_guess)
    return table

# Brute-force Attack
def brute_force_crack(file_path, max_length):
    chars = string.ascii_letters + string.digits + string.punctuation
    attempts = 0
    start_time = time.time()

    with Live(console=console, refresh_per_second=12) as live:
        for length in range(1, max_length + 1):
            for attempt in itertools.product(chars, repeat=length):
                password = ''.join(attempt)
                attempts += 1
                live.update(generate_table(attempts, password))
                if extract_file(file_path, password):
                    duration = time.time() - start_time
                    live.stop()
                    console.clear()
                    console.print(Panel(
                        f"[bold green]Password Found: [yellow]{password}[/yellow]\n"
                        f"Time Taken: {duration:.2f} seconds[/bold green]",
                        title="Success",
                        border_style="green"
                    ))
                    return
    console.print(Panel("[bold red]Password not found![/bold red]", title="Failure", border_style="red"))

# Dictionary Attack
def wordlist_crack(file_path, wordlist_path):
    try:
        with open(wordlist_path, 'r') as f:
            words = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        console.print(Panel("[bold red]Wordlist file not found.[/bold red]", title="Error", border_style="red"))
        return

    attempts = 0
    start_time = time.time()

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(bar_width=None),
        TimeElapsedColumn(),
        transient=True
    ) as progress:
        task = progress.add_task("Cracking archive...", total=len(words))
        for word in words:
            attempts += 1
            progress.update(task, advance=1)
            if extract_file(file_path, word):
                duration = time.time() - start_time
                console.clear()
                console.print(Panel(
                    f"[bold green]Password Found: [yellow]{word}[/yellow]\n"
                    f"Time Taken: {duration:.2f} seconds[/bold green]",
                    title="Success",
                    border_style="green"
                ))
                return
    console.print(Panel("[bold red]Password not found![/bold red]", title="Failure", border_style="red"))

# Main Entry
def main():
    dht_hackers_banner()
    dht_cracker_banner()

    file_path = Prompt.ask("[cyan]Enter archive file path[/cyan]")
    if not os.path.isfile(file_path):
        console.print(Panel("[bold red]File not found![/bold red]", title="Error", border_style="red"))
        return

    console.print(Panel(
        "[yellow]Choose cracking method:[/yellow]\n\n"
        "[blue]1.[/blue] Brute-force [dim](slow, no wordlist needed)[/dim]\n"
        "[blue]2.[/blue] Dictionary [dim](faster, requires wordlist)[/dim]",
        title="Crack Mode", border_style="yellow"
    ))

    choice = Prompt.ask("[cyan]Enter choice (1/2)[/cyan]", choices=["1", "2"])

    if choice == "1":
        max_len = Prompt.ask("[cyan]Enter max password length[/cyan]", default="4")
        if max_len.isdigit():
            brute_force_crack(file_path, int(max_len))
        else:
            console.print(Panel("[red]Invalid input! Enter a number.[/red]", title="Error", border_style="red"))
    elif choice == "2":
        wordlist_path = Prompt.ask("[cyan]Enter wordlist file path[/cyan]")
        if os.path.isfile(wordlist_path):
            wordlist_crack(file_path, wordlist_path)
        else:
            console.print(Panel("[bold red]Wordlist not found![/bold red]", title="Error", border_style="red"))

if __name__ == "__main__":
    main()
    
