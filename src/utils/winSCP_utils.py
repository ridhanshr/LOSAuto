import pyautogui
import os
import time

def automate_winSCP(pathWinSCP, noAplikasi, host, username, password):
    app_path = f"{str(pathWinSCP)}"
    os.startfile(app_path)
    time.sleep(3)

    pyautogui.typewrite('new')
    pyautogui.press('esc')

    for _ in range(4):
        pyautogui.hotkey('tab')
    pyautogui.typewrite(host)
    
    for _ in range(2):
        pyautogui.hotkey('tab')
    pyautogui.typewrite(username)

    pyautogui.hotkey('tab')
    pyautogui.typewrite(password)

    for _ in range(3):
        pyautogui.hotkey('tab')
    pyautogui.hotkey('enter')
    time.sleep(10)

    pyautogui.hotkey('ctrl', 'o')
    pyautogui.typewrite('/home/administrator/git-repo/LOS/los_automation_engine/')
    time.sleep(3)
    pyautogui.hotkey('enter')
    time.sleep(3)

    pyautogui.hotkey('ctrl', 'alt', 'f')
    time.sleep(1)
    pyautogui.typewrite('*manualQueue*')
    time.sleep(1)
    pyautogui.hotkey('enter')
    time.sleep(1)
    pyautogui.hotkey('ctrl', 'r')
    time.sleep(3)

    for _ in range(4):
        pyautogui.press('down')
    pyautogui.press('f4')
    time.sleep(8)
    pyautogui.hotkey('ctrl', 'r')
    time.sleep(3)
    pyautogui.hotkey('ctrl', 'f')
    time.sleep(1)
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.typewrite('KNP')
    pyautogui.hotkey('enter')
    time.sleep(1)

    pyautogui.press('esc')
    time.sleep(1)
    pyautogui.press('left')
    pyautogui.hotkey('ctrl', 'del')
    time.sleep(1)
    #pyautogui.hotkey('backspace')
    pyautogui.typewrite(noAplikasi)
    time.sleep(1)

    pyautogui.press('esc')
    pyautogui.hotkey('enter')
    time.sleep(3)
    
    pyautogui.hotkey('alt', 'f4')
    time.sleep(5)
    pyautogui.hotkey('enter')

# Contoh penggunaan
# path = 'C:/Program Files (x86)/WinSCP/WinSCP.exe'
# noAplikasi = 'KNP2024112500001'
# host = '172.24.141.33'
# username = 'administrator'
# password = 'c@rdl1nk'

# automate_winSCP(path, noAplikasi, host, username, password)