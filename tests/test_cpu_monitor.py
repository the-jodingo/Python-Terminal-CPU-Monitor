"""Tests for the CPU monitor helpers."""

from collections import deque

import pytest

from cpu_monitor import build_history_bar, format_load, top_n


def test_top_n_sorts_descending():
    procs = [{"pid": 1, "cpu_percent": 5.0},
             {"pid": 2, "cpu_percent": 50.0},
             {"pid": 3, "cpu_percent": 20.0}]
    out = top_n(procs, n=2)
    assert [p["pid"] for p in out] == [2, 3]


def test_top_n_handles_missing_cpu_percent():
    procs = [{"pid": 1}, {"pid": 2, "cpu_percent": 10.0}]
    assert top_n(procs, n=5)[0]["pid"] == 2


def test_build_history_bar_thresholds():
    hist = deque([10.0, 50.0, 90.0], maxlen=20)
    bar = build_history_bar(hist)
    assert len(bar) == 3
    assert bar[0] != bar[1] != bar[2]


def test_format_load():
    assert format_load((0.5, 1.25, 2.0)) == "0.50 / 1.25 / 2.00"


def test_top_n_empty():
    assert top_n([], n=3) == []
