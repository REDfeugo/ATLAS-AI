"""System information helpers."""

from __future__ import annotations

import platform
from typing import Dict

import psutil


def system_stats() -> Dict[str, str]:
    """Return CPU, RAM, and battery information."""

    cpu_percent = psutil.cpu_percent(interval=0.1)
    mem = psutil.virtual_memory()
    battery = psutil.sensors_battery()
    details = {
        "cpu_percent": cpu_percent,
        "memory_percent": mem.percent,
        "platform": platform.platform(),
    }
    if battery:
        details["battery_percent"] = battery.percent
    return {"status": "ok", "details": details}
