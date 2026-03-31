import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("ETSY_API_KEY")

def test_connection():
    url = "https://openapi.etsy.com/v3/application/openapi-ping"
    headers = {
        "x-api-key": API_KEY
    }
    response = requests.get(url, headers=headers)
    print("Status Code:", response.status_code)
    print("Response:", response.json())
test_connection()
