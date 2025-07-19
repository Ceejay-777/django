import requests

delete_id = input("What is the id of the product you want to delete? \n")
try: 
    id = int(delete_id)
except:
    print(f'Nothing for you!')

endpoint = "http://localhost:8000/api/products/10"

get_response = requests.delete(endpoint)
print(get_response.json())