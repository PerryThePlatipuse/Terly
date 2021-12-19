import os
from google.cloud import vision
import io
from PIL import Image, ImageDraw
import cv2
import numpy as np
from pprint import pprint
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\detecting handwriting-21f8330c8722.json"


# image1 = cv2.imread('photo.png')
# kernel_sharp = [[1, 4, 6, 4, 1],
#                 [4, 16, 24, 16, 4],
#                 [6, 24, -476, 24, 6],
#                 [4, 16, 24, 16, 4],
#                 [1, 4, 6, 4, 1]]
# kernel_sharp = np.array(kernel_sharp).astype(np.float64)
# kernel_sharp *= (-1 / 156)
# img1 = cv2.filter2D(src=image1, ddepth=-1, kernel=kernel_sharp)
# cv2.imwrite("photo.png", img1)


def detect_document(path):
    """Detects document features in an image."""
    from google.cloud import vision
    import io
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.document_text_detection(image=image, image_context={"language_hints": ["ru"]})
    blocks = []
    for page in response.full_text_annotation.pages:
        for block in page.blocks:
            paragr = []
            for paragraph in block.paragraphs:
                words = []
                for word in paragraph.words:
                    word_text = ''.join([
                        symbol.text for symbol in word.symbols
                    ])
                    words.append(word_text)
                paragr.append(' '.join(words))
            blocks.append(paragr)
    return blocks


pprint(detect_document("photo.png"))

# Ounogrfope - это
#
# ф, чем отличается меjon grouе от мезонит geneuuu: на дроблення клетка не получае nur. b-bа = te paciem
#
# 3. Какой этап эмбриогенезе есть у человека, но нет у животных? Морула
#
# Н. На каком этапе заканчивается