import paramiko

hostname = "172.24.141.33"
username = "administrator"
password = "c@rdl1nk"

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname, username=username, password=password)

sftp = ssh.open_sftp()
file_path = "/home/administrator/git-repo/LOS/los_automation_engine"

# Baca file dari server
with sftp.open(file_path, "r") as f:
    content = f.read()

print(content)
# Replace
# content = content.replace("console.log('Hello');", "console.log('Hello World!');")

# Simpan balik
# with sftp.open(file_path, "w") as f:
#     f.write(content)

sftp.close()
ssh.close()
print("✅ File JS di server berhasil diedit")
