import requests
import json
import os
from PIL import Image
import time

private_secret_key = "AIzaSyDEN_6QPOSdEES8AjkfUuWg3QShB0bvKA8"

url = "https://vision.googleapis.com/v1/images:annotate"

querystring = {"key": private_secret_key}
headers = {
    'Content-Type': "application/json",
}


def image_request():
    os.system("base64 -i 'static/styles/images/terly_photo.png' -o encoded_img.terly")
    time.sleep(0.5)
    with open("encoded_img.terly") as f:
        contet_ans = f.read().strip()
    payload = {
        "requests": [
            {
                "features": [
                    {
                        "maxResults": 50,
                        "model": "builtin/latest",
                        "type": "DOCUMENT_TEXT_DETECTION"
                    }
                ],
                "image": {
                    "content": str(contet_ans)
                },
                "imageContext": {
                    "cropHintsParams": {
                        "aspectRatios": [
                            0.8,
                            1,
                            1.2
                        ]
                    },
                    "languageHints": ["ru"]
                }
            }
        ]
    }
    json.dump(payload, open("request.json", 'w'))
    img = Image.open("static/styles/images/terly_photo.png")
    x, y = img.size
    response = requests.request("POST", url, data=json.dumps(payload), headers=headers, params=querystring)
    parsed_text = []
    for i in response.json()["responses"][0]["textAnnotations"][1:]:
        coords = i["boundingPoly"]["vertices"]
        # croping imgs
    return response.json()["responses"][0]["fullTextAnnotation"]["text"].replace('\n', ' ')
