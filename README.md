# Resource Monitor & System Logging Application

## Overview

This project consists of two Python scripts:

1.  **`system_monitor.py`**: A backend script that monitors and logs system CPU and memory usage to a file (`system_monitor.log`).
2.  **`gui.py`**: A Tkinter-based graphical user interface (GUI) that provides real-time system statistics (CPU and Memory usage) and allows users to start and stop the `system_monitor.py` script. It also displays the log output from the monitoring script directly in the GUI.

## Features

### `system_monitor_gui.py` (Resource Monitor GUI)
* **Real-time Stats Display**:
    * Shows current CPU usage percentage with a progress bar.
    * Shows current Memory usage percentage with a progress bar.
    * Usage percentages change color (blue/green for normal, orange for moderate, red for high).
* **Monitor Control**:
    * "Start Monitoring" button to initiate the `system_monitor.py` script.
    * "Stop Monitoring" button to terminate the `system_monitor.py` script.
    * Status label indicating the current state of the monitoring process.
* **Log Display**:
    * A scrolled text area displays messages from the GUI and the standard output of `system_monitor.py`.
    * "Clear Log" button to clear the log display area in the GUI.
* **Automatic Shutdown**: Gracefully stops the monitoring script if the GUI window is closed.

### `system_monitor.py` (Backend Monitoring Script)
* **System Resource Logging**: Logs CPU and Memory usage to `system_monitor.log2`.
* **Configurable**:
    * `LOG_FILE`: Defines the name of the log file (default: "system_monitor.log").
    * `SAMPLING_INTERVAL_SECONDS`: How often to log data (default: 10 seconds).
    * `MONITOR_DURATION_SECONDS`: Total time the script will monitor for if not stopped manually (default: 360 seconds / 6 minutes).
* **Console Output**: Prints status messages to the console (which are captured by the GUI).
* **Error Handling**: Logs errors and user interruptions (Ctrl+C).

## Prerequisites

* Python 3
* `psutil` library: For fetching system information like CPU and memory usage.
* `tkinter`: For the GUI. This is usually included with standard Python installations.

You can install `psutil` using pip:
```bash
pip install psutil
