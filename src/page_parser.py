import argparse
from docx import Document
import cv2
import numpy as np
from line_parser import LineParser
import re

class PageParser(LineParser):
    def __init__(self, hashes, CHARS_PER_LINE):
        LineParser.__init__(self, hashes)
        self.CHARS_PER_LINE = CHARS_PER_LINE

        self.keys_alignment = {'`' : None, '``' : 1, '```' : 2, '````' : 3}
        self.alignment_keys = {None : '` ', 0 : '` ', 1 : '`` ', 2 : '``` ' , 3 : '```` '}
    
    # Returns a list of lines that belong to the same page
    def parse_page(self, document, show = False):
        # denotes text that doesn't fit in a line an must be printed in the next line
        leftover = ''
        # list that stores image of each line
        lines = []
        alignment_carry = None

        # In every iteration, generate a line and wrap the leftover text to next line
        for para in document.paragraphs:
            text = re.sub('[\n\r]', '', para.text)
            text = re.sub('\s+', ' ', text)
            text = re.sub('\t', ' ', text)
            para_alignment = para.paragraph_format.alignment
            text = leftover + self.alignment_keys[para_alignment] + text + ' | '
            image, leftover, alignment_carry = self.parse_line_constrained(text, self.keys_alignment, self.CHARS_PER_LINE, alignment_carry)
            lines.append(image)

        # print all leftover text
        while leftover != '':
            text = leftover
            image, leftover, alignment_carry = self.parse_line_constrained(text, self.keys_alignment, self.CHARS_PER_LINE, alignment_carry)
            lines.append(image)
        
        if len(lines) == 0:
            print('Empty document!')
            return lines

        if show:
            page = lines[0]
            for i in range(1, len(lines)):
                page = np.vstack((page, lines[i]))
            self.show('window', page)
        return lines

    # Parse page - add page breaks when max no of lines in page is exceeded
    # fill incomplete page with lines of whitespaces
    # Uses parse_page(), returns a list of images of each page
    
    def parse_pages_constrained(self, document, LINES_PER_PAGE, show = False):
        lines = self.parse_page(document, show = False)
        line_shape = lines[0].shape

        totalLines = len(lines)
        totalPages = (totalLines // LINES_PER_PAGE)
        # Work-around to https://stackoverflow.com/questions/19951816/python-changes-to-my-copy-variable-affect-the-original-variable
        # Instead of appending temporary variable to a list of final images
        # Initialize list to required size and modify value at each index 
        finalImages = [[[i]] for i in range(0, totalPages)]
        
        remainderLines = totalLines % LINES_PER_PAGE
        blankLines = (LINES_PER_PAGE - (remainderLines)) % LINES_PER_PAGE

        if remainderLines != 0:
            finalImages.append([[0]])

        # Compute blank lines
        blanks = np.full((blankLines * line_shape[0], line_shape[1], line_shape[2]), 255, dtype = np.uint8)

        # Print all complete pages
        pageIndex = 0
        for i in range(0, totalPages):
            starting = True
            for j in range(i*LINES_PER_PAGE, (i+1)*LINES_PER_PAGE):
                if starting:
                    finalImages[pageIndex] = lines[j]
                    starting = False
                else:
                    finalImages[pageIndex] = np.vstack((finalImages[pageIndex], lines[j]))
            pageIndex += 1
        
        # Print incomplete page
        starting = True
        for i in range(0, remainderLines):
            if starting:
                finalImages[pageIndex] = lines[totalPages*LINES_PER_PAGE + i]
                starting = False
            else:
                finalImages[pageIndex] = np.vstack((finalImages[pageIndex], lines[totalPages*LINES_PER_PAGE + i]))

        # Print blanks at end of incomplete page
    

        if len(blanks) > 0:
            finalImages[pageIndex] = np.vstack((finalImages[pageIndex], blanks))

        # Add top and bottom margin
        vertical_margin = np.full((line_shape[0], line_shape[1], line_shape[2]), 255, dtype = np.uint8)
        
        for index in range(0, len(finalImages)):
            finalImages[index] = np.vstack((finalImages[index], vertical_margin))   # Add margin on bottom of page
            finalImages[index] = np.vstack((vertical_margin, finalImages[index]))   # Add margin on top of page

        # show all pages
        if show:
            for finalImage in finalImages:
                self.show('window', finalImage)
        return finalImages

    # Generates page from a list of lines
    def generate_page(line_list):
        if len(line_list) > 0:
            page = line_list[0]
            for i in range(1, len(line_list)):
                page = np.vstack((page, line_list[i]))
            return page
        else:
            print('Empty image list!')
            return [[]]



