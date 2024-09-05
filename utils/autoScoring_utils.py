import re
import time
from utils.winSCP_utils import automate_winSCP
from utils.ssh_utils import automate_putty
from utils.db_utils import check_appflag

def automate_scoring(pathWinSCP, noAplikasiData, host, username, password):
    print("Proses Scoring Mulai")
    time.sleep(5)
    automate_winSCP(pathWinSCP, noAplikasiData, host, username, password)
    time.sleep(3)
    automate_putty(noAplikasiData, host, username, password)
    
    appFlag = check_appflag(str(noAplikasiData))
    pattern = re.compile(r"'(.*?)'")
    match = pattern.search(str(appFlag))
    
    if match:
        return match.group(1)
    else:
        return None
    