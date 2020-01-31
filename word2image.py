import argparse
import json
import cv2
import random
import numpy as np

counter = 1 #Used to decide which image of letter will be used. Goes from 1 to 5

parser = argparse.ArgumentParser(description='Output image for word')
parser.add_argument('word', type=str, nargs=1)
args = parser.parse_args()

with open('hashes.json') as f:
    hashes = json.load(f)

word = args.word[0]
letter = word[0]
key = letter + str(counter) + '.jpg'
finalImage = np.array(hashes[key], dtype = np.uint8)

for i in range(1, len(word)):
    counter = 1 + (counter + 1)%5
    letter = word[i]
    key = letter + str(counter) + '.jpg'
    finalImage = np.hstack((finalImage, np.array(hashes[key], dtype = np.uint8)))

cv2.imshow(args.word[0], finalImage)
cv2.waitKey()