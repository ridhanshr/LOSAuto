#!/usr/bin/env python3
"""
GUI Application for LOS Automation
This application provides a graphical interface to run different LOS automation scripts
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import subprocess
import sys
import os

# Add project root to path to allow running this script directly
from src.config import config
if config.root_dir not in sys.path:
    sys.path.insert(0, config.root_dir)

import threading
import time
from datetime import datetime
from src.utils.driver_manager import sync_drivers

class LOSAutomationGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("LOS Automation Suite")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # Set window icon (if available)
        try:
            self.root.iconbitmap('favicon.ico')
        except:
            pass
        
        # Create main container
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create header
        self.create_header()
        
        # Create notebook for different automation types
        self.create_notebook()
        
        # Create status bar
        self.create_status_bar()
        
        # Create log area
        self.create_log_area()
        
        # Initialize variables
        self.running_process = None
        self.stop_event = threading.Event()
    
    def create_header(self):
        """Create the header section"""
        header_frame = ttk.Frame(self.main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        title_label = ttk.Label(
            header_frame,
            text="LOS Automation Suite",
            font=('Helvetica', 16, 'bold')
        )
        title_label.pack(side=tk.LEFT)
        
        # Add version info
        version_label = ttk.Label(
            header_frame,
            text="v1.0",
            font=('Helvetica', 10)
        )
        version_label.pack(side=tk.RIGHT)
    
    def create_notebook(self):
        """Create the notebook with different automation tabs"""
        notebook = ttk.Notebook(self.main_frame)
        notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create tabs
        self.main_los_tab = self.create_main_los_tab(notebook)
        self.supplement_tab = self.create_supplement_tab(notebook)
        self.addon_los_tab = self.create_addon_los_tab(notebook)
        self.addon_supp_tab = self.create_addon_supp_tab(notebook)
        self.cobrand_tab = self.create_cobrand_tab(notebook)
        self.recontest_tab = self.create_recontest_tab(notebook)
        self.settings_tab = self.create_settings_tab(notebook)
        
        # Add tabs to notebook
        notebook.add(self.main_los_tab, text="Main LOS")
        notebook.add(self.supplement_tab, text="Supplement LOS")
        notebook.add(self.addon_los_tab, text="Add-On LOS")
        notebook.add(self.addon_supp_tab, text="Add-On Supp LOS")
        notebook.add(self.cobrand_tab, text="LOS Cobrand")
        notebook.add(self.recontest_tab, text="LOS Recontest")
        notebook.add(self.settings_tab, text="Settings")
    
    def create_main_los_tab(self, notebook):
        """Create the Main LOS tab"""
        tab = ttk.Frame(notebook)
        
        # Description
        desc_frame = ttk.Frame(tab)
        desc_frame.pack(fill=tk.X, pady=5)
        
        desc_label = ttk.Label(
            desc_frame,
            text="Main LOS Automation - Complete loan origination process",
            wraplength=700
        )
        desc_label.pack()
        
        # Configuration options
        config_frame = ttk.LabelFrame(tab, text="Configuration", padding=10)
        config_frame.pack(fill=tk.X, pady=5, padx=5)
        
        # Browser selection
        browser_frame = ttk.Frame(config_frame)
        browser_frame.pack(fill=tk.X, pady=5)
        
        browser_label = ttk.Label(browser_frame, text="Browser:")
        browser_label.pack(side=tk.LEFT)
        
        self.browser_var = tk.StringVar(value="edge")
        browser_combo = ttk.Combobox(
            browser_frame,
            textvariable=self.browser_var,
            values=["edge", "chrome"],
            state="readonly",
            width=10
        )
        browser_combo.pack(side=tk.LEFT, padx=5)
        
        # Data file selection
        data_frame = ttk.Frame(config_frame)
        data_frame.pack(fill=tk.X, pady=5)
        
        data_label = ttk.Label(data_frame, text="Data File:")
        data_label.pack(side=tk.LEFT)
        
        self.data_file_var = tk.StringVar(value="Data/LOSData.xlsx")
        data_entry = ttk.Entry(data_frame, textvariable=self.data_file_var, width=50)
        data_entry.pack(side=tk.LEFT, padx=5)
        
        data_browse_btn = ttk.Button(
            data_frame,
            text="Browse",
            command=self.browse_data_file
        )
        data_browse_btn.pack(side=tk.LEFT)
        
        # Run button
        btn_frame = ttk.Frame(tab)
        btn_frame.pack(fill=tk.X, pady=10)
        
        run_btn = ttk.Button(
            btn_frame,
            text="Run Main LOS Automation",
            command=lambda: self.run_automation("src.scripts.main_los"),
            style="Accent.TButton"
        )
        run_btn.pack(pady=10)
        
        return tab
    
    def create_supplement_tab(self, notebook):
        """Create the Supplement LOS tab"""
        tab = ttk.Frame(notebook)
        
        # Description
        desc_frame = ttk.Frame(tab)
        desc_frame.pack(fill=tk.X, pady=5)
        
        desc_label = ttk.Label(
            desc_frame,
            text="Supplement LOS Automation - Supplement loan process",
            wraplength=700
        )
        desc_label.pack()
        
        # Configuration options
        config_frame = ttk.LabelFrame(tab, text="Configuration", padding=10)
        config_frame.pack(fill=tk.X, pady=5, padx=5)
        
        # Browser selection
        browser_frame = ttk.Frame(config_frame)
        browser_frame.pack(fill=tk.X, pady=5)
        
        browser_label = ttk.Label(browser_frame, text="Browser:")
        browser_label.pack(side=tk.LEFT)
        
        self.browser_supp_var = tk.StringVar(value="edge")
        browser_combo = ttk.Combobox(
            browser_frame,
            textvariable=self.browser_supp_var,
            values=["edge", "chrome"],
            state="readonly",
            width=10
        )
        browser_combo.pack(side=tk.LEFT, padx=5)
        
        # Data file selection
        data_frame = ttk.Frame(config_frame)
        data_frame.pack(fill=tk.X, pady=5)
        
        data_label = ttk.Label(data_frame, text="Data File:")
        data_label.pack(side=tk.LEFT)
        
        self.data_file_supp_var = tk.StringVar(value="Data/LOSData.xlsx")
        data_entry = ttk.Entry(data_frame, textvariable=self.data_file_supp_var, width=50)
        data_entry.pack(side=tk.LEFT, padx=5)
        
        data_browse_btn = ttk.Button(
            data_frame,
            text="Browse",
            command=lambda: self.browse_data_file(var=self.data_file_supp_var)
        )
        data_browse_btn.pack(side=tk.LEFT)
        
        # Run button
        btn_frame = ttk.Frame(tab)
        btn_frame.pack(fill=tk.X, pady=10)
        
        run_btn = ttk.Button(
            btn_frame,
            text="Run Supplement LOS Automation",
            command=lambda: self.run_automation("src.scripts.supplement_los"),
            style="Accent.TButton"
        )
        run_btn.pack(pady=10)
        
        return tab
    
    def create_addon_los_tab(self, notebook):
        """Create the Add-On LOS tab"""
        tab = ttk.Frame(notebook)
        
        # Description
        desc_frame = ttk.Frame(tab)
        desc_frame.pack(fill=tk.X, pady=5)
        
        desc_label = ttk.Label(
            desc_frame,
            text="Add-On LOS Automation - Add-on card process",
            wraplength=700
        )
        desc_label.pack()
        
        # Configuration options
        config_frame = ttk.LabelFrame(tab, text="Configuration", padding=10)
        config_frame.pack(fill=tk.X, pady=5, padx=5)
        
        # Browser selection
        browser_frame = ttk.Frame(config_frame)
        browser_frame.pack(fill=tk.X, pady=5)
        
        browser_label = ttk.Label(browser_frame, text="Browser:")
        browser_label.pack(side=tk.LEFT)
        
        self.browser_addon_var = tk.StringVar(value="edge")
        browser_combo = ttk.Combobox(
            browser_frame,
            textvariable=self.browser_addon_var,
            values=["edge", "chrome"],
            state="readonly",
            width=10
        )
        browser_combo.pack(side=tk.LEFT, padx=5)
        
        # Data file selection
        data_frame = ttk.Frame(config_frame)
        data_frame.pack(fill=tk.X, pady=5)
        
        data_label = ttk.Label(data_frame, text="Data File:")
        data_label.pack(side=tk.LEFT)
        
        self.data_file_addon_var = tk.StringVar(value="Data/LOSData.xlsx")
        data_entry = ttk.Entry(data_frame, textvariable=self.data_file_addon_var, width=50)
        data_entry.pack(side=tk.LEFT, padx=5)
        
        data_browse_btn = ttk.Button(
            data_frame,
            text="Browse",
            command=lambda: self.browse_data_file(var=self.data_file_addon_var)
        )
        data_browse_btn.pack(side=tk.LEFT)
        
        # Run button
        btn_frame = ttk.Frame(tab)
        btn_frame.pack(fill=tk.X, pady=10)
        
        run_btn = ttk.Button(
            btn_frame,
            text="Run Add-On LOS Automation",
            command=lambda: self.run_automation("src.scripts.addon_los"),
            style="Accent.TButton"
        )
        run_btn.pack(pady=10)
        
        return tab
    
    def create_addon_supp_tab(self, notebook):
        """Create the Add-On Supplement LOS tab"""
        tab = ttk.Frame(notebook)
        
        # Description
        desc_frame = ttk.Frame(tab)
        desc_frame.pack(fill=tk.X, pady=5)
        
        desc_label = ttk.Label(
            desc_frame,
            text="Add-On Supplement LOS Automation - Add-on supplement process",
            wraplength=700
        )
        desc_label.pack()
        
        # Configuration options
        config_frame = ttk.LabelFrame(tab, text="Configuration", padding=10)
        config_frame.pack(fill=tk.X, pady=5, padx=5)
        
        # Browser selection
        browser_frame = ttk.Frame(config_frame)
        browser_frame.pack(fill=tk.X, pady=5)
        
        browser_label = ttk.Label(browser_frame, text="Browser:")
        browser_label.pack(side=tk.LEFT)
        
        self.browser_addon_supp_var = tk.StringVar(value="edge")
        browser_combo = ttk.Combobox(
            browser_frame,
            textvariable=self.browser_addon_supp_var,
            values=["edge", "chrome"],
            state="readonly",
            width=10
        )
        browser_combo.pack(side=tk.LEFT, padx=5)
        
        # Data file selection
        data_frame = ttk.Frame(config_frame)
        data_frame.pack(fill=tk.X, pady=5)
        
        data_label = ttk.Label(data_frame, text="Data File:")
        data_label.pack(side=tk.LEFT)
        
        self.data_file_addon_supp_var = tk.StringVar(value="Data/LOSData.xlsx")
        data_entry = ttk.Entry(data_frame, textvariable=self.data_file_addon_supp_var, width=50)
        data_entry.pack(side=tk.LEFT, padx=5)
        
        data_browse_btn = ttk.Button(
            data_frame,
            text="Browse",
            command=lambda: self.browse_data_file(var=self.data_file_addon_supp_var)
        )
        data_browse_btn.pack(side=tk.LEFT)
        
        # Run button
        btn_frame = ttk.Frame(tab)
        btn_frame.pack(fill=tk.X, pady=10)
        
        run_btn = ttk.Button(
            btn_frame,
            text="Run Add-On Supplement LOS Automation",
            command=lambda: self.run_automation("src.scripts.addon_supp_los"),
            style="Accent.TButton"
        )
        run_btn.pack(pady=10)
        
        return tab
    
    def create_cobrand_tab(self, notebook):
        """Create the LOS Cobrand tab"""
        tab = ttk.Frame(notebook)
        
        # Description
        desc_frame = ttk.Frame(tab)
        desc_frame.pack(fill=tk.X, pady=5)
        
        desc_label = ttk.Label(
            desc_frame,
            text="LOS Cobrand Automation - Cobrand card process",
            wraplength=700
        )
        desc_label.pack()
        
        # Configuration options
        config_frame = ttk.LabelFrame(tab, text="Configuration", padding=10)
        config_frame.pack(fill=tk.X, pady=5, padx=5)
        
        # Browser selection
        browser_frame = ttk.Frame(config_frame)
        browser_frame.pack(fill=tk.X, pady=5)
        
        browser_label = ttk.Label(browser_frame, text="Browser:")
        browser_label.pack(side=tk.LEFT)
        
        self.browser_cobrand_var = tk.StringVar(value="edge")
        browser_combo = ttk.Combobox(
            browser_frame,
            textvariable=self.browser_cobrand_var,
            values=["edge", "chrome"],
            state="readonly",
            width=10
        )
        browser_combo.pack(side=tk.LEFT, padx=5)
        
        # Data file selection
        data_frame = ttk.Frame(config_frame)
        data_frame.pack(fill=tk.X, pady=5)
        
        data_label = ttk.Label(data_frame, text="Data File:")
        data_label.pack(side=tk.LEFT)
        
        self.data_file_cobrand_var = tk.StringVar(value="Data/LOSData.xlsx")
        data_entry = ttk.Entry(data_frame, textvariable=self.data_file_cobrand_var, width=50)
        data_entry.pack(side=tk.LEFT, padx=5)
        
        data_browse_btn = ttk.Button(
            data_frame,
            text="Browse",
            command=lambda: self.browse_data_file(var=self.data_file_cobrand_var)
        )
        data_browse_btn.pack(side=tk.LEFT)
        
        # Run button
        btn_frame = ttk.Frame(tab)
        btn_frame.pack(fill=tk.X, pady=10)
        
        run_btn = ttk.Button(
            btn_frame,
            text="Run LOS Cobrand Automation",
            command=lambda: self.run_automation("src.scripts.los_cobrand"),
            style="Accent.TButton"
        )
        run_btn.pack(pady=10)
        
        return tab

    def create_recontest_tab(self, notebook):
        """Create the LOS Recontest tab"""
        tab = ttk.Frame(notebook)
        
        # Description
        desc_frame = ttk.Frame(tab)
        desc_frame.pack(fill=tk.X, pady=5)
        
        desc_label = ttk.Label(
            desc_frame,
            text="LOS Recontest Automation - Recontest process",
            wraplength=700
        )
        desc_label.pack()
        
        # Configuration options
        config_frame = ttk.LabelFrame(tab, text="Configuration", padding=10)
        config_frame.pack(fill=tk.X, pady=5, padx=5)
        
        # Browser selection
        browser_frame = ttk.Frame(config_frame)
        browser_frame.pack(fill=tk.X, pady=5)
        
        browser_label = ttk.Label(browser_frame, text="Browser:")
        browser_label.pack(side=tk.LEFT)
        
        self.browser_recontest_var = tk.StringVar(value="edge")
        browser_combo = ttk.Combobox(
            browser_frame,
            textvariable=self.browser_recontest_var,
            values=["edge", "chrome"],
            state="readonly",
            width=10
        )
        browser_combo.pack(side=tk.LEFT, padx=5)
        
        # Data file selection
        data_frame = ttk.Frame(config_frame)
        data_frame.pack(fill=tk.X, pady=5)
        
        data_label = ttk.Label(data_frame, text="Data File:")
        data_label.pack(side=tk.LEFT)
        
        self.data_file_recontest_var = tk.StringVar(value="Data/LOSData.xlsx")
        data_entry = ttk.Entry(data_frame, textvariable=self.data_file_recontest_var, width=50)
        data_entry.pack(side=tk.LEFT, padx=5)
        
        data_browse_btn = ttk.Button(
            data_frame,
            text="Browse",
            command=lambda: self.browse_data_file(var=self.data_file_recontest_var)
        )
        data_browse_btn.pack(side=tk.LEFT)
        
        # Run button
        btn_frame = ttk.Frame(tab)
        btn_frame.pack(fill=tk.X, pady=10)
        
        run_btn = ttk.Button(
            btn_frame,
            text="Run LOS Recontest Automation",
            command=lambda: self.run_automation("src.scripts.los_recontest"),
            style="Accent.TButton"
        )
        run_btn.pack(pady=10)
        
        return tab
    
    def create_settings_tab(self, notebook):
        """Create the Settings tab"""
        tab = ttk.Frame(notebook)
        
        # Settings content
        settings_frame = ttk.LabelFrame(tab, text="Application Settings", padding=10)
        settings_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Theme selection
        theme_frame = ttk.Frame(settings_frame)
        theme_frame.pack(fill=tk.X, pady=5)
        
        theme_label = ttk.Label(theme_frame, text="Theme:")
        theme_label.pack(side=tk.LEFT)
        
        self.theme_var = tk.StringVar(value="default")
        theme_combo = ttk.Combobox(
            theme_frame,
            textvariable=self.theme_var,
            values=["default", "light", "dark"],
            state="readonly",
            width=15
        )
        theme_combo.pack(side=tk.LEFT, padx=5)
        
        # Log level
        log_frame = ttk.Frame(settings_frame)
        log_frame.pack(fill=tk.X, pady=5)
        
        log_label = ttk.Label(log_frame, text="Log Level:")
        log_label.pack(side=tk.LEFT)
        
        self.log_level_var = tk.StringVar(value="info")
        log_combo = ttk.Combobox(
            log_frame,
            textvariable=self.log_level_var,
            values=["debug", "info", "warning", "error"],
            state="readonly",
            width=15
        )
        log_combo.pack(side=tk.LEFT, padx=5)
        
        # Screenshot directory
        screenshot_frame = ttk.Frame(settings_frame)
        screenshot_frame.pack(fill=tk.X, pady=5)
        
        screenshot_label = ttk.Label(screenshot_frame, text="Screenshot Directory:")
        screenshot_label.pack(side=tk.LEFT)
        
        self.screenshot_dir_var = tk.StringVar(value="Data/screenshoot")
        screenshot_entry = ttk.Entry(
            screenshot_frame,
            textvariable=self.screenshot_dir_var,
            width=40
        )
        screenshot_entry.pack(side=tk.LEFT, padx=5)
        
        screenshot_browse_btn = ttk.Button(
            screenshot_frame,
            text="Browse",
            command=self.browse_screenshot_dir
        )
        screenshot_browse_btn.pack(side=tk.LEFT)
        
        # Save settings button
        save_btn = ttk.Button(
            settings_frame,
            text="Save Settings",
            command=self.save_settings,
            style="Accent.TButton"
        )
        save_btn.pack(pady=10)

        # Sync Drivers button
        sync_frame = ttk.Frame(settings_frame)
        sync_frame.pack(fill=tk.X, pady=10)
        
        sync_btn = ttk.Button(
            sync_frame,
            text="Sync WebDrivers (Edge & Chrome)",
            command=self.manual_sync_drivers
        )
        sync_btn.pack(pady=5)
        
        return tab
    
    def manual_sync_drivers(self):
        """Manually sync both Edge and Chrome drivers"""
        self.log_message("Starting manual WebDriver sync...")
        self.update_status("Syncing drivers...")
        
        def sync_thread():
            results = []
            for b_type in ["edge", "chrome"]:
                self.log_message(f"Checking {b_type} driver...")
                success, msg = sync_drivers(b_type)
                results.append((b_type, success, msg))
                self.log_message(msg)
            
            self.update_status("Sync complete")
            summary = "\n".join([f"{r[0].capitalize()}: {r[2]}" for r in results])
            messagebox.showinfo("Sync Result", f"WebDriver Sync Detail:\n\n{summary}")

        threading.Thread(target=sync_thread, daemon=True).start()
    
    def create_status_bar(self):
        """Create the status bar"""
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(
            self.main_frame,
            textvariable=self.status_var,
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        status_bar.pack(fill=tk.X, side=tk.BOTTOM)
    
    def create_log_area(self):
        """Create the log area"""
        log_frame = ttk.LabelFrame(self.main_frame, text="Log", padding=5)
        log_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Log text widget
        self.log_text = tk.Text(
            log_frame,
            height=10,
            wrap=tk.WORD,
            state=tk.DISABLED
        )
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(
            self.log_text,
            command=self.log_text.yview
        )
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_text.config(yscrollcommand=scrollbar.set)
        
        # Clear log button
        clear_btn = ttk.Button(
            log_frame,
            text="Clear Log",
            command=self.clear_log,
            width=10
        )
        clear_btn.pack(side=tk.RIGHT, padx=5, pady=2)
    
    def browse_data_file(self, var=None):
        """Browse for data file"""
        if var is None:
            var = self.data_file_var
        
        file_path = filedialog.askopenfilename(
            title="Select Data File",
            filetypes=[("Excel Files", "*.xlsx"), ("All Files", "*.*")]
        )
        
        if file_path:
            var.set(file_path)
    
    def browse_screenshot_dir(self):
        """Browse for screenshot directory"""
        dir_path = filedialog.askdirectory(title="Select Screenshot Directory")
        
        if dir_path:
            self.screenshot_dir_var.set(dir_path)
    
    def save_settings(self):
        """Save application settings"""
        try:
            browser = self.browser_var.get()
            config.set("browser", browser)
            # You can add more settings here like data_file, screenshot_dir, etc.
            config.set("data_file", self.data_file_var.get())
            config.set("screenshot_dir", self.screenshot_dir_var.get())
            config.set("log_level", self.log_level_var.get())
            config.save_config()
            self.log_message(f"Settings saved: Browser={browser}, Log Level={self.log_level_var.get()}")
            messagebox.showinfo("Settings", "Settings saved successfully")
        except Exception as e:
            self.log_message(f"Error saving settings: {str(e)}")
            messagebox.showerror("Error", f"Failed to save settings: {str(e)}")
    
    def clear_log(self):
        """Clear the log area"""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state=tk.DISABLED)
    
    def log_message(self, message):
        """Add a message to the log area"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, log_entry)
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
    
    def update_status(self, message):
        """Update the status bar"""
        self.status_var.set(message)
        self.root.update()
    
    def run_automation(self, script_name):
        """Run the selected automation script"""
        if self.running_process and self.running_process.poll() is None:
            messagebox.showwarning(
                "Warning",
                "An automation process is already running. Please wait for it to complete."
            )
            return
        
        # Confirm before running
        if not messagebox.askyesno(
            "Confirm",
            f"Are you sure you want to run {script_name}?"
        ):
            return
        
        try:
            # Determine which browser is selected for this script
            browser_type = "edge" # default
            if script_name == "src.scripts.main_los":
                browser_type = self.browser_var.get()
            elif script_name == "src.scripts.supplement_los":
                browser_type = self.browser_supp_var.get()
            elif script_name == "src.scripts.addon_los":
                browser_type = self.browser_addon_var.get()
            elif script_name == "src.scripts.addon_supp_los":
                browser_type = self.browser_addon_supp_var.get()
            elif script_name == "src.scripts.los_cobrand":
                browser_type = self.browser_cobrand_var.get()
            elif script_name == "src.scripts.los_recontest":
                browser_type = self.browser_recontest_var.get()
            # Pass the log level from config or default to 'info'
            log_level = config.get("log_level", "info")
            script_args = []

            # Sync driver before running
            self.log_message(f"Verifying {browser_type} driver compatibility...")
            self.update_status(f"Syncing {browser_type} driver...")
            
            success, msg = sync_drivers(browser_type)
            self.log_message(msg)
            
            if not success:
                if not messagebox.askyesno("Driver Warning", f"{msg}\n\nDo you want to try running anyway?"):
                    self.update_status("Aborted")
                    return

            # Start the automation in a separate thread
            self.stop_event.clear()
            automation_thread = threading.Thread(
                target=self.run_script_thread,
                args=(script_name, browser_type, log_level, script_args),
                daemon=True
            )
            automation_thread.start()
            
            self.log_message(f"Started {script_name}")
            self.update_status(f"Running {script_name}...")
            
        except Exception as e:
            self.log_message(f"Error starting {script_name}: {str(e)}")
            self.update_status("Error")
            messagebox.showerror("Error", f"Failed to start automation: {str(e)}")
    
    def run_script_thread(self, script_name, browser_type, log_level, script_args=[]):
        try:
            from queue import Queue, Empty
            
            # Run the script module from root
            root_dir = config.root_dir
            
            # Run the script with browser and log-level arguments
            # Set PYTHONUNBUFFERED to ensure real-time output streaming
            env = os.environ.copy()
            env["PYTHONUNBUFFERED"] = "1"
            
            cmd = [sys.executable, "-m", script_name, "--browser", browser_type, "--log-level", log_level]
            if script_args:
                cmd.extend(script_args)
                
            self.running_process = subprocess.Popen(
                cmd,
                cwd=root_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                universal_newlines=True,
                env=env
            )
            
            # Queue for collecting output from threads
            output_queue = Queue()
            
            def read_output(pipe, prefix=""):
                """Read lines from pipe and put them in queue"""
                try:
                    for line in iter(pipe.readline, ''):
                        if line:
                            output_queue.put((prefix, line.strip()))
                except:
                    pass
            
            # Start threads to read stdout and stderr
            stdout_thread = threading.Thread(target=read_output, args=(self.running_process.stdout, ""))
            stderr_thread = threading.Thread(target=read_output, args=(self.running_process.stderr, "ERROR: "))
            stdout_thread.daemon = True
            stderr_thread.daemon = True
            stdout_thread.start()
            stderr_thread.start()
            
            # Monitor the process output
            while True:
                if self.stop_event.is_set():
                    self.running_process.terminate()
                    self.log_message(f"Stopped {script_name}")
                    self.update_status("Stopped")
                    break
                
                # Process any queued output
                try:
                    while True:
                        prefix, line = output_queue.get_nowait()
                        self.log_message(f"{prefix}{line}")
                except Empty:
                    pass
                
                # Check if process has finished
                return_code = self.running_process.poll()
                if return_code is not None:
                    # Wait briefly for remaining output
                    time.sleep(0.5)
                    try:
                        while True:
                            prefix, line = output_queue.get_nowait()
                            self.log_message(f"{prefix}{line}")
                    except Empty:
                        pass
                    
                    if return_code == 0:
                        self.log_message(f"{script_name} completed successfully")
                        self.update_status("Completed")
                    else:
                        self.log_message(f"{script_name} failed with return code {return_code}")
                        self.update_status("Failed")
                    break
                
                # Small delay
                time.sleep(0.1)
                
        except Exception as e:
            self.log_message(f"Error running {script_name}: {str(e)}")
            self.update_status("Error")
        finally:
            self.running_process = None
    
    def stop_automation(self):
        """Stop the running automation"""
        if self.running_process and self.running_process.poll() is None:
            self.stop_event.set()
            self.log_message("Stopping automation...")
            self.update_status("Stopping...")
        else:
            messagebox.showinfo("Info", "No automation process is currently running")

if __name__ == "__main__":
    root = tk.Tk()
    
    # Apply styling
    style = ttk.Style(root)
    style.configure('TFrame', background='#f0f0f0')
    style.configure('TLabel', background='#f0f0f0')
    style.configure('TButton', padding=5)
    style.configure('Accent.TButton', foreground='black', background='#4a7abc')
    
    app = LOSAutomationGUI(root)
    root.mainloop()