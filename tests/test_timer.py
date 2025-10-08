"""Tests for PerfsTimer."""

import time
import io
import sys
from perfs_timer import PerfsTimer


def test_basic_timing():
    """Test basic start/stop functionality."""
    timer = PerfsTimer()
    timer.start("test")
    time.sleep(0.1)
    timer.stop("test")

    assert "test" in timer._starts
    assert "test" in timer._stops
    duration = timer._stops["test"] - timer._starts["test"]
    assert 0.09 < duration < 0.15  # Allow some margin


def test_multiple_timers():
    """Test multiple named timers."""
    timer = PerfsTimer()

    timer.start("task1")
    time.sleep(0.05)
    timer.stop("task1")

    timer.start("task2")
    time.sleep(0.05)
    timer.stop("task2")

    assert len(timer._starts) == 2
    assert len(timer._stops) == 2
    assert "task1" in timer._starts
    assert "task2" in timer._starts


def test_reset():
    """Test that reset clears all timers."""
    timer = PerfsTimer()

    timer.start("test")
    timer.stop("test")

    assert len(timer._starts) == 1
    assert len(timer._stops) == 1

    timer.reset()

    assert len(timer._starts) == 0
    assert len(timer._stops) == 0

    timer.start("after_reset")
    timer.stop("after_reset")

    assert len(timer._starts) == 1
    assert "after_reset" in timer._starts
    assert "test" not in timer._starts


def test_running_timer():
    """Test that running (non-stopped) timers are indicated."""
    timer = PerfsTimer()

    timer.start("completed")
    timer.stop("completed")

    timer.start("still_running")
    # Don't stop this one

    assert "completed" in timer._starts
    assert "completed" in timer._stops
    assert "still_running" in timer._starts
    assert "still_running" not in timer._stops


def test_order_preserved():
    """Test that timers are printed in the order they were started."""
    timer = PerfsTimer()

    timer.start("first")
    timer.stop("first")

    timer.start("second")
    timer.stop("second")

    timer.start("third")
    timer.stop("third")

    keys = list(timer._starts.keys())
    assert keys == ["first", "second", "third"]


def test_prints_output():
    """Test that prints() outputs correct formatted content."""
    timer = PerfsTimer()

    timer.start("completed_task")
    time.sleep(0.1)
    timer.stop("completed_task")

    timer.start("running_task")
    # Don't stop this one

    # Capture stdout
    captured_output = io.StringIO()
    sys.stdout = captured_output

    timer.prints()

    # Restore stdout
    sys.stdout = sys.__stdout__

    output = captured_output.getvalue()

    # Check for expected content
    assert "Performance Report" in output
    assert "completed_task" in output
    assert "running_task" in output
    assert "RUNNING" in output
    assert "s" in output  # Check for seconds indicator
    assert "=" in output  # Check for formatting lines

    # Verify completed task shows a duration
    lines = output.split("\n")
    completed_line = [line for line in lines if "completed_task" in line][0]
    assert "0." in completed_line  # Should have a numeric duration

    # Verify running task shows RUNNING status
    running_line = [line for line in lines if "running_task" in line][0]
    assert "RUNNING" in running_line
