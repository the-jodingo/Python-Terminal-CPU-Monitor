[![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![psutil](https://img.shields.io/badge/psutil-required-4B8BBE)](https://github.com/giampaolo/psutil)
[![rich](https://img.shields.io/badge/rich-required-8A2BE2)](https://github.com/Textualize/rich)
[![Platform](https://img.shields.io/badge/platform-Linux-lightgrey)](https://www.kernel.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

# Python Terminal CPU Monitor

A live terminal dashboard for CPU usage: overall load, per-core breakdown, load
average, and the top CPU-consuming processes — refreshed in place.

## Requirements

- Python 3.8+
- `psutil` and `rich`

```bash
pip install psutil rich
```

## Usage

```bash
python3 cpu_monitor.py
```

Press `Ctrl+C` to exit. The dashboard refreshes twice per second and keeps a
rolling history bar of the last 20 samples.

## What it shows

| Metric | Source |
|---|---|
| Overall CPU usage | `psutil.cpu_percent()` |
| Per-core usage | `psutil.cpu_percent(percpu=True)` (first 8 cores) |
| Load average (1/5/15 min) | `os.getloadavg()` |
| Top processes by CPU | `psutil.process_iter()` sorted by `cpu_percent` |

## Notes

- On macOS, `os.getloadavg()` reports the load average but it is not directly
  comparable to Linux (macOS counts differently). The script is written for Linux.
- Want email alerts on sustained high CPU? Extend it with `smtplib`, or use
  Prometheus + Grafana for anything production-facing.

## License

MIT
