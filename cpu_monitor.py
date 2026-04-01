import psutil
import time
import os
from rich.console import Console
from rich.table import Table
from rich.live import Live
from rich.panel import Panel
from collections import deque

console = Console()
cpu_history = deque(maxlen=20)  # For simple sparkline-like history

def get_cpu_info():
    cpu_percent = psutil.cpu_percent(interval=0.5)
    cpu_per_core = psutil.cpu_percent(interval=0.1, percpu=True)
    load_avg = os.getloadavg()
    top_processes = sorted(psutil.process_iter(['pid', 'name', 'cpu_percent']), 
                           key=lambda p: p.info['cpu_percent'], reverse=True)[:10]
    
    cpu_history.append(cpu_percent)
    return cpu_percent, cpu_per_core, load_avg, top_processes

def create_table(cpu_percent, cpu_per_core, load_avg, top_processes):
    table = Table(title="Linux CPU Monitoring System")
    
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green")
    
    table.add_row("Overall CPU Usage", f"{cpu_percent:.1f}%")
    table.add_row("Load Average (1/5/15min)", f"{load_avg[0]:.2f} / {load_avg[1]:.2f} / {load_avg[2]:.2f}")
    table.add_row("Cores", str(psutil.cpu_count(logical=True)))
    
    # Per-core
    core_str = ", ".join([f"C{i}:{p:.0f}%" for i, p in enumerate(cpu_per_core[:8])])  # Limit display
    if len(cpu_per_core) > 8:
        core_str += f" ... +{len(cpu_per_core)-8} more"
    table.add_row("Per-Core Usage", core_str)
    
    # History bar (simple)
    hist_bar = "".join(["█" if p > 70 else "▓" if p > 40 else "░" for p in cpu_history])
    table.add_row("CPU History (recent)", hist_bar)
    
    # Top processes
    proc_table = Table(title="Top CPU Processes", box=None)
    proc_table.add_column("PID", style="dim")
    proc_table.add_column("Name")
    proc_table.add_column("CPU %", justify="right")
    
    for p in top_processes:
        try:
            proc_table.add_row(str(p.info['pid']), p.info['name'][:25], f"{p.info['cpu_percent']:.1f}")
        except:
            pass
    
    return Panel.fit(table, title="Real-time CPU Monitor"), proc_table

with Live("", refresh_per_second=2, screen=True) as live:
    while True:
        try:
            cpu_percent, cpu_per_core, load_avg, top_processes = get_cpu_info()
            main_panel, proc_table = create_table(cpu_percent, cpu_per_core, load_avg, top_processes)
            
            live.update(f"{main_panel}\n{proc_table}")
            time.sleep(1.5)
        except KeyboardInterrupt:
            console.print("[bold red]Monitoring stopped.[/bold red]")
            break
