import requests

delete_id = input("What is the id of the product you want to delete? \n")
try: 
    id = int(delete_id)
except:
    delete_id = None
    print(f'Nothing for you!')

endpoint = f"http://localhost:8000/api/products/{delete_id}/delete/"

get_response = requests.delete(endpoint)
print(get_response.status_code, get_response.status_code==204)