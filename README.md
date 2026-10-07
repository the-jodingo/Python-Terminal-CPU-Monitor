[![CI](https://github.com/the-jodingo/Python-Terminal-CPU-Monitor/actions/workflows/ci.yml/badge.svg)](https://github.com/the-jodingo/Python-Terminal-CPU-Monitor/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![psutil](https://img.shields.io/badge/psutil-required-4B8BBE)](https://github.com/giampaolo/psutil)
[![rich](https://img.shields.io/badge/rich-required-8A2BE2)](https://github.com/Textualize/rich)
[![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20macOS-lightgrey)](https://www.kernel.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

# Python Terminal CPU Monitor

A live terminal dashboard for CPU usage: overall utilisation, per-core
breakdown, load average, a rolling history bar, and the top CPU-consuming
processes — refreshed in place.

## Table of contents

- [Requirements](#requirements)
- [Install](#install)
- [Usage](#usage)
- [What it shows](#what-it-shows)
- [Testing and CI](#testing-and-ci)
- [Notes](#notes)
- [License](#license)

## Requirements

| Tool | Version |
|---|---|
| Python | 3.11+ |
| `psutil` | >= 5.9 |
| `rich` | >= 13.0 |

## Install

```bash
git clone https://github.com/the-jodingo/Python-Terminal-CPU-Monitor.git
cd Python-Terminal-CPU-Monitor
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Usage

```bash
python3 cpu_monitor.py
```

Press `Ctrl+C` to exit. The dashboard refreshes twice per second.

## What it shows

| Metric | Source |
|---|---|
| Overall CPU usage | `psutil.cpu_percent()` |
| Per-core usage | `psutil.cpu_percent(percpu=True)` — first 8 cores, with a count of the rest |
| Load average (1/5/15 min) | `os.getloadavg()` |
| History bar | Rolling 20-sample window of overall CPU |
| Top processes | `psutil.process_iter()`, sorted by `cpu_percent` |

## Testing and CI

```bash
pip install -r requirements-dev.txt
pytest -q
```

GitHub Actions runs the suite on Linux and macOS, Python 3.11 and 3.12.

## Notes

- **macOS load average differs from Linux** — macOS counts runnable + blocked
  threads, so the figures are not directly comparable. The tool is primarily
  aimed at Linux.
- Processes that exit mid-sample are skipped rather than crashing the loop.
- Want alerts on sustained high CPU? Extend with `smtplib`, or move to
  Prometheus + Grafana for anything production-facing.

## License

[MIT](LICENSE) © Joash Odingo
