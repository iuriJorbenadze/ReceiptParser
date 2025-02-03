import requests
import os
import logging

logger = logging.getLogger(__name__)

def process_receipt_image(image_path):
    """
    Process receipt image using OCR.space API
    Returns structured data in format:
    {
        "merchant": "Walmart",
        "total": 29.99,
        "items": ["Milk 2L", "Bread Whole Wheat"],
        "raw_text": "Full OCR text here..."
    }
    """
    api_key = os.getenv('OCR_SPACE_API_KEY')
    if not api_key:
        raise ValueError("OCR_SPACE_API_KEY environment variable not set")

    try:
        with open(image_path, 'rb') as f:
            response = requests.post(
                'https://api.ocr.space/parse/image',
                files={'file': f},
                data={
                    'apikey': api_key,
                    'language': 'eng',
                    'isTable': 'true',  # Enable receipt/table mode
                    'OCREngine': '2',    # Better for receipts
                    'isOverlayRequired': 'false'
                },
                timeout=30  # Increase timeout for large receipts
            )

        response.raise_for_status()
        result = response.json()

        if result.get('IsErroredOnProcessing', False):
            raise Exception(f"OCR Error: {result.get('ErrorMessage', 'Unknown error')}")

        parsed_text = result['ParsedResults'][0]['ParsedText']

        # Basic structure extraction (customize based on your needs)
        return {
            "raw_text": parsed_text,
            "items": extract_items(parsed_text),
            "total": extract_total(parsed_text),
            "merchant": extract_merchant(parsed_text)
        }

    except Exception as e:
        logger.error(f"OCR Processing failed: {str(e)}")
        raise

def extract_items(text):
    """Simple item extraction logic (customize this)"""
    return [line.strip() for line in text.split('\r\n') if '$' in line or '€' in line]

def extract_total(text):
    """Simple total extraction (customize this)"""
    for line in reversed(text.split('\r\n')):
        if 'total' in line.lower():
            return float(''.join(c for c in line if c.isdigit() or c == '.'))
    return None

def extract_merchant(text):
    """Simple merchant extraction (customize this)"""
    return text.split('\r\n')[0].strip()