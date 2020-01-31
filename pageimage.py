import word2image
import argparse
import json
from docx import Document
import cv2
import numpy as np

parser = argparse.ArgumentParser(description='Output page for docx page')
parser.add_argument('document_path', type=str, nargs=1)
args = parser.parse_args()

CHARS_PER_LINE = 54
document = Document('test.docx')
with open('hashes.json') as f:
    hashes = json.load(f)



line_parser = word2image.Parser(hashes)
leftover = '' # denotes text that doesn't fit in a line an must be printed in the next line
lines = [] # list that stores image of each line
for para in document.paragraphs:
    text = leftover + para.text
    image, leftover = line_parser.lineimage_constrained(text, CHARS_PER_LINE)
    lines.append(image)
while leftover != '':
    text = leftover
    image, leftover = line_parser.lineimage_constrained(text, CHARS_PER_LINE)
    lines.append(image)
page = lines[0]
for i in range(1, len(lines)):
    page = np.vstack((page, lines[i]))
line_parser.show('window', page)