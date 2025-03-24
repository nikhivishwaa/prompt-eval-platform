import io
from PIL import Image
import numpy as np
# from tensorflow.keras.models import load_model
import joblib as jb
import cv2
from django.http import HttpResponse
from collections import Counter

MODEL_V1 = jb.load('Models/saved_model/v1/tooth_disease_cnn.h5')
MODEL_V2 = jb.load('Models/saved_model/v2/tooth-classifier.joblib.h5')
MODEL_V3 = jb.load('Models/saved_model/v3/tooth-classifier.joblib.h5')

LABELS = ['Cavity', 'Fillings', 'Impacted Tooth', 'Implant', 'Normal']

async def ready_file(file):
    x_ray = file.read()
    image = Image.open(io.BytesIO(x_ray))

    image_np = np.array(image)

    print(image_np.shape)
    return image_np

async def predict_by_model1(image):
    image_rgb = cv2.cvtColor(image, cv2.COLOR_RGBA2RGB)
    image_resized = cv2.resize(image_rgb, (70, 70))
    # print('image shape:', image_resized.shape)
    prediction = MODEL_V1.predict(np.array([image_resized]))

    label = LABELS[np.argmax(prediction)]
    confidence = round(np.max(prediction) * 100, 2)

    result = {
        'title':f"Predicted:{label}\nConfidence: {confidence} %",
        "confidence": confidence,
        "predicted":label,
        "metadata": {
            "version": 'v1.0.0',
            "model" : "v1",
            "input_shape": "70 x 70"
        }
     }

    return result

async def predict_by_model2(image):
    image_rgb = cv2.cvtColor(image, cv2.COLOR_RGBA2RGB)
    image_resized = cv2.resize(image_rgb, (128, 128))

    img_gray = cv2.cvtColor(image_resized, cv2.COLOR_RGB2GRAY)
    img_hq = cv2.equalizeHist(img_gray)
    img_color = cv2.cvtColor(img_hq, cv2.COLOR_GRAY2RGB)
    img_blur = cv2.GaussianBlur(img_color, (3, 3), 0)
    # print('image shape:', image_resized.shape)
    prediction = MODEL_V2.predict(np.array([img_blur]))

    label = LABELS[np.argmax(prediction)]
    confidence = round(np.max(prediction) * 100, 2)

    result = {
        'title':f"Predicted:{label}\nConfidence: {confidence} %",
        "confidence": confidence,
        "predicted":label,
        "metadata": {
            "version": 'v1.1.0',
            "model" : "v2",
            "input_shape": "128 x 128"
        }
     }

    return result

async def predict_by_model3(image):
    image_rgb = cv2.cvtColor(image, cv2.COLOR_RGBA2RGB)
    image_resized = cv2.resize(image_rgb, (224, 224))

    img_gray = cv2.cvtColor(image_resized, cv2.COLOR_RGB2GRAY)
    img_hq = cv2.equalizeHist(img_gray)
    img_color = cv2.cvtColor(img_hq, cv2.COLOR_GRAY2RGB)
    img_blur = cv2.GaussianBlur(img_color, (3, 3), 0)
    # print('image shape:', image_resized.shape)
    prediction = MODEL_V3.predict(np.array([img_blur]))

    label = LABELS[np.argmax(prediction)]
    confidence = round(np.max(prediction) * 100, 2)

    result = {
        'title':f"Predicted:{label}\nConfidence: {confidence} %",
        "confidence": confidence,
        "predicted":label,
        "metadata": {
            "version": 'v1.2.0',
            "model" : "v3",
            "input_shape": "224 x 224"
        }
     }

    return result

async def make_prediction(image):
    image_np = await ready_file(image)
    pred = []
    pred[0] = await predict_by_model1(image_np)
    pred[1] = await predict_by_model2(image_np)
    pred[2] = await predict_by_model3(image_np)

        
    # Create a Counter object to get mejority vote

    predictions = [pred[0]['predicted'], pred[1]['predicted'], pred[2]['predicted']]
    counter = Counter([prediction])

    vote = counter.most_common(1)[0][0]

    highest_confidence = 0.0
    idx = None
    for i, result in enumerate(pred):
        if result['predicted'] == vote:
            if highest_confidence < result['confidence']:
                idx = i
        
    if idx is not None:
        max_voted_prediction = pred[idx]
        max_voted_prediction['majority_vote'] = True
        return max_voted_prediction
    else:
        prediction = pred[0]
        prediction['majority_vote'] = False
        return prediction


    # if pred[0]['predicted'] == pred[1]['predicted']:
    #     pred[1]['majority_vote'] = True
    #     return pred[1]
    
    # else:
    #     # if int(float(pred[0]['confidence'])) >= int(float(pred[1]['confidence'])):
    #     pred[1]['majority_vote'] = False
    #     return pred[0]
        
    #     # else:
    #     #     return pred[1]

