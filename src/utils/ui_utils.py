import os
import shutil
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from src.config import config

def setup_webdriver(browser_type="edge"):
    """Setup webdriver based on configuration"""
    is_headless = config.get("headless", False)
    
    if browser_type.lower() == "chrome":
        chrome_path = r'drivers/chromedriver.exe'
        service = ChromeService(executable_path=chrome_path)
        chrome_options = ChromeOptions()
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-software-rasterizer")
        chrome_options.add_argument("--remote-allow-origins=*")
        chrome_options.add_argument("--incognito")
        if is_headless:
            chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(service=service, options=chrome_options)
    else:  # Default to Edge
        edge_path = r'drivers/msedgedriver.exe'
        service = EdgeService(executable_path=edge_path)
        edge_options = EdgeOptions()
        edge_options.add_argument("--log-level=1")
        edge_options.add_argument("--remote-allow-origins=*")
        if is_headless:
            edge_options.add_argument("--headless")
        driver = webdriver.Edge(service=service, options=edge_options)
    
    driver.maximize_window()
    return driver

def save_screenshot(driver, filename, screenshot_dir=None):
    """Save screenshot to configured directory"""
    if screenshot_dir is None:
        screenshot_dir = config.get("screenshot_dir", "Data/screenshoot")
    
    # Ensure directory exists
    os.makedirs(screenshot_dir, exist_ok=True)
    
    # Save screenshot
    screenshot_path = os.path.join(screenshot_dir, filename)
    driver.save_screenshot(screenshot_path)
    print(f"Screenshot saved: {screenshot_path}")

def move_screenshot(temp_filename, screenshot_dir=None):
    """Move a screenshot from current dir to screenshot dir"""
    if screenshot_dir is None:
        screenshot_dir = config.get("screenshot_dir", "Data/screenshoot")
    
    os.makedirs(screenshot_dir, exist_ok=True)
    dest_path = os.path.join(screenshot_dir, temp_filename)
    
    if os.path.exists(temp_filename):
        shutil.move(temp_filename, dest_path)
        print(f"Screenshot moved to: {dest_path}")
