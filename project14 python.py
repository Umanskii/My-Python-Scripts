import subprocess
import requests

# Define the IP addresses and thresholds
IP_addresses = ["ec2-user@54.167.247.196", "ec2-user@44.203.76.147"]
cpu_threshold = 80
mem_threshold = 80
disk_threshold = 90
my_webhook = "https://hooks.slack.com/services/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"

# Function to run remote commands via SSH and return the result
def run_remote_command(node, command):
    try:
        result = subprocess.check_output(["ssh", node, command], universal_newlines=True)
        return result.strip()
    except subprocess.CalledProcessError as e:
        return str(e)

# Function to send a Slack message
def send_slack_message(node, text):
    payload = {
        "text": f"{node}: {text}",
        "channel": "D05FH0P5NTV"
    }
    headers = {'Content-type': 'application/json'}
    response = requests.post(my_webhook, json=payload, headers=headers)
    if response.status_code != 200:
        print(f"Failed to send Slack message to {node}")

# Iterate through the IP addresses
for node in IP_addresses:
    print(f"\n#################### Checking Memory, Disk space, and CPU on {node} ####################")
    
    mem_result = run_remote_command(node, "mem_utilization")
    cpu_result = run_remote_command(node, "cpu_utilization")
    disk_result = run_remote_command(node, "disk_utilization")
    
    mem_result = int(mem_result) if mem_result.isdigit() else -1
    cpu_result = int(cpu_result) if cpu_result.isdigit() else -1
    disk_result = int(disk_result) if disk_result.isdigit() else -1
    
    if mem_result < mem_threshold:
        send_slack_message(node, f"{mem_result} % Memory is OK")
    else:
        send_slack_message(node, "Memory needs attention")
    
    if cpu_result < cpu_threshold:
        send_slack_message(node, f"{cpu_result} % CPU is Fine")
    else:
        send_slack_message(node, "CPU needs attention")
    
    if disk_result < disk_threshold:
        send_slack_message(node, f"{disk_result} % Disk is OK")
    else:
        send_slack_message(node, "Disk needs attention")
