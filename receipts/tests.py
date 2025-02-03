from django.test import TestCase

# Create your tests here.

import requests
url = 'http://localhost:8000/api/receipts/upload/'
files = {'image': open('Untitled.png', 'rb')}
response = requests.post(url, files=files)
print(response.json())