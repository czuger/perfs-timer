"""Core timer implementation."""

import time
from collections import OrderedDict
from typing import Dict


class PerfsTimer:
    """Simple performance timer to measure execution time of code blocks."""

    def __init__(self) -> None:
        """Initialize the timer with empty performance records."""
        self._starts: Dict[str, float] = OrderedDict()
        self._stops: Dict[str, float] = OrderedDict()

    def start(self, name: str) -> None:
        """Start timing a named performance block.

        Args:
            name: Identifier for the performance block
        """
        self._starts[name] = time.perf_counter()

    def stop(self, name: str) -> None:
        """Stop timing a named performance block.

        Args:
            name: Identifier for the performance block
        """
        self._stops[name] = time.perf_counter()

    def prints(self) -> None:
        """Print a formatted performance report of all timers."""
        print("\n" + "=" * 50)
        print("Performance Report".center(50))
        print("=" * 50)

        for name in self._starts:
            if name not in self._stops:
                print(f"{name:.<40} RUNNING")
            else:
                duration = self._stops[name] - self._starts[name]
                print(f"{name:.<40} {duration:>8.4f}s")

        print("=" * 50 + "\n")

    def reset(self) -> None:
        """Clear all performance records."""
        self._starts.clear()
        self._stops.clear()
