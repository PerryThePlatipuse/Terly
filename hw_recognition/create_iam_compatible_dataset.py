import os
import numpy as np
import cv2
import json


class DataProvider():
    "this class creates machine-written text for a word list. TODO: change getNext() to return your samples."

    def __init__(self):
        words = os.listdir("HKR/ann")
        self.wordList = []
        for i in words:
            with open(f"/Users/alex/Documents/pythonProject/Terly/hw_recognition/HKR/ann/{i}") as f:
                if all(map(lambda x: not x.isalpha() or 1040 <= ord(x) <= 1103, json.loads(f.read())["description"])):
                    self.wordList.append(i)
        self.idx = 0

    def hasNext(self):
        "are there still samples to process?"
        return self.idx < len(self.wordList)

    def getNext(self):
        "TODO: return a sample from your data as a tuple containing the text and the image"
        word = self.wordList[self.idx]
        img = cv2.imread(f"/Users/alex/Documents/pythonProject/Terly/hw_recognition/HKR/img/{word.split('.')[0]}.jpg",
                         cv2.IMREAD_GRAYSCALE)
        with open(f"/Users/alex/Documents/pythonProject/Terly/hw_recognition/HKR/ann/{word}") as f:
            word = json.loads(f.read())["description"]
        self.idx += 1
        return (word, img)


def createIAMCompatibleDataset(dataProvider):
    "this function converts the passed dataset to an IAM compatible dataset"

    # create files and directories
    f = open('words.txt', 'w+')
    if not os.path.exists('sub'):
        os.makedirs('sub')
    if not os.path.exists('sub/sub-sub'):
        os.makedirs('sub/sub-sub')

    # go through data and convert it to IAM format
    ctr = 0
    while dataProvider.hasNext():
        sample = dataProvider.getNext()

        # write img
        cv2.imwrite('sub/sub-sub/sub-sub-%d.png' % ctr, sample[1])

        # write filename, dummy-values and text
        line = 'sub-sub-%d' % ctr + ' X X X X X X X ' + sample[0] + '\n'
        f.write(line)

        ctr += 1


if __name__ == '__main__':
    dataProvider = DataProvider()
    createIAMCompatibleDataset(dataProvider)
