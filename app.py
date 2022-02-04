from flask import Flask, render_template, request
import os, shutil
import time
from GoogleVision import detect_document

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

path = "/Users/alex/Downloads/"
to_del = map(lambda x: os.path.join(path, x.name),
             filter(lambda x: "terly_photo" in x.name, os.scandir("/Users/alex/Downloads/")))
for i in to_del:
    os.remove(i)


@app.route('/')
def main_page():
    # time.sleep(2)
    # text = detect_document("/Users/alex/Documents/pythonProject/Terly/static/styles/images/terly_photo.png")
    # time.sleep(5)
    # files = list(map(lambda x: os.path.join(path, x.name),
    #                  filter(lambda x: "terly_photo" in x.name, os.scandir("/Users/alex/Downloads/"))))
    # if files:
    #     file = files[0]
    # text = '\n'.join(detect_document("/Users/alex/Documents/pythonProject/Terly/static/styles/images/terly_photo.png"))
    text = "Стоит дней – период встречного правления Наполеона с конца марта 1815 г. по 6 июня 1815г. решение венского конгресса Наполеон урок человечества часть Saxony передавалась Герцогство Варшавская – Россия кроме территории отходивший костре не проси 14 сентября 1815г. Александром первым Франция первым Фридрихом-Вильгельмом третьим был подписан акт о создании священного Союза к чему вскоре присоединились почти все монархи Европе кроме турецкого султана он крестьянин и Англии."
    # shutil.copyfile(file, "/Users/alex/Documents/pythonProject/Terly/static/styles/images/terly_photo.png")
    return render_template("index.html", text=text)


@app.route('/send_img')
def send_img():
    img = request.args.get('img_url')
    print(img)


if __name__ == '__main__':
    app.run()
