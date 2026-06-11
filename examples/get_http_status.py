import sys
import os
import json
from cryptography.hazmat.primitives.serialization import load_der_private_key
import epd_util

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: python3 get_http_status.py <ip_or_hostname>")
        sys.exit(1)

    target = sys.argv[1]
    api_url = f"http://{target}/api/control/request"
    if not target.replace('.', '').isdigit() and not target.endswith('.local'):
        api_url = f"http://smartwiz-art-{target}.local/api/control/request"

    private_key_path = f"{os.getcwd()}/app_private.der"
    if not os.path.exists(private_key_path):
        print("app_private.der not found. Run device_register.py first.")
        sys.exit(1)

    with open(private_key_path, "rb") as f:
        app_private_key = load_der_private_key(f.read(), password=None)

    request_id = "1"
    request_utc = epd_util.get_current_request_utc()
    
    response = epd_util.send_get_device_status_request(api_url, request_id, request_utc, app_private_key)
    if response:
        print(json.dumps(response.json(), indent=4))
    else:
        print("Failed to get status.")
