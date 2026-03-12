import re
import time
from src.utils.ssh_utils import background_scoring_ssh
from src.utils.db_utils import check_appflag

import logging

logger = logging.getLogger("LOSAuto.AutoScoring")

def automate_scoring(pathWinSCP, noAplikasiData, host, username, password):
    """
    Performs background scoring via SSH to replace UI-based Putty/WinSCP.
    pathWinSCP is kept for backward compatibility but ignored in background mode.
    """
    time.sleep(3)
    # The new background logic handles both file update (SFTP) and command execution (SSH)
    success = background_scoring_ssh(noAplikasiData, host, username, password)
    
    if not success:
        logger.info("Background scoring failed.")
        return None

    # Get final appFlag
    appFlag_raw = check_appflag(str(noAplikasiData))
    pattern = re.compile(r"'(.*?)'")
    match = pattern.search(str(appFlag_raw))
    
    if match:
        return match.group(1)
    else:
        return None