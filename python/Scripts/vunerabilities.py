import time
import json
import requests
from zapv2 import ZAPv2
from urllib.parse import urljoin, urlencode

# Configure the ZAP API Key
api_key = 'e914nhk6jpbq52bu29psqdkg2o'
zap = ZAPv2(apikey=api_key)

# Prompt the user for the target URL
target = input("Enter the target URL (default: http://localhost:8000): ").strip()
if not target:
    target = 'http://localhost:8000'

print(f"Starting scan on target: {target}")

# Optimize ZAP settings for faster scanning
print("Configuring ZAP for optimized scanning...")
zap.ascan.set_option_thread_per_host(10)
zap.ascan.set_option_max_scan_duration_in_mins(10)
zap.ascan.set_option_delay_in_ms(0)
zap.spider.set_option_max_depth(5)
zap.spider.set_option_thread_count(10)

# Step 1: Open the target URL
zap.urlopen(target)
time.sleep(2)

# Step 2: Spider the target
print("Starting spidering...")
spider_id = zap.spider.scan(target)

# Wait for the spidering to complete
while int(zap.spider.status(spider_id)) < 100:
    print(f"Spider progress: {zap.spider.status(spider_id)}%")
    time.sleep(1)
print("Spidering completed.")

# Step 3: Passive scan delay
print("Allowing passive scanner some time...")
time.sleep(3)

# Step 4: Start active scan
print("Starting active scan...")
scan_id = zap.ascan.scan(target)

# Wait for the active scan to complete
while int(zap.ascan.status(scan_id)) < 100:
    print(f"Active scan progress: {zap.ascan.status(scan_id)}%")
    time.sleep(5)
print("Active scanning completed.")

# Step 5: Fetch payloads from PayloadsAllTheThings
def fetch_payloads_from_github(raw_url):
    """
    Fetch raw payloads from a GitHub file.
    """
    try:
        response = requests.get(raw_url)
        response.raise_for_status()
        return [line.strip() for line in response.text.splitlines() if line.strip() and not line.startswith("#")]
    except requests.RequestException as e:
        print(f"[ERROR] Failed to fetch payloads: {e}")
        return []

print("Fetching additional payloads from PayloadsAllTheThings...")
payload_url = "https://raw.githubusercontent.com/swisskyrepo/PayloadsAllTheThings/master/Traversal%20Directory/Path-Traversal.txt"
payloads = fetch_payloads_from_github(payload_url)
if payloads:
    print(f"[INFO] Loaded {len(payloads)} additional payloads.")
else:
    print("[WARN] No payloads loaded. Proceeding with default scan results.")

# Step 6: Retrieve and process ZAP alerts
print("Retrieving scan results...")
alerts = zap.core.alerts()
print(f"Total alerts retrieved: {len(alerts)}")

# Step 7: Add manual payload validation
validated_vulnerabilities = []
for payload in payloads:
    test_url = urljoin(target, payload)
    try:
        response = requests.get(test_url, timeout=5)
        if response.status_code == 200 and any(keyword in response.text for keyword in ['root:', 'bin/bash', 'shadow:', '[global]']):
            print(f"[SUCCESS] Path Traversal vulnerability detected with payload: {payload}")
            validated_vulnerabilities.append({
                "payload": payload,
                "status": response.status_code,
                "snippet": response.text[:100]
            })
        else:
            print(f"[INFO] Payload tested but no vulnerability detected: {payload}")
    except requests.RequestException as e:
        print(f"[ERROR] Failed to test payload {payload}: {e}")

# Step 8: Filter ZAP alerts based on CWE IDs or keywords
vulnerabilities = {
    '22',   # Path Traversal
    '79',   # Cross-Site Scripting (XSS)
    '95',   # Code Injection
    '338',  # Cryptographically Weak PRNG
    '601',  # Open Redirect
    '502',  # Deserialization of Untrusted Data
    '208',  # Observable Timing Discrepancy
    '23',   # Relative Path Traversal
    '943',  # Improper Neutralization in Data Query Logic
    '798',  # Hard-coded Credentials
    '606',  # Unchecked Input for Loop Condition
    '346',  # Origin Validation Error
    '185',  # Regular Expression with Non-Literal Value
}
filtered_alerts = [
    alert for alert in alerts
    if alert.get('cweid', '0') in vulnerabilities or
    any(keyword in alert.get('description', '').lower() for keyword in ['xss', 'sql injection', 'path traversal'])
]

# Combine filtered ZAP results with validated vulnerabilities
all_vulnerabilities = filtered_alerts + validated_vulnerabilities

# Step 9: Write results to a JSON file
output_file = 'results.json'
with open(output_file, 'w') as json_file:
    json.dump(all_vulnerabilities, json_file, indent=4)

print(f"Scan results saved to {output_file}")
