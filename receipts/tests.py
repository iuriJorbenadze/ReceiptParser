import os

import requests
import json

def test_receipt_processing():
    try:
        # Configuration
        TEST_IMAGE_URL = "https://ocr.space/Content/Images/receipt-ocr-original.webp"
        API_ENDPOINT = "http://localhost:8000/api/receipts/upload/"
        TEMP_IMAGE_PATH = "test_receipt.webp"

        # Download and process
        print("Downloading test image...")
        image_response = requests.get(TEST_IMAGE_URL)
        image_response.raise_for_status()

        with open(TEMP_IMAGE_PATH, "wb") as f:
            f.write(image_response.content)

        print("\nSending to API...")
        with open(TEMP_IMAGE_PATH, "rb") as image_file:
            response = requests.post(API_ENDPOINT, files={"image": image_file})

        # Raw JSON response (copy-paste friendly)
        print("\n=== RAW JSON RESPONSE ===")
        print(response.text)

        # Beautified version
        parsed = response.json()
        print("\n=== BEAUTIFIED PROCESSED DATA ===")
        print(json.dumps(parsed["processed_data"], indent=2, ensure_ascii=False))

        # Human-friendly raw text
        print("\n=== HUMAN-READABLE RAW TEXT ===")
        print(parsed["processed_data"]["raw_text"].replace("\\n", "\n"))

    except Exception as e:
        print(f"\nError: {str(e)}")
    finally:
        if os.path.exists(TEMP_IMAGE_PATH):
            os.remove(TEMP_IMAGE_PATH)

if __name__ == "__main__":
    test_receipt_processing()