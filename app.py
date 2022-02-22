from flask import Flask, render_template, request, redirect
import shutil
import multiprocessing
import requests
import json
import os
import time
from PIL import Image


private_secret_key = "AIzaSyDEN_6QPOSdEES8AjkfUuWg3QShB0bvKA8"
url = "https://vision.googleapis.com/v1/images:annotate"
querystring = {"key": private_secret_key}
headers = {'Content-Type': "application/json",}


app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
path = "/Users/alex/Downloads/"
to_del = map(lambda x: os.path.join(path, x.name),
             filter(lambda x: "terly_photo" in x.name, os.scandir("/Users/alex/Downloads/")))
for i in to_del:
    os.remove(i)


def encode_text(recognised, text):
    with open("encoded_text.terly", 'w') as f:
        f.write(str(int(recognised)) + text)


def decode_text():
    with open("encoded_text.terly", 'r') as f:
        ans = f.read().strip()
        return bool(int(ans[0])), ans[1:]


encode_text(False, 'Ошибка распознавания, пожалуйста, повторите позднее')


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
    try:
        json.dump(payload, open("request.json", 'w'))
        img = Image.open("static/styles/images/terly_photo.png")
        x, y = img.size
        response = requests.request("POST", url, data=json.dumps(payload), headers=headers, params=querystring)
        parsed_text = []
        for i in response.json()["responses"][0]["textAnnotations"][1:]:
            coords = i["boundingPoly"]["vertices"]
            # croping imgs
        text = response.json()["responses"][0]["fullTextAnnotation"]["text"].replace('\n', ' ')
    except:
        text = "Нестабильное подключение к интернету, пожалуйста, переключитесь на другую сеть"
    encode_text(True, text)


@app.route('/')
def main_page():
    if decode_text()[0]:
        ans = decode_text()[1]
        encode_text(False, 'Ошибка распознавания, пожалуйста, повторите позднее')
        return render_template("index.html", text=ans)
    time.sleep(2)
    try:
        files = list(map(lambda x: os.path.join(path, x.name),
                         filter(lambda x: "terly_photo" in x.name, os.scandir("/Users/alex/Downloads/"))))
        if files:
            file = files[0]
        shutil.copyfile(file, "/Users/alex/Documents/pythonProject/Terly/static/styles/images/terly_photo.png")
    except:
        return redirect("http://127.0.0.1:5000/loading")
    # jpg problem
    p = multiprocessing.Process(target=image_request)
    p.start()
    return redirect("http://127.0.0.1:5000/loading")



@app.route('/send_img')
def send_img():
    img = request.args.get('img_url')
    print(img)


@app.route('/loading')
def loading_page():
    return render_template("cude.html")


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000)
