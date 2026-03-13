import sys
import argparse
import os
from src.utils.driver_manager import sync_drivers

def main():
    parser = argparse.ArgumentParser(description='Sync WebDrivers with installed browsers.')
    parser.add_argument('--browser', type=str, help='Specific browser to sync (chrome/edge). If omitted, both will be synced.')
    args = parser.parse_args()

    drivers_dir = "drivers"
    
    browsers = [args.browser] if args.browser else ["chrome", "edge"]
    
    print(f"=== WebDriver Sync Started ===")
    
    all_success = True
    for browser in browsers:
        print(f"Checking {browser.capitalize()}...")
        success, message = sync_drivers(browser, drivers_dir)
        if success:
            print(f"[SUCCESS] {message}")
        else:
            print(f"[FAILED] {message}")
            all_success = False
            
    print(f"=== Sync Process Finished ===")
    
    if not all_success:
        sys.exit(1)
    sys.exit(0)

if __name__ == "__main__":
    main()
