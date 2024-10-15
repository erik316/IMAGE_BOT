import requests
import json
from time import sleep
import io
import base64
from PIL import Image

class TextToImage:
    def __init__(self, url:str, api_key:str, secret_key:str):
        self.URL = url
        self.AUTH_HEADERS = {
            'X-Key': f'Key {api_key}',
            'X-Secret': f'Secret {secret_key}',
        }

    def get_model(self):
        response = requests.get(self.URL + 'key/api/v1/models', headers=self.AUTH_HEADERS)
        data = response.json()
        return data[0]['id']
    
    def generate(self, prompt, model, images=1, width=256, height=256):
        params = {
            "type": "GENERATE",
            "numImages": images,
            "width": width,
            "style": "UHD",
            "height": height,
            "generateParams": {
                "query": f"{prompt}"
            }
        }
        data = {
            'model_id': (None, model),
            'params': (None, json.dumps(params), 'application/json')
        }
        response = requests.post(self.URL + 'key/api/v1/text2image/run', headers=self.AUTH_HEADERS, files=data)
        data = response.json()
        return data['uuid']
        
    def check_generation(self, request_id, attempts=10, delay=10):
        while attempts > 0:
            response = requests.get(self.URL + 'key/api/v1/text2image/status/' + request_id, headers=self.AUTH_HEADERS)
            data = response.json()
            if data['status'] == 'DONE':
                return data['images']

            attempts -= 1
            sleep(delay)

# url = 'https://api-key.fusionbrain.ai/'
# api_key = "926CACA9575182184FA33FA922CFBEC6"
# secret_key = "2615F5EEA5F06DFC133836530CBF7A44"

# api = TextToImage(url,api_key, secret_key)
# model = api.get_model()
# id = api.generate("", model)
# img = api.check_generation(id)
# print(img)

def base64_to_jpg(base_64, output_path):
    image_data = base64.b64decode(base_64)
    image = Image.open(io.BytesIO(image_data))
    image = image.convert('RGB')
    image.save(output_path, 'JPEG')




