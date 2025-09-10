from flask import Flask, request
import subprocess, json, datetime

app = Flask(__name__)
LOG='/var/log/selfheal-webhook.log'

def log(msg):
    with open(LOG,'a') as f:
        f.write(f"{datetime.datetime.now().isoformat()} {msg}\n")

def run(cmd):
    log("Running: " + " ".join(cmd))
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        log(f"rc={out.returncode}\nstdout:\n{out.stdout}\nstderr:\n{out.stderr}")
    except Exception as e:
        log("Exception: " + str(e))

@app.route('/alerts', methods=['POST'])
def alerts():
    payload = request.get_json(force=True, silent=True) or {}
    log("Received: " + json.dumps(payload))
    for a in payload.get('alerts', []):
        name = a.get('labels', {}).get('alertname', '')
        status = a.get('status', '')
        log(f"Handling alert={name} status={status}")
        if status != 'firing':
            continue
        if name == 'NginxDown':
            run(['/usr/bin/ansible-playbook','-i','/opt/selfheal/playbooks/inventory.ini','/opt/selfheal/playbooks/heal_nginx.yml','-b'])
        elif name == 'HighCPU':
            run(['/usr/bin/ansible-playbook','-i','/opt/selfheal/playbooks/inventory.ini','/opt/selfheal/playbooks/mitigate_cpu.yml','-b'])
    return 'ok', 200

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001)

