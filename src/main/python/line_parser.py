import argparse
# import cv2            Use to debug. In release, no cv2 to reduce size. Use pip install python-opencv
import random
import numpy as np
import re
from math import ceil


class LineParser:
    def __init__(self, hashes):
        self.hashes = hashes

    # Generates image of a line of text
    def parse_line(self, line):
        
        counter = random.randrange(1, 6, 1)

        # initialze finalImage to the image of first word before appending other words
        letter = line[0]
        if check_inv(letter) == True:
            letter = 'inv'
        elif check_dinv(letter) == True:
            letter = 'dinv'
        elif check_hyphen(letter):
            letter = '-'

        key = letter + str(counter) + '.jpg'
        
        if letter == ' ':
            letter = 'whitespace'
            key = letter + '.jpg'
        finalImage = self.hashes[key]
        
        for i in range(1, len(line)):
            # In every iteration of counter is a random number between 1..5
            counter = random.randrange(1, 6, 1)
            letter = line[i]
            # JSON file contains dictionary where key is like A3.jpg and value is image array
            # Keys are accordingly generated
            if check_inv(letter) == True:
                letter = 'inv'
            elif check_dinv(letter) == True:
                letter = 'dinv'
            elif check_hyphen(letter):
                letter = '-'
            
            key = letter + str(counter) + '.jpg'

            if letter == ' ':
                letter = 'whitespace'
                key = letter + '.jpg'
            finalImage = np.hstack((finalImage, self.hashes[key]))

        return finalImage      

    # Generates image of a line of text where output image length is fixed
    # Invokes parse_line with additional logic wrapped around it
    def parse_line_constrained(self, line, keys_alignment_dict, MAX_CHARS, alignment_carry, para_end_sentinel = '|'): 

        assert(MAX_CHARS > 0)
        
        wordlist = line.split()
        leftover = ''

        partialLength = 0
        charsCovered = 0
        alignment = alignment_carry
        finalImage = np.array([[[]]], dtype = np.uint8)

        
        # 2 characters on left edge are used up for blankspaces - left margin
        if MAX_CHARS > 2:
            finalImage = self.parse_line('  ')
            partialLength += 2
        # line image is generated word by word
        for word in wordlist:

            if word == para_end_sentinel:
                charsCovered += len(para_end_sentinel) + 1
                leftover = line[charsCovered:]
                break

            if word in keys_alignment_dict:
                alignment = keys_alignment_dict[word]
                charsCovered += len(word) + 1
                continue

            partialLength += len(word) + 2 # in every iteration one word and two spaces are added
            charsCovered += len(word) + 1 # in every iteration one word and a space are covered from text line
            
            if partialLength > MAX_CHARS:
                charsCovered -= (len(word) + 1)
                partialLength -= (len(word) + 2)
                leftover = line[charsCovered:]
                break
            
            finalImage = np.hstack((finalImage, self.parse_line(word + '  ')))

        # Add spaces for remaining characters in line
        n_spaces = MAX_CHARS - partialLength

        if n_spaces > 0:
            # Left aligned or justified text
            if alignment == 3 or alignment == None:
                spaces = ' '*(n_spaces)
                finalImage = np.hstack((finalImage, self.parse_line(spaces)))

            # Right aligned text
            elif alignment == 2:
                spaces = ' '*(n_spaces)
                finalImage = np.hstack((self.parse_line(spaces), finalImage))

            #Center aligned text
            elif alignment == 1:
                l_spaces = ' '*(n_spaces // 2)
                r_spaces = ' '*ceil(n_spaces / 2)
                if len(l_spaces) > 0:
                    finalImage = np.hstack((self.parse_line(l_spaces), finalImage))
                finalImage = np.hstack((finalImage, self.parse_line(r_spaces)))

        next_line_alignment = alignment
        # leftover is the text that did not fit in line
        return finalImage, leftover, next_line_alignment 


    def show(self, window_name, image):
        # Used to debug. Uncomment the lines below and install python-opencv
        # cv2.imshow(window_name, image)
        # cv2.waitKey()
        # cv2.destroyWindow(window_name)
        return


def check_inv(letter):
    if letter == '‘' or letter == '’' or letter == "'":
        return True
    else:
        return False

def check_dinv(letter):
    if letter == '“' or letter == '”' or letter == '"':
        return True
    else:
        return False

def check_hyphen(letter):
    if letter == '-' or letter == '–':
        return True
    else:
        return False
