"""Live terminal CPU monitor.

Shows overall CPU usage, per-core usage, load average, a rolling history bar,
and the top CPU-consuming processes. Refreshes in place with `rich`.

Usage:
    python3 cpu_monitor.py
"""

from __future__ import annotations

import os
import time
from collections import deque

import psutil
from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.table import Table

console = Console()

HISTORY_LEN = 20
TOP_N = 10

# Rolling history of overall CPU percentages, for the sparkline bar.
cpu_history: deque[float] = deque(maxlen=HISTORY_LEN)

# Thresholds for the history bar glyphs.
_HIGH, _MID = 70.0, 40.0


def top_n(processes: list[dict], n: int = TOP_N) -> list[dict]:
    """Return the `n` processes with the highest CPU usage.

    Processes missing a `cpu_percent` key are treated as 0.0 so they sort last
    rather than raising.
    """
    return sorted(
        processes, key=lambda p: p.get("cpu_percent") or 0.0, reverse=True
    )[:n]


def build_history_bar(history: deque[float]) -> str:
    """Render CPU history as a compact glyph bar."""
    return "".join(
        "█" if p > _HIGH else "▓" if p > _MID else "░" for p in history
    )


def format_load(load_avg: tuple[float, float, float]) -> str:
    """Format a 1/5/15-minute load average tuple."""
    return " / ".join(f"{v:.2f}" for v in load_avg[:3])


def get_cpu_info() -> tuple[float, list[float], tuple, list[dict]]:
    """Sample current CPU state. Blocking; takes ~0.6s."""
    cpu_percent = psutil.cpu_percent(interval=0.5)
    cpu_per_core = psutil.cpu_percent(interval=0.1, percpu=True)
    load_avg = os.getloadavg()

    procs = []
    for p in psutil.process_iter(["pid", "name", "cpu_percent"]):
        try:
            procs.append(p.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    cpu_history.append(cpu_percent)
    return cpu_percent, cpu_per_core, load_avg, top_n(procs)


def create_tables(
    cpu_percent: float,
    cpu_per_core: list[float],
    load_avg: tuple,
    top_processes: list[dict],
) -> tuple[Panel, Table]:
    """Build the summary panel and the top-processes table."""
    table = Table(title="CPU Monitor")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green")

    table.add_row("Overall CPU usage", f"{cpu_percent:.1f}%")
    table.add_row("Load average (1/5/15 min)", format_load(load_avg))
    table.add_row("Logical cores", str(psutil.cpu_count(logical=True)))

    shown = cpu_per_core[:8]
    core_str = ", ".join(f"C{i}:{p:.0f}%" for i, p in enumerate(shown))
    if len(cpu_per_core) > len(shown):
        core_str += f"  (+{len(cpu_per_core) - len(shown)} more)"
    table.add_row("Per-core usage", core_str)
    table.add_row("History (recent)", build_history_bar(cpu_history))

    proc_table = Table(title="Top CPU processes", box=None)
    proc_table.add_column("PID", style="dim")
    proc_table.add_column("Name")
    proc_table.add_column("CPU %", justify="right")

    for p in top_processes:
        name = (p.get("name") or "?")[:25]
        cpu = p.get("cpu_percent") or 0.0
        proc_table.add_row(str(p.get("pid", "?")), name, f"{cpu:.1f}")

    return Panel.fit(table, title="Real-time CPU monitor"), proc_table


def main() -> None:
    """Run the monitor loop until interrupted."""
    with Live("", refresh_per_second=2, screen=True) as live:
        while True:
            try:
                cpu_percent, cpu_per_core, load_avg, top_processes = get_cpu_info()
                panel, proc_table = create_tables(
                    cpu_percent, cpu_per_core, load_avg, top_processes
                )
                live.update(f"{panel}\n{proc_table}")
                time.sleep(1.5)
            except KeyboardInterrupt:
                console.print("[bold red]Monitoring stopped.[/bold red]")
                break


if __name__ == "__main__":
    main()
