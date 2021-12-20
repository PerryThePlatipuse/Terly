from flask import Flask, render_template

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

print("kal")
@app.route('/')
def hello_world():
    print("yes")# put application's code here
    return render_template("index.html")


if __name__ == '__main__':
    app.run()

