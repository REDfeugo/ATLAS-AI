"""Simple in-memory rate limiting utilities."""

from __future__ import annotations

import time
from collections import defaultdict, deque
from typing import Deque, DefaultDict


class SlidingWindowRateLimiter:
    """Track calls per key within a moving one-minute window."""

    def __init__(self, max_per_minute: int) -> None:
        self.max_per_minute = max_per_minute
        self.calls: DefaultDict[str, Deque[float]] = defaultdict(deque)

    def allow(self, key: str) -> bool:
        """Return True if the caller is still within the rate limit."""

        now = time.time()
        window_start = now - 60
        queue = self.calls[key]
        while queue and queue[0] < window_start:
            queue.popleft()
        if len(queue) >= self.max_per_minute:
            return False
        queue.append(now)
        return True
