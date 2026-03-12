"""
Configuration module for LOS Automation
Handles application settings and configuration
"""

import json
import os
import sys
from typing import Dict, Any, Optional

class LOSConfig:
    def __init__(self):
        # Get project root (where the executable or main script resides)
        if getattr(sys, 'frozen', False):
            self.root_dir = os.path.dirname(sys.executable)
        else:
            # 2 levels up from src/config.py
            self.root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            
        self.config_file = os.path.join(self.root_dir, "config.json")
        self.default_config = {
            "browser": "edge",
            "data_file": "Data/LOSData.xlsx",
            "screenshot_dir": "Data/screenshoot",
            "log_level": "info",
            "theme": "default",
            "timeout": 30,
            "headless": False,
            "window_size": "1920,1080",
            "credentials": {
                "username": "cc_dam",
                "password": ""
            }
        }
        
        self.config = self.default_config.copy()
        self.load_config()
    
    def load_config(self) -> None:
        """Load configuration from file"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    loaded_config = json.load(f)
                    # Update default config with loaded values
                    self.config.update(loaded_config)
                    # Ensure all default keys are present
                    for key, value in self.default_config.items():
                        if key not in self.config:
                            self.config[key] = value
        except Exception as e:
            print(f"Error loading config: {e}")
            self.config = self.default_config.copy()
    
    def save_config(self) -> None:
        """Save configuration to file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=4)
        except Exception as e:
            print(f"Error saving config: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value"""
        return self.config.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """Set configuration value"""
        self.config[key] = value
    
    def get_credentials(self) -> Dict[str, str]:
        """Get credentials"""
        return self.config.get("credentials", {})
    
    def set_credentials(self, username: str, password: str) -> None:
        """Set credentials"""
        self.config["credentials"] = {"username": username, "password": password}

# Global configuration instance
config = LOSConfig()