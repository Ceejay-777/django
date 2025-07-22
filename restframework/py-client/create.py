import requests

headers = {'Authorization': 'Bearer 403d85b9b59578e28e70de39eb2150f8dc7dad66'}

endpoint = "http://localhost:8000/api/products/"

data = {
    "title": "This field is done",
    "price": "32.99"
}

get_response = requests.post(endpoint, json=data, headers=headers)
print(get_response.json()) 