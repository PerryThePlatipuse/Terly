import requests
import json
import os
import time
import numpy as np
import cv2
from private_key import private_secret_key


url = "https://vision.googleapis.com/v1/images:annotate"

querystring = {"key": private_secret_key}
headers = {
    'Content-Type': "application/json",
}


def encode_text(recognised, text):
    with open("encoded_text.terly", 'w') as f:
        f.write(str(int(recognised)) + text)


def decode_text():
    with open("encoded_text.terly", 'r') as f:
        ans = f.read().strip()
        return bool(int(ans[0])), ans[1:]


encode_text(False, 'Ошибка распознавания, пожалуйста, повторите позднее')


def order_points(pts):
    # initialzie a list of coordinates that will be ordered
    # such that the first entry in the list is the top-left,
    # the second entry is the top-right, the third is the
    # bottom-right, and the fourth is the bottom-left
    rect = np.zeros((4, 2), dtype="float32")
    # the top-left point will have the smallest sum, whereas
    # the bottom-right point will have the largest sum
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]
    # now, compute the difference between the points, the
    # top-right point will have the smallest difference,
    # whereas the bottom-left will have the largest difference
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]
    # return the ordered coordinates
    return rect


def four_point_transform(image, pts):
    # obtain a consistent order of the points and unpack them
    # individually
    rect = order_points(pts)
    (tl, tr, br, bl) = rect

    # compute the width of the new image, which will be the
    # maximum distance between bottom-right and bottom-left
    # x-coordiates or the top-right and top-left x-coordinates
    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))

    # compute the height of the new image, which will be the
    # maximum distance between the top-right and bottom-right
    # y-coordinates or the top-left and bottom-left y-coordinates
    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))

    # now that we have the dimensions of the new image, construct
    # the set of destination points to obtain a "birds eye view",
    # (i.e. top-down view) of the image, again specifying points
    # in the top-left, top-right, bottom-right, and bottom-left
    # order
    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype="float32")

    # compute the perspective transform matrix and then apply it
    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))

    # return the warped image
    return warped


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
        response = requests.request("POST", url, data=json.dumps(payload), headers=headers, params=querystring)
        with open("database/how_much.txt", 'r') as f:
            count = int(f.read().strip())
        with open("database/annotations.json", 'r') as f:
            dct = json.load(f)
        with open("database/annotations.json", 'w') as f:
            for i in response.json()["responses"][0]["textAnnotations"][1:]:
                count += 1
                coords = i["boundingPoly"]["vertices"]
                description = i["description"]
                dct[count] = description
                pct = four_point_transform(cv2.imread("static/styles/images/terly_photo.png"),
                                           np.array([[coords[0]["x"], coords[0]["y"]],
                                                     [coords[1]["x"], coords[1]["y"]],
                                                     [coords[2]["x"], coords[2]["y"]],
                                                     [coords[3]["x"], coords[3]["y"]]]))
                cv2.imwrite(f"database/db/file{count}.png", pct)
            json.dump(dct, f, ensure_ascii=False)
            text = response.json()["responses"][0]["fullTextAnnotation"]["text"].replace('\n', ' ')
        with open("database/how_much.txt", 'w') as f:
            f.write(str(count))
    except:
        text = "Нестабильное подключение к интернету, пожалуйста, переключитесь на другую сеть"
    encode_text(True, text)


image_request()
