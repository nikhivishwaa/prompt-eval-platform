import requests
import io
import json

MODEL_URL = 'http://localhost:5000/api'

async def make_prediction(file, mimetype=None):
    try:
        print(file)
        r = requests.post(
            MODEL_URL,
            # files={'image': ('image.jpg', io.BytesIO(image_data), mimetype)}
            files={'image': file}
        )
        if r.status_code == 200:
            result = json.loads(r.text)
            print(f"Model Called : {result}")
            return result
    except Exception as e:
        print(f"Failed to call to external service: {e}")
        return None    