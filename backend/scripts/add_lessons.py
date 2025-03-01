import requests

api_url = "http://127.0.0.1:8000/api/store-lessons"

response = requests.post(api_url)
print(response.json())  # Check if lessons were stored