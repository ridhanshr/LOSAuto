from pywinauto.application import Application
from utils.db_utils import check_appflag
from utils.winSCP_utils import automate_winSCP
import pyautogui
import time
import re

def automate_putty(noAplikasi, host, username, password):
    def run_putty(command):
        app = Application().start("putty.exe")
    
        pyautogui.typewrite(host)
        for _ in range(10):
            pyautogui.hotkey('tab')
        
        pyautogui.hotkey('enter')
        time.sleep(3)

        # Login
        pyautogui.typewrite(username)
        pyautogui.hotkey('enter')
        time.sleep(1)
        pyautogui.typewrite(password)
        pyautogui.hotkey('enter')
        time.sleep(1)

        # Menjalankan perintah
        pyautogui.typewrite('cd /home/administrator/git-repo/LOS/los_automation_engine')
        pyautogui.hotkey('enter')
        time.sleep(1)

        pyautogui.typewrite(command)
        pyautogui.hotkey('enter')
        time.sleep(3)

    command1 = 'node -r dotenv/config wrkScoring.js'
    command2 = 'node -r dotenv/config manualQueue.js'
    run_putty(command1)
    time.sleep(5)
    run_putty(command2)
    time.sleep(15)

    appFlag = None
    pattern = re.compile(r"'(.*?)'")
    
    while True:
        appFlag = check_appflag(str(noAplikasi))
        match = pattern.search(str(appFlag))
        if match:
            appFlag = match.group(1)
        print("appFlag ", appFlag)

        if appFlag in ["5.7.0"]:
            # Close applications if appFlag is 5.7.0
            for _ in range(2):
                pyautogui.hotkey('ctrl', 'c')
                time.sleep(2)
                pyautogui.hotkey('alt', 'f4')
                time.sleep(1)
                pyautogui.hotkey('enter')
                time.sleep(3)
            break

        # Perform actions to retry if appFlag is not yet 5.7.0
        automate_winSCP(r'C:/Program Files (x86)/WinSCP/WinSCP.exe', noAplikasi, host, username, password)
        time.sleep(5)
        pyautogui.hotkey('ctrl', 'c')
        time.sleep(1)
        pyautogui.hotkey('alt', 'tab')
        time.sleep(1)
        pyautogui.hotkey('ctrl', 'c')
        time.sleep(3)
        pyautogui.typewrite(command1)
        time.sleep(3)
        pyautogui.hotkey('enter')
        time.sleep(1)
        pyautogui.hotkey('alt', 'tab')
        time.sleep(5)
        pyautogui.typewrite(command2)
        time.sleep(3)
        pyautogui.hotkey('enter')
        
        time.sleep(15)

# # EXAMPLE  
# host = '172.24.141.33'
# username = 'administrator'
# password = 'c@rdl1nk'

# automate_putty(host, username, password)