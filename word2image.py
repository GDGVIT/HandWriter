import argparse
import json
import cv2
import random
import numpy as np



def main():
    # Used to decide which image of letter will be used. Goes from 1 to 5
    counter = 1 

    with open('hashes.json') as f:
        hashes = json.load(f)
    # JSON file contains dictionary where key is like A3.jpg and value is image array
    word = args.word[0]
    letter = word[0]
    if letter == ' ':
        letter = 'whitespace'
    key = letter + str(counter) + '.jpg'
    finalImage = np.array(hashes[key], dtype = np.uint8)

    for i in range(1, len(word)):
        # In every iteration of loop counter goes from 1..5 incremented by 1 
        counter = 1 + (counter + 1)%5
        letter = word[i]
        key = letter + str(counter) + '.jpg'
        if letter == ' ':
            letter = 'whitespace'
            key = letter + '.jpg'
        finalImage = np.hstack((finalImage, np.array(hashes[key], dtype = np.uint8)))

    show(args.word[0], finalImage)

class Parser:
    def __init__(self, hashes):
        self.hashes = hashes

    # Generates image of a line of text
    def lineimage(self, line):
        
        assert(len(line) > 0)
        
        counter = 1
        letter = line[0]
        key = letter + str(counter) + '.jpg'
        if letter == ' ':
            letter = 'whitespace'
            key = letter + '.jpg'
        finalImage = np.array(self.hashes[key], dtype = np.uint8)

        for i in range(1, len(line)):
            counter = 1 + (counter + 1)%5
            letter = line[i]
            key = letter + str(counter) + '.jpg'
            if letter == ' ':
                letter = 'whitespace'
                key = letter + '.jpg'
            finalImage = np.hstack((finalImage, np.array(self.hashes[key], dtype = np.uint8)))

        return finalImage      

    # Generates image of a line of text where output image length is fixed
    def lineimage_constrained(self, line, MAX_CHARS): 
        
        assert(MAX_CHARS > 0)
        
        totalChars = len(line)
        wordlist = line.split()
        leftover = ''
        partialLength = 0
        charsCovered = 0
        starting = True
        finalImage = np.array([[]], dtype = np.uint8)
        # line image is generated word by word
        for word in wordlist:
            partialLength += len(word) + 2 # in every iteration one word and two spaces are added
            charsCovered += len(word) + 1 # in every iteration one word and a space are covered from text line
            if partialLength > MAX_CHARS:
                charsCovered -= (len(word) + 1)
                partialLength -= (len(word) + 2)
                leftover = line[charsCovered:] + '  '
                break
            if starting:
                finalImage = self.lineimage(word)
            else:
                finalImage = np.hstack((finalImage, self.lineimage(word)))
            finalImage = np.hstack((finalImage, self.lineimage('  ')))
            starting = False
        
        # Add spaces to the end of line
        n_spaces = MAX_CHARS - partialLength
        if starting:
            finalImage = self.lineimage(' ')
            n_spaces -= 1
        spaces = ' '*(n_spaces)
        if(len(spaces) > 0):
            finalImage = np.hstack((finalImage, self.lineimage(spaces)))
        # leftover is the text that did not fit in line
        return finalImage, leftover 


    def show(self, window_name, image):
        cv2.imshow(window_name, image)
        cv2.waitKey()
        cv2.destroyWindow(window_name)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Output image for word')
    parser.add_argument('word', type=str, nargs=1)
    args = parser.parse_args()
    main()