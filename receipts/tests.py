# from django.test import TestCase
#
# # Create your tests here.
#
# import requests
# url = 'http://localhost:8000/api/receipts/upload/'
# files = {'image': open('Untitled.png', 'rb')}
# response = requests.post(url, files=files)
# print(response.json())


import requests

# Simple one-time test
def test_upload():
    try:
        files = {'image': open('test_receipt.png', 'rb')}  # Replace with your file
        response = requests.post('http://localhost:8000/api/receipts/upload/', files=files)

        print("Status Code:", response.status_code)
        print("Response JSON:")
        print(response.json())

    except FileNotFoundError:
        print("Error: test_receipt.jpg not found in current directory")
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to server. Is it running?")
    except Exception as e:
        print("Unexpected error:", str(e))

# Run the test
test_upload()