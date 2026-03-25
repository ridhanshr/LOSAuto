import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from src.config import config

def setup_webdriver(browser_type="edge", fast_mode=False):
    """Setup webdriver based on configuration"""
    # Use relative paths for drivers as they are in the project root
    if browser_type.lower() == "chrome":
        chrome_path = os.path.abspath(os.path.join(os.getcwd(), 'drivers', 'chromedriver.exe'))
        service = Service(executable_path=chrome_path)
        chrome_options = ChromeOptions()
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-software-rasterizer")
        chrome_options.add_argument("--remote-allow-origins=*")
        
        # Fast mode: headless and more optimizations
        if fast_mode or config.get("headless", False):
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            
        driver = webdriver.Chrome(service=service, options=chrome_options)
    else:  # Default to Edge
        edge_path = os.path.abspath(os.path.join(os.getcwd(), 'drivers', 'msedgedriver.exe'))
        service = Service(executable_path=edge_path)
        edge_options = EdgeOptions()
        edge_options.add_argument("--log-level=1")
        edge_options.add_argument("--remote-allow-origins=*")
        
        # Fast mode
        if fast_mode or config.get("headless", False):
            edge_options.add_argument("--headless")
            
        driver = webdriver.Edge(service=service, options=edge_options)
    
    driver.maximize_window()
    return driver

def save_screenshot(driver, filename, screenshot_dir=None):
    """Save screenshot to configured directory"""
    if screenshot_dir is None:
        screenshot_dir = config.get("screenshot_dir", "Data/screenshoot")
    
    # Ensure directory exists
    if not os.path.isabs(screenshot_dir):
        screenshot_dir = os.path.abspath(os.path.join(os.getcwd(), screenshot_dir))
        
    os.makedirs(screenshot_dir, exist_ok=True)
    
    # Save screenshot
    screenshot_path = os.path.join(screenshot_dir, filename)
    driver.save_screenshot(screenshot_path)
    # print(f"Screenshot saved: {screenshot_path}")
