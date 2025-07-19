import requests

endpoint = "http://localhost:8000/api/products/2/update"

data = {
    "title": "Hello sharply",
    "price": 0.00
}

get_response = requests.put(endpoint, json=data)
print(get_response.json())