import os
import re
import subprocess
import requests
import zipfile
import io
import winreg
import time
from typing import Optional, Tuple

def get_edge_version() -> Optional[str]:
    """Get Microsoft Edge browser version from Windows Registry."""
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Edge\BLBeacon")
        version, _ = winreg.QueryValueEx(key, "version")
        return version
    except Exception:
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Microsoft\Edge\BLBeacon")
            version, _ = winreg.QueryValueEx(key, "version")
            return version
        except Exception:
            return None

def get_chrome_version() -> Optional[str]:
    """Get Google Chrome browser version from Windows Registry."""
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Google\Chrome\BLBeacon")
        version, _ = winreg.QueryValueEx(key, "version")
        return version
    except Exception:
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Google\Chrome\BLBeacon")
            version, _ = winreg.QueryValueEx(key, "version")
            return version
        except Exception:
            return None

def get_driver_version(driver_path: str) -> Optional[str]:
    """Get the version of the driver executable."""
    if not os.path.exists(driver_path):
        return None
    try:
        result = subprocess.run([driver_path, "--version"], capture_output=True, text=True)
        # Output is usually like 'ChromeDriver 132.0.6834.159 (...)' or 'msedgedriver 132.0.2906.0 (...)'
        match = re.search(r'(\d+\.\d+\.\d+\.\d+)', result.stdout)
        if match:
            return match.group(1)
        return None
    except Exception:
        return None

def update_edge_driver(target_dir: str, version: str) -> bool:
    """Download and update Microsoft Edge Driver."""
    try:
        # Check if file is locked and try to kill existing driver processes
        driver_path = os.path.join(target_dir, "msedgedriver.exe")
        if os.path.exists(driver_path):
            try:
                subprocess.run(['taskkill', '/F', '/IM', 'msedgedriver.exe', '/T'], capture_output=True)
            except Exception:
                pass
            time.sleep(1)

        print(f"Updating Edge Driver to version {version}...")
        
        # Try exact version first
        urls = [
            f"https://msedgedriver.microsoft.com/{version}/edgedriver_win64.zip",
            f"https://msedgedriver.azureedge.net/{version}/edgedriver_win64.zip",
            # Fallback to major version latest if exact fails
            f"https://msedgedriver.azureedge.net/LATEST_RELEASE_{version.split('.')[0]}_WINDOWS"
        ]

        success = False
        for url in urls:
            if "LATEST_RELEASE" in url:
                try:
                    v_resp = requests.get(url)
                    if v_resp.status_code == 200:
                        actual_v = v_resp.text.strip().replace('\x00', '')
                        url = f"https://msedgedriver.microsoft.com/{actual_v}/edgedriver_win64.zip"
                    else:
                        continue
                except:
                    continue

            response = requests.get(url)
            if response.status_code == 200:
                with zipfile.ZipFile(io.BytesIO(response.content)) as zip_ref:
                    for file in zip_ref.namelist():
                        if file.endswith("msedgedriver.exe"):
                            filename = os.path.basename(file)
                            with open(os.path.join(target_dir, filename), "wb") as f:
                                f.write(zip_ref.read(file))
                            success = True
                            break
            if success:
                break
        
        return success
    except Exception as e:
        print(f"Error updating Edge Driver: {e}")
        return False

def update_chrome_driver(target_dir: str, version: str) -> bool:
    """Download and update Chrome Driver."""
    try:
        # Kill existing driver processes
        driver_path = os.path.join(target_dir, "chromedriver.exe")
        if os.path.exists(driver_path):
            try:
                subprocess.run(['taskkill', '/F', '/IM', 'chromedriver.exe', '/T'], capture_output=True)
            except Exception:
                pass
            time.sleep(1)

        print(f"Updating Chrome Driver for version {version}...")
        # Since Chrome 115, they use "Chrome for Testing" availability dashboard
        major_version = version.split('.')[0]
        v_url = f"https://googlechromelabs.github.io/chrome-for-testing/LATEST_RELEASE_{major_version}"
        v_response = requests.get(v_url)
        
        if v_response.status_code != 200:
            # Fallback to known good versions json
            v_url = "https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json"
            v_response = requests.get(v_url)
            data = v_response.json()
            url = None
            for channel in data['channels'].values():
                for download in channel['downloads'].get('chromedriver', []):
                    if download['platform'] == 'win64':
                        url = download['url']
                        break
                if url: break
        else:
            actual_version = v_response.text.strip()
            url = f"https://storage.googleapis.com/chrome-for-testing-public/{actual_version}/win64/chromedriver-win64.zip"

        if not url:
            return False

        response = requests.get(url)
        if response.status_code != 200:
            return False

        with zipfile.ZipFile(io.BytesIO(response.content)) as zip_ref:
            for file in zip_ref.namelist():
                if file.endswith("chromedriver.exe"):
                    filename = os.path.basename(file)
                    with open(os.path.join(target_dir, filename), "wb") as f:
                        f.write(zip_ref.read(file))
                    return True
        return False
    except Exception as e:
        print(f"Error updating Chrome Driver: {e}")
        return False

def sync_drivers(browser_type: str, drivers_dir: str = "drivers") -> Tuple[bool, str]:
    """Check and update the specified driver if necessary."""
    if not os.path.exists(drivers_dir):
        os.makedirs(drivers_dir)

    if browser_type.lower() == "edge":
        browser_version = get_edge_version()
        if not browser_version:
            return False, "Microsoft Edge not detected."
        
        driver_path = os.path.join(drivers_dir, "msedgedriver.exe")
        driver_version = get_driver_version(driver_path)
        
        # Check if major versions match (or if driver is missing)
        if not driver_version or driver_version.split('.')[0] != browser_version.split('.')[0]:
            success = update_edge_driver(drivers_dir, browser_version)
            if success:
                return True, f"Edge Driver updated to {browser_version}."
            return False, "Failed to update Edge Driver."
        return True, "Edge Driver is up to date."

    elif browser_type.lower() == "chrome":
        browser_version = get_chrome_version()
        if not browser_version:
            return False, "Google Chrome not detected."
        
        driver_path = os.path.join(drivers_dir, "chromedriver.exe")
        driver_version = get_driver_version(driver_path)
        
        if not driver_version or driver_version.split('.')[0] != browser_version.split('.')[0]:
            success = update_chrome_driver(drivers_dir, browser_version)
            if success:
                return True, f"Chrome Driver updated to {browser_version}."
            return False, "Failed to update Chrome Driver."
        return True, "Chrome Driver is up to date."

    return False, f"Unsupported browser type: {browser_type}"
