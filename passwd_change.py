import csv
import paramiko

def change_password(ip, port, user, old_pw, new_pw):
    try:
        port = int(port)  # 포트는 정수로
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, port=port, username=user, password=old_pw, timeout=5)

        # passwd 명령은 인터랙티브하지만, echo로 대체 가능 (Red Hat, Ubuntu 등에서)
        cmd = f'echo -e "{old_pw}\n{new_pw}\n{new_pw}" | passwd'
        stdin, stdout, stderr = ssh.exec_command(cmd)
        result = stdout.read().decode() + stderr.read().decode()

        print(f"[{ip}:{port}] ✅ 완료:\n{result}")
        ssh.close()
    except Exception as e:
        print(f"[{ip}:{port}] ❌ 실패: {e}")

# CSV 읽기 및 처리
with open('servers.csv') as file:
    reader = csv.DictReader(file)
    for row in reader:
        change_password(row['ip'], row['port'], row['username'], row['old_password'], row['new_password'])

