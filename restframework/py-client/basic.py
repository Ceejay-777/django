import requests

# endpoint = "https://httpbin.org/status/200"
# endpoint = "https://httpbin.org/anything"

endpoint = "http://localhost:8000/api/"

get_response = requests.post(endpoint, params={"abc": 123}, json={"id": "hello world two", "content": "watermelon"})
print(get_response.json())