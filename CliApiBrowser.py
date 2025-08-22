import os
import sys
import requests
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

console = Console()
load_dotenv()

class GeminiBrowser:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            console.print("[bold red]API key not set in .env[/bold red]")
            sys.exit(1)
        self.model = "gemini-1.5-flash"  

    def set_model(self, model_name):
        supported_models = ['gemini-1.5-flash', 'gemini-1.5-pro']
        if model_name in supported_models:
            self.model = model_name
            console.print(f"[cyan]Switched to model:[/cyan] [bold]{model_name}[/bold]")
        else:
            console.print("[red]Unsupported model.[/red] Available models: "
                          + ', '.join(supported_models))

    def gemini_query(self, prompt):
        api_url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={self.api_key}"
        headers = {"Content-Type": "application/json"}
        data = {"contents": [{"parts": [{"text": prompt}]}]}
        response = requests.post(api_url, json=data, headers=headers)

        if response.status_code == 200:
            output = response.json()
            try:
                return output["candidates"][0]["content"]["parts"][0]["text"].strip()
            except (KeyError, IndexError):
                return "No response from Gemini."
        else:
            console.print(f"[bold red]Error {response.status_code}[/bold red]: {response.text}")
            return None

def main():
    bot = GeminiBrowser()
    console.print(Panel("[bold cyan]Welcome to the Gemini CLI Browser[/bold cyan]\n"
                        "Type [yellow]exit[/yellow] to quit\n"
                        "Switch models with [yellow]/model NAME[/yellow]\n"
                        "Save last reply with [yellow]/save filename.txt[/yellow]",
                        title="Info", style="blue"))

    last_reply = None  

    while True:
        user_input = Prompt.ask("[bold green]>>>[/bold green]").strip()

        if user_input.lower() in ["exit", "quit"]:
            console.print("[bold red]Goodbye![/bold red]")
            break

        elif user_input.startswith('/model'):
            parts = user_input.split(maxsplit=1)
            if len(parts) == 2:
                model_name = parts[1].strip()
                bot.set_model(model_name)
            else:
                console.print("[yellow]Usage:[/yellow] /model MODEL_NAME")

        elif user_input.startswith('/save'):
            parts = user_input.split(maxsplit=1)
            if len(parts) == 2:
                filename = parts[1].strip()
                if last_reply:
                    try:
                        with open(filename, "w", encoding="utf-8") as f:
                            f.write(last_reply)
                        console.print(f"[bold green]Reply saved to {filename}[/bold green]")
                    except Exception as e:
                        console.print(f"[bold red]Error saving file:[/bold red] {e}")
                else:
                    console.print("[yellow]No reply to save yet.[/yellow]")
            else:
                console.print("[yellow]Usage:[/yellow] /save filename.txt")

        else:
            with console.status("[bold cyan]Thinking...[/bold cyan]", spinner="dots"):
                reply = bot.gemini_query(user_input)

            if reply:
                console.print(Panel(reply, title="Gemini Reply", style="green"))
                last_reply = reply  

if __name__ == "__main__":
    main()