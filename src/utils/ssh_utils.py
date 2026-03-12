import paramiko
import time
import re
import logging
from src.utils.db_utils import check_appflag

logger = logging.getLogger("LOSAuto.SSH")

def run_ssh_command(host, username, password, command, wait_time=5):
    """Executes a command via SSH in the background."""
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(host, username=username, password=password)
        stdin, stdout, stderr = ssh.exec_command(command)
        # We don't wait for completion if it's a long running process like Node.js
        # but we might want to read a bit of output to ensure it started.
        time.sleep(wait_time)
        return ssh, stdin, stdout, stderr
    except Exception as e:
        logger.error(f"SSH Error: {e}")
        return None, None, None, None

def update_manual_queue_remote(host, username, password, no_aplikasi):
    """Updates the manualQueue.js file on the remote server using SFTP."""
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(host, username=username, password=password)
        sftp = ssh.open_sftp()
        
        file_path = "/home/administrator/git-repo/LOS/los_automation_engine/manualQueue.js"
        
        # Read the file
        with sftp.open(file_path, "r") as f:
            content = f.read().decode('utf-8')
        
        # Replace KNP... with the new no_aplikasi
        # Looking for a pattern like KNP followed by digits
        # Based on winSCP_utils, it looks for 'KNP' and replaces it.
        # We'll use a regex to replace the existing KNP value or any placeholder.
        new_content = re.sub(r'KNP\d+', no_aplikasi, content)
        
        # If no specific KNP value found, just replace 'KNP' literal if that was the placeholder
        if new_content == content:
            new_content = content.replace('KNP', no_aplikasi)

        # Write the file back
        with sftp.open(file_path, "w") as f:
            f.write(new_content)
            
        sftp.close()
        ssh.close()
        logger.info(f"manualQueue.js updated with {no_aplikasi}")
        return True
    except Exception as e:
        logger.error(f"SFTP Error: {e}")
        return False

def background_scoring_ssh(noAplikasi, host, username, password):
    """Performs background scoring via SSH with retries."""
    pattern = re.compile(r"'(.*?)'")
    
    # We will loop until success or a terminal state is reached
    while True:
        # 1. Update the manualQueue.js file via SFTP
        logger.info(f"Updating manualQueue.js for {noAplikasi}...")
        if not update_manual_queue_remote(host, username, password, noAplikasi):
            logger.info("Failed to update manualQueue.js, retrying in 10s...")
            time.sleep(10)
            continue

        # 2. Run the node command via SSH
        logger.info("Starting scoring command via SSH...")
        command = 'cd /home/administrator/git-repo/LOS/los_automation_engine && node -r dotenv/config manualQueue.js'
        ssh, stdin, stdout, stderr = run_ssh_command(host, username, password, command)
        
        if not ssh:
            logger.info("SSH connection failed, retrying in 10s...")
            time.sleep(10)
            continue

        try:
            # 3. Poll for appFlag 5.7.0
            logger.info("Polling for flag 5.7.0...")
            start_poll = time.time()
            poll_duration = 60 # Poll for 1 minute before retrying the command
            
            while time.time() - start_poll < poll_duration:
                appFlag_raw = check_appflag(str(noAplikasi))
                match = pattern.search(str(appFlag_raw))
                appFlag = match.group(1) if match else None
                logger.info(f"Current appFlag: {appFlag}")

                if appFlag == "5.7.0":
                    logger.info("Scoring successful (Flag 5.7.0)")
                    ssh.close()
                    return True
                
                # Check for terminal/reject flags
                if appFlag in ["9.2.1", "9.2.3"]:
                    logger.info(f"Application rejected/terminated with flag {appFlag}")
                    ssh.close()
                    return False
                
                time.sleep(10)
            
            logger.info("Timeout reached for this attempt. Retrying scoring process...")
            
        finally:
            ssh.close()
            # Safety break to avoid extremely tight loops if something goes wrong
            time.sleep(5)