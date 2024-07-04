import requests
from app import *

img_path = open(os.path.join(CURDIR, "image/cap1.jpg"), "rb")

url = "http://127.0.0.1:8000/upload"
file = {"file": img_path}
resp = requests.post(url=url, files=file)
print(resp.json())

resp = requests.get(url="http://127.0.0.1:8000/get_image")
print(resp.json())
