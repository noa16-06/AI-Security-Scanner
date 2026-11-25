import os
import sys
from ollama import Client
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

client = Client(
    host=os.getenv("API_HOST", "http://localhost:11434"),
    headers={"x-some-header": os.getenv("HEADER_VALUE", "some-value")},
)
console = Console()

security_prompt = """Review this source code for concrete security issues.
Return a concise Markdown report with:
- A short summary
- Distinct findings, ordered by severity
- For each finding: severity, location, why it matters, impact, and a concise fix

Do not repeat the source code, duplicate findings, or include whole-file rewrites.
Only report issues supported by the code. If there are no findings, say so.

Source code:
{code}
"""

# Check if the user provided a file path as an argument
if len(sys.argv) < 2 or not os.path.isfile(sys.argv[1]):
    console.print("[yellow]Usage: python scanner.py <path_to_code_file>[/]")
    sys.exit(1)

console.print(
    Panel.fit(
        "[bold]AI Security Scanner[/bold]\n[dim]Ollama-powered code review[/dim]",
        border_style="cyan",
    )
)
code_file_path = sys.argv[1]
with open(code_file_path, 'r') as code_file:
    code_content = code_file.read()

prompt = security_prompt.format(code=code_content)

try:
    console.print(f"[dim]Scanning {code_file_path}...[/]")
    response = client.chat(
        model="qwen2.5:7b",
        messages=[{"role": "user", "content": prompt}],
    )
    console.print("[green]✓ Scan complete[/]")
    console.print(
        Panel(
            Markdown(response.message.content),
            title="Security scan report",
            border_style="cyan",
            padding=(1, 2),
        )
    )

# Handle exceptions that may occur during the request
except Exception as e:
    console.print(f"[bold red]Scan failed:[/] {e}")