import time
import json
import requests
from zapv2 import ZAPv2
from urllib.parse import urljoin

# Configure the ZAP API Key
api_key = 'e914nhk6jpbq52bu29psqdkg2o'
zap = ZAPv2(apikey=api_key)

# User target URL
target = input("Enter the target URL (default: http://localhost:8000): ").strip()
if not target:
    target = 'http://localhost:8000'

context_name = "DynamicContext"
print(f"Configuring ZAP for target: {target}")

# Step 1: Create or update the context
print(f"Setting up context: {context_name}")
context_id = zap.context.new_context(context_name)  # Create a new context
zap.context.include_in_context(context_name, f'{target}.*')  # Add URL pattern to the context
print(f"Context '{context_name}' created with target URL included.")

# Optimize ZAP settings for faster scanning
print("Configuring ZAP for optimized scanning...")
zap.ascan.set_option_thread_per_host(20)  # Increase threads per host
zap.ascan.set_option_max_scan_duration_in_mins(10)  # Increase scan duration
zap.ascan.set_option_delay_in_ms(0)  # No delay between requests
zap.spider.set_option_max_depth(5)  # Increase spider depth to 5
zap.spider.set_option_thread_count(20)  # Increase the number of spider threads

# Step 2: Open the target URL
zap.urlopen(target)
time.sleep(2)

# Step 3: Spider the target (with increased parallelism and depth)
print("Starting spidering...")
spider_id = zap.spider.scan(target)

# Wait for the spidering to complete
while int(zap.spider.status(spider_id)) < 100:
    print(f"Spider progress: {zap.spider.status(spider_id)}%")
    time.sleep(1)
print("Spidering completed.")

# Step 4: Passive scan delay (shortened)
print("Allowing passive scanner a brief time...")
time.sleep(2)

# Step 5: Start active scan (with more parallelism)
print("Starting active scan...")
scan_id = zap.ascan.scan(target)

# Wait for the active scan to complete
while int(zap.ascan.status(scan_id)) < 100:
    print(f"Active scan progress: {zap.ascan.status(scan_id)}%")
    time.sleep(2)
print("Active scanning completed.")

# Step 6: Define a set of predefined payloads (optional, if you want more control over specific tests)
payloads = [
    "../../../../etc/passwd",  # Linux
    "/../../../../etc/shadow",  # Linux
    "../etc/hosts",  # Common path
    "../../windows/system32/drivers/etc/hosts",  # Windows
    "/../../../etc/passwd",  # Another common path
    "..%2F..%2F..%2F..%2Fetc%2Fpasswd",  # URL-encoded traversal
]

print(f"[INFO] Using {len(payloads)} predefined payloads.")

# Step 7: Retrieve all ZAP alerts (no filtering)
print("Retrieving scan results...")
alerts = zap.core.alerts()
print(f"Total alerts retrieved: {len(alerts)}")

# Step 8: Initialize an empty list to hold success findings
successful_findings = []

# Step 9: Add manual payload validation for path traversal (or other types you are checking for)
for payload in payloads:
    test_url = urljoin(target, payload)
    try:
        response = requests.get(test_url, timeout=5)

        # Check for successful HTTP status (200 OK) and analyze content for signs of vulnerability
        if response.status_code == 200:
            if any(keyword in response.text for keyword in ['root:', 'bin/bash', 'shadow:', '[global]']):
                print(f"[SUCCESS] Path Traversal vulnerability detected with payload: {payload}")
                successful_findings.append({
                    "payload": payload,
                    "status": response.status_code,
                    "snippet": response.text[:100]  # Store the first 100 characters of the response
                })
            else:
                print(f"[INFO] Payload tested but no vulnerability detected: {payload}")
        else:
            print(f"[INFO] No vulnerability detected with payload {payload}, status code: {response.status_code}")

    except requests.RequestException as e:
        print(f"[ERROR] Failed to test payload {payload}: {e}")

# Step 10: Combine ZAP alerts and successful findings
all_vulnerabilities = alerts + successful_findings

# Step 11: Write results to a JSON file
output_file = 'results.json'
with open(output_file, 'w') as json_file:
    json.dump(all_vulnerabilities, json_file, indent=4)

print(f"Scan results saved to {output_file}")
