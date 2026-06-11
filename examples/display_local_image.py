#import pytest
import sys
import os
import epd_util
import json
from cryptography.hazmat.primitives.serialization import load_der_private_key
from cryptography.hazmat.primitives import serialization

def on_custom_data_receive(data):
    global response
    response = data.decode('utf-8')

if __name__ == "__main__":

    try:
        if len(sys.argv) < 3:
            print(f"Usage: python3 display_local_image.py <device_id_or_ip> <image_file.s6>")
            sys.exit(1)

        target = sys.argv[1]
        s6_image_file_path = sys.argv[2]
        art_sdk_root = os.getcwd()

        # 1. Load keys first
        private_key_path = f"{art_sdk_root}/app_private.der"
        if not os.path.exists(private_key_path):
            print("app_private.der not found. Please run device_register.py first.")
            sys.exit(-1)

        with open(private_key_path, "rb") as f:
            app_private_key = load_der_private_key(f.read(), password=None)

        epd_public_key_file_path = f"{art_sdk_root}/epd_public_key.der"
        if not os.path.exists(epd_public_key_file_path):
            print("epd_public_key.der not found. Please run device_register.py first.")
            sys.exit(-1)
            
        with open(epd_public_key_file_path, "rb") as f:
            epd_public_key_bin = f.read()

        # 2. Resolve api_url and device_id
        device_id = os.getenv("ART_DEVICE_ID")
        if target.replace('.', '').isdigit() or target.endswith('.local'):
            api_url = f"http://{target}/api/control/request"
            if "smartwiz-art-" in target:
                extracted_id = target.split("smartwiz-art-")[1].split(".")[0]
                if not device_id:
                    device_id = extracted_id
        else:
            if not device_id:
                device_id = target
            api_url = f"http://smartwiz-art-{target}.local/api/control/request"

        # 3. Fetch device_id if missing
        if not device_id or len(device_id) < 32:
            try:
                print(f"Fetching device status from {target} to get accurate device_id...")
                tmp_request_id = "0"
                tmp_request_utc = epd_util.get_current_request_utc()
                status_resp = epd_util.send_get_device_status_request(api_url, tmp_request_id, tmp_request_utc, app_private_key)
                if status_resp and status_resp.status_code == 200:
                    device_id = status_resp.json().get("device_id")
                    print(f"Retrieved device_id: {device_id}")
            except Exception as e:
                print(f"Warning: Could not fetch device_id, using fallback: {e}")

        if not device_id:
            device_id = "0" * 32

        # 4. Prepare IV and Encryption
        cbc_iv = device_id[-16:].encode('ascii')
        if len(cbc_iv) != 16:
            cbc_iv = cbc_iv.zfill(16)
            
        caption = "Test Image"
        orientation = 0
        x_offset = 0
        y_offset = 0
        width = 800
        height = 480
        
        epd_public_key = serialization.load_der_public_key(epd_public_key_bin)
        encrypted_image = epd_util.make_encrypted_image(0, s6_image_file_path, epd_public_key, cbc_iv, x_offset, y_offset, width, height, caption, orientation)

        # 5. Upload and Display
        request_id = "1"
        request_utc = epd_util.get_current_request_utc()
        
        print("Uploading image...")
        response = epd_util.send_image_upload_request(api_url, request_id, request_utc, app_private_key, encrypted_image)
        if response is None:
            print("Upload failed.")
            sys.exit(1)
            
        json_resp = response.json()
        if not json_resp.get("result"):
            print(f"Upload failed: {json_resp}")
            sys.exit(1)

        file = json_resp["file"]
        print(f"Image uploaded successfully. File: {file}")

        print("Requesting display update...")
        request_utc = epd_util.get_current_request_utc()
        user_name   = "smartwizart-cli-user"
        user_comment = "user image by smartwizart-cli"
        response = epd_util.send_display_request(api_url, request_id, request_utc, app_private_key, file, user_name, user_comment)
        if response:
            print(response.json())
            print("Success! The image will be updated shortly.")
        else:
            print("Display request failed.")
            
        sys.exit(0)
    except Exception as e:
        print(f"Display local image failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
