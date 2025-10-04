"""CLI banner utilities for the Atlas API."""

from __future__ import annotations

GOLD = "\033[38;5;220m"
RESET = "\033[0m"


def print_banner() -> None:
    """Emit a gold-on-black Atlas banner in the terminal."""

    banner = r"""
      ___  _____ _             
     / _ \|  ___| | __ _ ___   
    / /_\ \ |_  | |/ _` / __|  
    |  _  |  _| | | (_| \__ \  
    |_| |_|_|   |_|\__,_|___/  
    """
    tagline = "Atlas API ready · Offline-first · Black & Gold"
    print(f"{GOLD}{banner}{RESET}")
    print(f"{GOLD}{tagline}{RESET}")
