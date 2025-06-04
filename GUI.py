#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import subprocess
import threading
import time
import psutil
import os
import signal
import sys

class SystemMonitorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Resource Monitor") # Window title, can also be changed if desired
        self.root.geometry("600x500")
        
        # Process tracking
        self.monitor_process = None
        self.is_monitoring = False
        self.stats_thread = None
        self.stop_stats = False
        
        self.setup_ui()
        self.start_realtime_stats()
    
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Resource Monitor", # MODIFIED: Changed title text
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Real-time stats frame
        stats_frame = ttk.LabelFrame(main_frame, text="Real-time System Stats", padding="10")
        stats_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        stats_frame.columnconfigure(1, weight=1)
        
        # CPU Usage
        ttk.Label(stats_frame, text="CPU Usage:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.cpu_var = tk.StringVar(value="0.0%")
        self.cpu_label = ttk.Label(stats_frame, textvariable=self.cpu_var, 
                                  font=("Arial", 12, "bold"), foreground="blue")
        self.cpu_label.grid(row=0, column=1, sticky=tk.W)
        
        # CPU Progress bar
        self.cpu_progress = ttk.Progressbar(stats_frame, length=200, mode='determinate')
        self.cpu_progress.grid(row=0, column=2, padx=(10, 0))
        
        # Memory Usage
        ttk.Label(stats_frame, text="Memory Usage:").grid(row=1, column=0, sticky=tk.W, padx=(0, 10), pady=(5, 0))
        self.mem_var = tk.StringVar(value="0.0%")
        self.mem_label = ttk.Label(stats_frame, textvariable=self.mem_var, 
                                  font=("Arial", 12, "bold"), foreground="green")
        self.mem_label.grid(row=1, column=1, sticky=tk.W, pady=(5, 0))
        
        # Memory Progress bar
        self.mem_progress = ttk.Progressbar(stats_frame, length=200, mode='determinate')
        self.mem_progress.grid(row=1, column=2, padx=(10, 0), pady=(5, 0))
        
        # Control buttons frame
        control_frame = ttk.LabelFrame(main_frame, text="Monitor Control", padding="10")
        control_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Start button
        self.start_btn = ttk.Button(control_frame, text="Start Monitoring", 
                                   command=self.start_monitoring, style="Success.TButton")
        self.start_btn.grid(row=0, column=0, padx=(0, 10))
        
        # Stop button
        self.stop_btn = ttk.Button(control_frame, text="Stop Monitoring", 
                                  command=self.stop_monitoring, state="disabled")
        self.stop_btn.grid(row=0, column=1, padx=(0, 10))
        
        # Status label
        self.status_var = tk.StringVar(value="") # MODIFIED: Removed initial text
        self.status_label = ttk.Label(control_frame, textvariable=self.status_var, 
                                     font=("Arial", 10), foreground="gray")
        self.status_label.grid(row=0, column=2, padx=(20, 0))
        
        # Log display frame
        log_frame = ttk.LabelFrame(main_frame, text="Monitor Log Output", padding="10")
        log_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(3, weight=1)
        
        # Log text area
        self.log_text = scrolledtext.ScrolledText(log_frame, height=10, width=70)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Clear log button
        clear_btn = ttk.Button(log_frame, text="Clear Log", command=self.clear_log)
        clear_btn.grid(row=1, column=0, pady=(5, 0))
        
    def start_realtime_stats(self):
        """Start the real-time stats update thread"""
        if not self.stats_thread or not self.stats_thread.is_alive():
            self.stop_stats = False
            self.stats_thread = threading.Thread(target=self.update_realtime_stats, daemon=True)
            self.stats_thread.start()
    
    def update_realtime_stats(self):
        """Update real-time CPU and memory stats"""
        while not self.stop_stats:
            try:
                # Get system stats
                cpu_percent = psutil.cpu_percent(interval=0.1)
                memory_info = psutil.virtual_memory()
                mem_percent = memory_info.percent
                
                # Update GUI in main thread
                self.root.after(0, self.update_stats_display, cpu_percent, mem_percent)
                
                time.sleep(1)  # Update every second
            except Exception as e:
                print(f"Error updating stats: {e}")
                break
    
    def update_stats_display(self, cpu_percent, mem_percent):
        """Update the stats display in the GUI"""
        self.cpu_var.set(f"{cpu_percent:.1f}%")
        self.mem_var.set(f"{mem_percent:.1f}%")
        
        # Update progress bars
        self.cpu_progress['value'] = cpu_percent
        self.mem_progress['value'] = mem_percent
        
        # Change colors based on usage levels
        if cpu_percent > 80:
            self.cpu_label.configure(foreground="red")
        elif cpu_percent > 60:
            self.cpu_label.configure(foreground="orange")
        else:
            self.cpu_label.configure(foreground="blue")
            
        if mem_percent > 80:
            self.mem_label.configure(foreground="red")
        elif mem_percent > 60:
            self.mem_label.configure(foreground="orange")
        else:
            self.mem_label.configure(foreground="green")
    
    def start_monitoring(self):
        """Start the system monitor script"""
        if self.is_monitoring:
            return
            
        try:
            # Check if the script file exists
            if not os.path.exists("system_monitor.py"):
                messagebox.showerror("Error", "system_monitor.py not found in current directory!")
                return
            
            # Start the monitoring process
            self.monitor_process = subprocess.Popen(
                [sys.executable, "system_monitor.py"],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1
            )
            
            self.is_monitoring = True
            self.start_btn.configure(state="disabled")
            self.stop_btn.configure(state="normal")
            self.status_var.set("Monitoring active - logging to system_monitor.log2") # This will appear when monitoring starts
            
            # Start thread to read output
            threading.Thread(target=self.read_process_output, daemon=True).start()
            
            self.log_message("System monitoring started successfully")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start monitoring: {str(e)}")
            self.log_message(f"Error starting monitoring: {str(e)}")
    
    def stop_monitoring(self):
        """Stop the system monitor script"""
        if not self.is_monitoring or not self.monitor_process:
            return
            
        try:
            # Terminate the process
            if self.monitor_process.poll() is None:  # Process is still running
                self.monitor_process.terminate()
                
                # Wait a bit for graceful termination
                try:
                    self.monitor_process.wait(timeout=3)
                except subprocess.TimeoutExpired:
                    # Force kill if it doesn't terminate gracefully
                    self.monitor_process.kill()
                    self.monitor_process.wait()
            
            self.is_monitoring = False
            self.monitor_process = None
            self.start_btn.configure(state="normal")
            self.stop_btn.configure(state="disabled")
            self.status_var.set("Monitoring stopped") # This will appear when monitoring stops
            
            self.log_message("System monitoring stopped")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to stop monitoring: {str(e)}")
            self.log_message(f"Error stopping monitoring: {str(e)}")
    
    def read_process_output(self):
        """Read output from the monitoring process"""
        if not self.monitor_process:
            return
            
        try:
            for line in iter(self.monitor_process.stdout.readline, ''):
                if line:
                    # Update GUI in main thread
                    self.root.after(0, self.log_message, line.strip())
                    
                # Check if process has ended
                if self.monitor_process.poll() is not None:
                    break
                    
        except Exception as e:
            self.root.after(0, self.log_message, f"Error reading process output: {str(e)}")
        
        # Process has ended
        if self.is_monitoring:
            self.root.after(0, self.monitoring_finished)
    
    def monitoring_finished(self):
        """Called when monitoring process finishes"""
        self.is_monitoring = False
        self.monitor_process = None
        self.start_btn.configure(state="normal")
        self.stop_btn.configure(state="disabled")
        self.status_var.set("Monitoring completed") # This will appear when monitoring completes
        self.log_message("System monitoring completed")
    
    def log_message(self, message):
        """Add a message to the log display"""
        timestamp = time.strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
    
    def clear_log(self):
        """Clear the log display"""
        self.log_text.delete(1.0, tk.END)
    
    def on_closing(self):
        """Handle window closing"""
        self.stop_stats = True
        if self.is_monitoring:
            self.stop_monitoring()
        self.root.destroy()

def main():
    root = tk.Tk()
    app = SystemMonitorGUI(root)
    
    # Handle window closing
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    
    # Configure style for better button appearance
    style = ttk.Style()
    try:
        style.configure("Success.TButton", foreground="green")
    except:
        pass  # Style might not be available on all systems
    
    root.mainloop()

if __name__ == "__main__":
    main()