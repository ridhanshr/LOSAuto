import sys
import os
import tkinter as tk
from tkinter import ttk
import importlib
import multiprocessing

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def run_gui():
    root = tk.Tk()
    
    # Apply styling
    style = ttk.Style(root)
    style.configure('TFrame', background='#f0f0f0')
    style.configure('TLabel', background='#f0f0f0')
    style.configure('TButton', padding=5)
    style.configure('Accent.TButton', foreground='black', background='#4a7abc')
    
    from src.gui.app import LOSAutomationGUI
    app = LOSAutomationGUI(root)
    root.mainloop()

if __name__ == "__main__":
    # Support for multiprocessing when frozen
    multiprocessing.freeze_support()
    
    # Check if we are running a script module
    if len(sys.argv) > 1 and sys.argv[1] == "-m":
        if len(sys.argv) < 3:
            print("Usage: program.exe -m module_name [args...]")
            sys.exit(1)
        
        module_name = sys.argv[2]
        # Remove -m and module_name from argv
        sys.argv = [sys.argv[0]] + sys.argv[3:]
        
        try:
            # Import the module
            module = importlib.import_module(module_name)
            
            # Execute run() or main() if they exist
            if hasattr(module, 'run'):
                module.run()
            elif hasattr(module, 'main'):
                module.main()
            else:
                print(f"Error: Module {module_name} has no run() or main() function")
                sys.exit(1)
                
        except Exception as e:
            print(f"Error executing module {module_name}: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)
    else:
        # Normal GUI startup
        run_gui()
