import re

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

        # Add this cleaning step
        cleaned_text = (
            parsed_text
            .replace('\t', ' ')          # Replace tabs with spaces
            .replace('\r', '')           # Remove carriage returns
            .replace('\\', '\\\\')       # Escape backslashes
            .replace('\n', '\\n')        # Escape newlines
            .replace('"', '\\"')         # Escape double quotes
        )


        # Basic structure extraction (customize based on your needs)
        return {
            "raw_text": cleaned_text,
            "items": extract_items(parsed_text),
            "total": extract_total(parsed_text),
            "merchant": extract_merchant(parsed_text)
        }

    except Exception as e:
        logger.error(f"OCR Processing failed: {str(e)}")
        raise

def extract_items(text):
    """Improved item extraction with price pairing"""
    items = []
    for line in text.split('\r\n'):
        # Skip non-item lines
        if any(keyword in line.lower() for keyword in ['subtotal', 'tax', 'total', 'coupon', 'change due']):
            continue

        # Find all potential prices in the line
        prices = re.findall(r'\b\d+\.\d{2}\b', line)
        if not prices:
            continue

        # Use last price in line as item price
        price = prices[-1]

        # Clean up line components
        parts = []
        for part in line.split('\t'):
            part = part.strip()
            # Remove product codes and flags
            if not any([
                re.match(r'^\d{10,}$', part),  # Long numeric codes
                part in ['X', 'F', 'I', 'N'],  # Single-letter flags
                re.match(r'^\d+\.\d{2}$', part) and part != price  # Other prices
            ]):
                parts.append(part)

        # Rebuild item string
        clean_line = ' '.join(parts)
        # Remove any remaining price markers except the last one
        clean_line = re.sub(r'\s\d+\.\d{2}(?!.*\d+\.\d{2})', '', clean_line)
        items.append(f"{clean_line} {price}")

    return items

def extract_total(text):
    """Simple total extraction (customize this)"""
    for line in reversed(text.split('\r\n')):
        if 'total' in line.lower():
            return float(''.join(c for c in line if c.isdigit() or c == '.'))
    return None

def extract_merchant(text):
    """Simple merchant extraction (customize this)"""
    return text.split('\r\n')[0].strip()