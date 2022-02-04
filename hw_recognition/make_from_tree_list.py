import os
import json
import tqdm
import numpy as np
import cv2
from deslant_img import deslant_img
for i in tqdm.tqdm(os.listdir("HKR/img")):
    img = cv2.imread(f"/Users/alex/Documents/pythonProject/Terly/hw_recognition/HKR/img/{i}", cv2.IMREAD_GRAYSCALE)
    res = deslant_img(img)
    cv2.imwrite(f"/Users/alex/Documents/pythonProject/Terly/hw_recognition/HKR/img/{i}", res.img)