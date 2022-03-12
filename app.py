from flask import Flask, render_template, request, redirect
import shutil
import multiprocessing
import os
import time
from GoogleVision import image_request, encode_text, decode_text


app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
path = "/Users/alex/Downloads/"
to_del = map(lambda x: os.path.join(path, x.name),
             filter(lambda x: "terly_photo" in x.name, os.scandir("/Users/alex/Downloads/")))
for i in to_del:
    os.remove(i)


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
