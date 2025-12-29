#!/usr/bin/env python3
"""
CLI Interactiva para probar el sistema de colas.

Uso:
    python app_cli.py
    
Comandos:
    start              - Iniciar workers
    stop               - Detener workers
    add <name> [prio]  - Añadir tarea (prioridad 0-3)
    flood <n>          - Añadir N tareas aleatorias
    status             - Ver estado detallado
    clear              - Limpiar pantalla
    help               - Mostrar ayuda
    quit               - Salir
"""

import asyncio
import argparse
import random
import sys
from typing import Optional

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.layout import Layout
from rich.live import Live
from rich.text import Text
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich import box

from queue_system import (
    QueueManager,
    Task,
    TaskPriority,
    TaskType,
    get_config,
)


console = Console()


# ============================================================
# Visualización con Rich
# ============================================================

def create_header() -> Panel:
    """Crea el header de la aplicación."""
    title = Text("🚀 QueueSystem - CLI Interactiva", style="bold cyan")
    subtitle = Text("Sistema de Colas de Alto Rendimiento", style="dim")
    return Panel(
        Text.assemble(title, "\n", subtitle),
        box=box.DOUBLE,
        border_style="cyan"
    )


def create_queue_table(manager: QueueManager) -> Table:
    """Crea tabla de estado de las colas."""
    table = Table(title="📊 Estado de Colas", box=box.ROUNDED)
    
    table.add_column("Cola", style="cyan", width=15)
    table.add_column("Tamaño", justify="center", width=12)
    table.add_column("Capacidad", justify="center", width=12)
    table.add_column("Llenado", justify="center", width=20)
    
    # Dataset Queue
    dq = manager.dataset_queue
    fill_bar = create_fill_bar(dq.fill_ratio)
    table.add_row(
        "📦 Dataset",
        str(dq.qsize),
        str(dq.maxsize),
        fill_bar
    )
    
    # Command Queue
    cq = manager.command_queue
    fill_bar = create_fill_bar(cq.fill_ratio)
    table.add_row(
        "⚙️  Command",
        str(cq.qsize),
        str(cq.maxsize),
        fill_bar
    )
    
    return table


def create_fill_bar(ratio: float) -> Text:
    """Crea una barra de llenado visual."""
    filled = int(ratio * 10)
    empty = 10 - filled
    
    if ratio < 0.5:
        color = "green"
    elif ratio < 0.8:
        color = "yellow"
    else:
        color = "red"
    
    bar = "█" * filled + "░" * empty
    return Text(f"{bar} {ratio*100:.0f}%", style=color)


def create_workers_table(manager: QueueManager) -> Table:
    """Crea tabla de estado de workers."""
    table = Table(title="👷 Workers", box=box.ROUNDED)
    
    table.add_column("ID", style="cyan", width=15)
    table.add_column("Estado", justify="center", width=15)
    table.add_column("Tarea Actual", width=20)
    table.add_column("Completadas", justify="right", width=12)
    
    # Dataset workers
    for w in manager.dataset_pool.get_worker_status():
        state_icon = "🟢" if w["state"] == "processing" else "🟡" if w["state"] == "idle" else "🔴"
        state_text = Text(f"{state_icon} {w['state']}")
        task_text = w["current_task"] or "-"
        table.add_row(w["id"], state_text, task_text, str(w["tasks_completed"]))
    
    # Command workers
    for w in manager.command_pool.get_worker_status():
        state_icon = "🟢" if w["state"] == "processing" else "🟡" if w["state"] == "idle" else "🔴"
        state_text = Text(f"{state_icon} {w['state']}")
        task_text = w["current_task"] or "-"
        table.add_row(w["id"], state_text, task_text, str(w["tasks_completed"]))
    
    return table


def create_metrics_panel(manager: QueueManager) -> Panel:
    """Crea panel de métricas."""
    m = manager.metrics
    
    content = Text()
    content.append("Completadas: ", style="dim")
    content.append(f"{m.tasks_completed}", style="green bold")
    content.append("  │  Fallidas: ", style="dim")
    content.append(f"{m.tasks_failed}", style="red bold")
    content.append("  │  Rechazadas: ", style="dim")
    content.append(f"{m.tasks_rejected}", style="yellow bold")
    content.append("\n")
    content.append("Throughput: ", style="dim")
    content.append(f"{m.throughput:.2f}/s", style="cyan bold")
    content.append("  │  Tiempo Prom: ", style="dim")
    content.append(f"{m.avg_processing_time:.2f}s", style="cyan bold")
    content.append("  │  Uptime: ", style="dim")
    content.append(f"{m.uptime_seconds:.0f}s", style="cyan")
    
    return Panel(content, title="📈 Métricas", box=box.ROUNDED)


def create_help_panel() -> Panel:
    """Crea panel de ayuda."""
    help_text = """
[bold cyan]Comandos disponibles:[/bold cyan]

  [green]start[/green]              Iniciar todos los workers
  [green]stop[/green]               Detener todos los workers
  [green]add[/green] <name> [prio]  Añadir tarea (prio: 0=CRITICAL, 1=HIGH, 2=NORMAL, 3=LOW)
  [green]cmd[/green] <name> [prio]  Añadir comando del sistema
  [green]flood[/green] <n>          Añadir N tareas aleatorias
  [green]status[/green]             Mostrar estado actual
  [green]clear[/green]              Limpiar pantalla
  [green]help[/green]               Mostrar esta ayuda
  [green]quit[/green]               Salir de la aplicación
"""
    return Panel(help_text, title="❓ Ayuda", box=box.ROUNDED, border_style="dim")


def print_status(manager: QueueManager):
    """Imprime el estado completo del sistema."""
    console.print()
    console.print(create_queue_table(manager))
    console.print()
    console.print(create_workers_table(manager))
    console.print()
    console.print(create_metrics_panel(manager))
    console.print()


# ============================================================
# Comandos CLI
# ============================================================

class QueueCLI:
    """Clase principal de la CLI."""
    
    def __init__(self, dataset_workers: int = None, command_workers: int = None):
        # Cargar configuración desde config.yml
        config = get_config()
        
        # Usar parámetros explícitos o valores de config.yml
        _dataset_workers = dataset_workers or config.workers.dataset
        _command_workers = command_workers or config.workers.command
        
        self.manager = QueueManager(
            dataset_workers=_dataset_workers,
            command_workers=_command_workers,
        )
        self.running = True
        
        # Configurar callbacks para ver actividad
        self.manager.on_task_start = self._on_task_start
        self.manager.on_task_complete = self._on_task_complete
    
    async def _on_task_start(self, task: Task, worker_id: str):
        """Callback cuando inicia una tarea."""
        console.print(
            f"  [dim]→[/dim] [cyan]{worker_id}[/cyan] procesando "
            f"[yellow]{task.name}[/yellow] ({task.priority.name})"
        )
    
    async def _on_task_complete(self, task: Task, worker_id: str, elapsed: float):
        """Callback cuando termina una tarea."""
        console.print(
            f"  [dim]✓[/dim] [green]{worker_id}[/green] completó "
            f"[yellow]{task.name}[/yellow] en {elapsed:.2f}s"
        )
    
    async def cmd_start(self):
        """Inicia los workers."""
        if self.manager.running:
            console.print("[yellow]⚠ Los workers ya están corriendo[/yellow]")
            return
        
        await self.manager.start()
        console.print("[green]✓ Workers iniciados[/green]")
    
    async def cmd_stop(self):
        """Detiene los workers."""
        if not self.manager.running:
            console.print("[yellow]⚠ Los workers ya están detenidos[/yellow]")
            return
        
        await self.manager.stop()
        console.print("[red]✗ Workers detenidos[/red]")
    
    async def cmd_add(self, name: str, priority: int = 2):
        """Añade una tarea de dataset."""
        prio = TaskPriority.from_int(priority)
        # Tiempo de procesamiento aleatorio entre 0.5 y 3 segundos
        proc_time = random.uniform(0.5, 3.0)
        
        task = await self.manager.enqueue_dataset(
            name=name,
            priority=prio,
            processing_time=proc_time
        )
        
        if task:
            console.print(
                f"[green]✓[/green] Tarea añadida: [cyan]{task.task_id}[/cyan] "
                f"'{task.name}' ({prio.name}, {proc_time:.1f}s)"
            )
        else:
            console.print("[red]✗ Cola llena, tarea rechazada[/red]")
    
    async def cmd_command(self, name: str, priority: int = 1):
        """Añade un comando del sistema."""
        prio = TaskPriority.from_int(priority)
        proc_time = random.uniform(0.1, 0.5)  # Comandos son rápidos
        
        task = await self.manager.enqueue_command(
            name=name,
            priority=prio,
            processing_time=proc_time
        )
        
        if task:
            console.print(
                f"[green]✓[/green] Comando añadido: [cyan]{task.task_id}[/cyan] "
                f"'{task.name}' ({prio.name})"
            )
        else:
            console.print("[red]✗ Cola llena, comando rechazado[/red]")
    
    async def cmd_flood(self, count: int):
        """Añade múltiples tareas aleatorias."""
        names = ["query_sales", "export_report", "load_data", "sync_db", "calculate_metrics"]
        added = 0
        
        with console.status(f"Añadiendo {count} tareas..."):
            for i in range(count):
                name = f"{random.choice(names)}_{i}"
                priority = random.randint(0, 3)
                proc_time = random.uniform(0.3, 2.0)
                
                task = await self.manager.enqueue_dataset(
                    name=name,
                    priority=TaskPriority.from_int(priority),
                    processing_time=proc_time
                )
                if task:
                    added += 1
        
        console.print(f"[green]✓ Añadidas {added}/{count} tareas[/green]")
        if added < count:
            console.print(f"[yellow]⚠ {count - added} rechazadas (cola llena)[/yellow]")
    
    async def cmd_status(self):
        """Muestra estado del sistema."""
        print_status(self.manager)
    
    def cmd_help(self):
        """Muestra ayuda."""
        console.print(create_help_panel())
    
    def cmd_clear(self):
        """Limpia la pantalla."""
        console.clear()
        console.print(create_header())
    
    async def process_command(self, line: str) -> bool:
        """
        Procesa un comando.
        Retorna False si el usuario quiere salir.
        """
        parts = line.strip().split()
        if not parts:
            return True
        
        cmd = parts[0].lower()
        args = parts[1:]
        
        try:
            if cmd in ("quit", "exit", "q"):
                return False
            
            elif cmd == "start":
                await self.cmd_start()
            
            elif cmd == "stop":
                await self.cmd_stop()
            
            elif cmd == "add":
                if not args:
                    console.print("[red]Uso: add <nombre> [prioridad][/red]")
                else:
                    name = args[0]
                    priority = int(args[1]) if len(args) > 1 else 2
                    await self.cmd_add(name, priority)
            
            elif cmd == "cmd":
                if not args:
                    console.print("[red]Uso: cmd <nombre> [prioridad][/red]")
                else:
                    name = args[0]
                    priority = int(args[1]) if len(args) > 1 else 1
                    await self.cmd_command(name, priority)
            
            elif cmd == "flood":
                if not args:
                    console.print("[red]Uso: flood <cantidad>[/red]")
                else:
                    count = int(args[0])
                    await self.cmd_flood(count)
            
            elif cmd == "status":
                await self.cmd_status()
            
            elif cmd == "clear":
                self.cmd_clear()
            
            elif cmd == "help":
                self.cmd_help()
            
            else:
                console.print(f"[red]Comando desconocido: {cmd}[/red]")
                console.print("[dim]Escribe 'help' para ver los comandos disponibles[/dim]")
        
        except ValueError as e:
            console.print(f"[red]Error en argumentos: {e}[/red]")
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
        
        return True

    async def run(self):
        """Loop principal de la CLI."""
        console.clear()
        console.print(create_header())
        console.print()
        self.cmd_help()
        console.print()
        
        # Función para leer input sin bloquear el event loop
        loop = asyncio.get_event_loop()
        
        while self.running:
            try:
                # Mostrar prompt
                console.print("[bold green]>[/bold green] ", end="")
                
                # Leer input de forma no-bloqueante usando run_in_executor
                # Esto permite que los workers sigan corriendo mientras esperamos input
                line = await loop.run_in_executor(None, input)
                
                if not await self.process_command(line):
                    # Usuario quiere salir
                    if self.manager.running:
                        console.print("[dim]Deteniendo workers...[/dim]")
                        await self.manager.stop()
                    console.print("[cyan]¡Hasta luego! 👋[/cyan]")
                    break
                
            except KeyboardInterrupt:
                console.print("\n[yellow]Ctrl+C detectado. Escribe 'quit' para salir.[/yellow]")
            except EOFError:
                break


# ============================================================
# Main
# ============================================================

def parse_args():
    """Parsea argumentos de línea de comandos."""
    parser = argparse.ArgumentParser(
        description="QueueSystem - CLI Interactiva para sistema de colas"
    )
    config = get_config()
    parser.add_argument(
        "--dataset-workers", "-d",
        type=int,
        default=None,
        help=f"Número de workers para cola de datasets (config.yml: {config.workers.dataset})"
    )
    parser.add_argument(
        "--command-workers", "-c",
        type=int,
        default=None,
        help=f"Número de workers para cola de comandos (config.yml: {config.workers.command})"
    )
    return parser.parse_args()


async def main():
    """Punto de entrada principal."""
    args = parse_args()
    
    cli = QueueCLI(
        dataset_workers=args.dataset_workers,
        command_workers=args.command_workers
    )
    
    await cli.run()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        console.print("\n[cyan]Bye![/cyan]")
