"""
Printer Automation - Step 1: GUI Foundation
Implements: Tkinter GUI with Start/Stop, counter, and live logging
"""

import tkinter as tk
from tkinter import scrolledtext
import logging
from logging.handlers import QueueHandler
import queue
import threading
from datetime import datetime
import printer_automation_logic



class PrinterAutomationGUI:
    def __init__(self, root):
        self.root = root
        print(self.root.__dict__)
        self.root.title("Printer Automation Control")
        self.root.attributes('-topmost', True)
        
        
        #self.root.geometry("600x500")
        #self.root.resizable(True, True)
        
        # State variables
        self.is_running = False
        self.items_printed = 0
        self.automation_thread = None
        self.delay_seconds = 2.0
        self.automation_lib = printer_automation_logic.AutomationFramework()
                
        # Build GUI
        self.build_gui()
    
    
    def build_gui(self):
        """Create the GUI layout"""
        
        # ===== TOP SECTION: Title and Status =====
        top_frame = tk.Frame(self.root, bg="#f0f0f0", pady=10)
        top_frame.pack(fill=tk.X, padx=10, pady=(10, 0))
        
        title = tk.Label(
            top_frame,
            text="Printer Automation Control",
            font=("Arial", 14, "bold"),
            bg="#f0f0f0"
        )
        title.pack()
        
        # ===== STATUS SECTION =====
        status_frame = tk.Frame(self.root, bg="#e8f5e9", relief=tk.RAISED, bd=1)
        status_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Status indicator
        self.status_label = tk.Label(
            status_frame,
            text="Status: IDLE",
            font=("Arial", 11, "bold"),
            bg="#e8f5e9",
            fg="#1b5e20"
        )
        self.status_label.pack(anchor=tk.W, padx=10, pady=5)
        
        # Item counter
        self.counter_label = tk.Label(
            status_frame,
            text="Items Printed: 0",
            font=("Arial", 11),
            bg="#e8f5e9"
        )
        self.counter_label.pack(anchor=tk.W, padx=10, pady=5)
        
        # ===== CONTROL BUTTONS SECTION =====
        button_frame = tk.Frame(self.root)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.start_button = tk.Button(
            button_frame,
            text="▶ START",
            font=("Arial", 11, "bold"),
            bg="#4caf50",
            fg="white",
            padx=20,
            pady=8,
            cursor="hand2",
            command=self.start_automation
        )
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        self.stop_button = tk.Button(
            button_frame,
            text="⏹ STOP",
            font=("Arial", 11, "bold"),
            bg="#f44336",
            fg="white",
            padx=20,
            pady=8,
            cursor="hand2",
            command=self.stop_automation,
            state=tk.DISABLED
        )
        self.stop_button.pack(side=tk.LEFT, padx=5)
        
        self.reset_button = tk.Button(
            button_frame,
            text="Reset Counter",
            font=("Arial", 10),
            bg="#2196f3",
            fg="white",
            padx=15,
            pady=6,
            cursor="hand2",
            command=self.reset_counter
        )
        self.reset_button.pack(side=tk.LEFT, padx=5)
        
        delay_frame = tk.Frame(self.root, bg="#f5f5f5", relief=tk.SUNKEN, bd=1)
        delay_frame.pack(fill=tk.X, padx=10, pady=10)
        delay_label = tk.Label(
            delay_frame,
            text="Delay Between Jobs (seconds):",
            font=("Arial", 10),
            bg="#f5f5f5"
            )
        delay_label.pack(anchor=tk.W, padx=10, pady=(8, 2))

        self.delay_entry = tk.Entry(
            delay_frame,
            font=("Arial", 11),
            width=10
            )
        self.delay_entry.pack(anchor=tk.W, padx=10, pady=(0, 8))
        self.delay_entry.insert(0, "120.0")  # Default value
       
        
    
    def start_automation(self):
        """Start the automation process"""
        
        try:
            self.delay_seconds = float(self.delay_entry.get())
            if self.delay_seconds < 0:
                self.delay_seconds = 0
        except ValueError:
            self.delay_seconds = 2.0
            self.delay_entry.delete(0, tk.END)
            self.delay_entry.insert(0, "1.0")
        
        self.is_running = True
        self.update_status("RUNNING", "#1b5e20")
        
        # Disable start, enable stop
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.delay_entry.config(state=tk.DISABLED)  # Lock it
        
        # Start automation in a separate thread
        self.automation_thread = threading.Thread(target=self.run_automation, daemon=True)
        self.automation_thread.start()

    
    def stop_automation(self):
        """Stop the automation process"""
        self.is_running = False
        self.update_status("STOPPED", "#b71c1c")
        
        # Disable stop, enable start
        self.stop_button.config(state=tk.DISABLED)
        self.start_button.config(state=tk.NORMAL)
        self.delay_entry.config(state=tk.NORMAL)

    
    def reset_counter(self):
        """Reset the items printed counter"""
        self.items_printed = 0
        self.counter_label.config(text="Items Printed: 0")
 
 
    def update_counter(self):
        """Update the counter label (call from main thread)"""
        self.counter_label.config(text=f"Items Printed: {self.items_printed}")
    
    def update_status(self, status_text, color):
        """Update the status label"""
        self.status_label.config(text=f"Status: {status_text}", fg=color)
    
    def is_running_check(self):
        """Update the status label"""
        return(self.is_running)
    
    def run_automation(self):
        """
        Main automation loop (runs in a separate thread)
        Currently just simulates activity - we'll add actual automation later
        """
    
        
        # Simulate some work
        try:
            print("Start automation")
            self.automation_lib.main_logic(self.is_running_check, self.delay_seconds)
        
        finally:
            # Ensure we stop gracefully
            if self.is_running:
                self.is_running = False
                self.root.after(0, self.stop_automation)

def main():
    root = tk.Tk()
    app = PrinterAutomationGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
