import requests
import json

#
BASE_URL = "http://localhost:8000"

response = requests.post(f"{BASE_URL}/length", json={"source_unit": 'm', "target_unit": 'mi', "amount": "234.23"})
print("Length response status: " + str(response.status_code))
if response.status_code == 200:
    result = response.json()
    print(f"Response: {result}")
elif response.status_code == 404:
    json_data = json.loads(response.text)
    error = json_data["detail"]
    print(f"Error: {error}")

print("")
response = requests.post(f"{BASE_URL}/weight", json={"source_unit": 'oz', "target_unit": 'kg', "amount": "2342398.234"})
print("Weight response status: " + str(response.status_code))
if response.status_code == 200:
    result = response.json()
    print(f"Response: {result}")
elif response.status_code == 404:
    json_data = json.loads(response.text)
    error = json_data["detail"]
    print(f"Error: {error}")

print("")
response = requests.post(f"{BASE_URL}/currency", json={"source_unit": "USD", "target_unit": "EUR", "amount": "153.24"})
print("Currency response status: " + str(response.status_code))
if response.status_code == 200:
    result = response.json()
    print(f"Response: {result}")
elif response.status_code == 404: 
    json_data = json.loads(response.text)
    error = json_data["detail"]
    print(f"Error: {error}")
