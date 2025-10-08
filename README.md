# PerfsTimer

A simple, lightweight performance timer for measuring execution time of code blocks in Python.

## Installation

```bash
pip install perfs-timer
```

## Usage
```python
from perfs_timer import PerfsTimer

timer = PerfsTimer()

# Time a code block
timer.start("my_operation")
# ... your code here ...
timer.stop("my_operation")

# Print all results
timer.prints()