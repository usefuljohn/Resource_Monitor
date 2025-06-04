#! /usr/bin/python3
import psutil
import time
import logging
import datetime

# Configuration
LOG_FILE = "system_monitor.log"
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
SAMPLING_INTERVAL_SECONDS = 10  # Log data every 10 seconds
MONITOR_DURATION_SECONDS = 360 # Monitor for 6 minutes (360 seconds)

def setup_logger():
    """Configures the logger to write to a file."""
    logging.basicConfig(filename=LOG_FILE,
                        level=logging.INFO,
                        format=LOG_FORMAT,
                        filemode='a') # Append to the log file if it exists

def get_system_stats():
    """Retrieves CPU and memory usage."""
    cpu_usage = psutil.cpu_percent(interval=1)  # Interval for CPU measurement
    memory_info = psutil.virtual_memory()
    memory_usage = memory_info.percent
    return cpu_usage, memory_usage

def log_stats(cpu, mem):
    """Logs the CPU and memory usage."""
    logging.info(f"CPU Usage: {cpu}% | Memory Usage: {mem}%")

def monitor_system(duration_seconds, interval_seconds):
    """
    Monitors system CPU and memory usage for a specified duration
    and logs the data at given intervals.

    Args:
        duration_seconds (int): Total time in seconds to monitor the system.
        interval_seconds (int): Time in seconds between each log entry.
    """
    start_time = time.time()
    end_time = start_time + duration_seconds

    logging.info(f"Starting system monitoring for {duration_seconds} seconds "
                 f"(sampling every {interval_seconds} seconds). Logging to {LOG_FILE}")
    print(f"Monitoring system... Press Ctrl+C to stop early. Data is being logged to {LOG_FILE}")

    try:
        while time.time() < end_time:
            cpu, mem = get_system_stats()
            log_stats(cpu, mem)
            # Wait for the next interval, considering the time taken by get_system_stats
            time_to_sleep = interval_seconds - (time.time() - start_time) % interval_seconds
            if time_to_sleep > 0:
                time.sleep(time_to_sleep)
    except KeyboardInterrupt:
        logging.info("System monitoring stopped by user.")
        print("System monitoring stopped by user.")
    except Exception as e:
        logging.error(f"An error occurred during monitoring: {e}")
        print(f"An error occurred: {e}")
    finally:
        logging.info("System monitoring finished.")
        print("System monitoring finished.")

if __name__ == "__main__":
    setup_logger()
    monitor_system(MONITOR_DURATION_SECONDS, SAMPLING_INTERVAL_SECONDS)
