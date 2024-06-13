import requests
import json

BASE = "http://127.0.0.1:5000/"


response = requests.get(
    BASE + "users/account", {"login": json.dumps({"test": "hello"})}
)
# response = requests.post(BASE + "users/account", {"login": {"username": "123"}})
# response = requests.delete(BASE + "tests/1")
# response = requests.post(BASE + "tests/10", {"username": "frog", "password": "123"})
# print(response)
print(response.json())
