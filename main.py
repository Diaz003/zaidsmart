#!/usr/bin/env python3
"""
ZAIDSMART entry point.
"""

import argparse
import asyncio
import os
import subprocess
from typing import Sequence

from dotenv import load_dotenv

load_dotenv()


def print_banner():
    from rich.console import Console

    console = Console()
    banner = """
███████╗ █████╗ ██╗██████╗ ███████╗███╗   ███╗ █████╗ ██████╗ ████████╗
╚══███╔╝██╔══██╗██║██╔══██╗██╔════╝████╗ ████║██╔══██╗██╔══██╗╚══██╔══╝
  ███╔╝ ███████║██║██║  ██║███████╗██╔████╔██║███████║██████╔╝   ██║
 ███╔╝  ██╔══██║██║██║  ██║╚════██║██║╚██╔╝██║██╔══██║██╔══██╗   ██║
███████╗██║  ██║██║██████╔╝███████║██║ ╚═╝ ██║██║  ██║██║  ██║   ██║
╚══════╝╚═╝  ╚═╝╚═╝╚═════╝ ╚══════╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝
"""
    console.print(banner, style="bold cyan")
    console.print("-" * 70, style="dim")
    console.print(
        "-> Iniciando entorno de Inteligencia Artificial para: "
        "[bold cyan]ZAIDSMART[/bold cyan]..."
    )


def check_port(port: int) -> bool:
    import socket

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        return sock.connect_ex(("127.0.0.1", port)) != 0


def render_task_table(tasks: Sequence[dict]):
    from rich.table import Table

    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("ID", style="bold")
    table.add_column("Agente")
    table.add_column("Estado")
    table.add_column("Progreso", justify="right")
    table.add_column("Descripcion", overflow="fold")

    for task in tasks[:8]:
        table.add_row(
            task.get("id", "-"),
            task.get("agent", "manager"),
            task.get("status", "queued"),
            f"{task.get('progress', 0)}%",
            (task.get("description", "") or "")[:72],
        )

    if not tasks:
        table.add_row("-", "-", "sin tareas", "0%", "Todavia no hay actividad")

    return table


async def run_cli_monitor():
    from rich.console import Console
    from rich.live import Live

    from core.agent_runner import get_all_tasks, init_db

    console = Console()
    await init_db()
    console.print("Modo CLI activo. Pulsa Ctrl+C para salir.", style="bold green")

    with Live(render_task_table([]), refresh_per_second=4, console=console) as live:
        while True:
            tasks = await get_all_tasks()
            live.update(render_task_table(tasks))
            await asyncio.sleep(2)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cli-only", action="store_true", help="Solo interfaz terminal")
    parser.add_argument(
        "--refresh-models",
        action="store_true",
        help="Re-escanear modelos y salir",
    )
    args = parser.parse_args()

    print_banner()

    if args.refresh_models:
        from core.scraper import get_free_models

        models = get_free_models()
        print(f"\nSe encontraron {len(models)} modelos gratuitos:")
        for model in models:
            print(f"  - {model}")
        return

    from rich.console import Console

    console = Console()
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))

    console.print(f"Verificando puerto {port}...")
    if not check_port(port):
        console.print(f"Puerto {port} ocupado, intentando liberar...", style="yellow")
        subprocess.run(["fuser", "-k", f"{port}/tcp"], check=False, capture_output=True)

    console.print("Entorno virtual activado.", style="green")
    console.print(f"Dashboard disponible en: [link]http://{host}:{port}[/link]")

    try:
        result = subprocess.run(
            ["tailscale", "ip", "-4"],
            capture_output=True,
            text=True,
            timeout=3,
            check=False,
        )
        ts_ip = result.stdout.strip()
        if ts_ip:
            console.print(f"Tailscale: [bold]{ts_ip}:{port}[/bold]")
    except Exception:
        pass

    console.print("-" * 70, style="dim")

    if args.cli_only:
        try:
            asyncio.run(run_cli_monitor())
        except KeyboardInterrupt:
            console.print("\nCLI detenido.", style="yellow")
        return

    import uvicorn

    uvicorn.run(
        "api.main:app",
        host=host,
        port=port,
        reload=True,
        log_level="warning",
    )


if __name__ == "__main__":
    main()
