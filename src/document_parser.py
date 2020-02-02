import argparse
import json
from docx import Document
from page_parser import PageParser
from PIL import Image

class DocumentParser(PageParser):
    def __init__(self, hashes, CHARS_PER_LINE, LINES_PER_PAGE): 
        PageParser.__init__(self, hashes, CHARS_PER_LINE)
        self.LINES_PER_PAGE = LINES_PER_PAGE
    

    def parse_document(self, document, destination_path):
        page_parser = PageParser(self.hashes, self.CHARS_PER_LINE)
        pageImages = page_parser.parse_pages_constrained(document, self.LINES_PER_PAGE, False)
        
        # Each image (currently an np.ndarray) has to be converted into a PIL Image
        # these images are stored in allImages:
        allImages = []
        for index in range(1, len(pageImages)):
            allImages.append(
                Image.fromarray(pageImages[index].astype('uint8'), 'RGB')
            )
        firstPage = Image.fromarray(pageImages[0].astype('uint8'), 'RGB')
        firstPage.save(destination_path, "PDF", save_all = True, append_images = allImages, resolution = 100.0)


def main():
    document = Document('../test.docx')
    with open('../hashes.json') as f:
        hashes = json.load(f)
    CHARS_PER_LINE = 54
    LINES_PER_PAGE = 30

    document_parser = DocumentParser(hashes, CHARS_PER_LINE, LINES_PER_PAGE)
    document_parser.parse_document(document, '../out.pdf')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Output pages for docx document')
    parser.add_argument('document_path', type=str, nargs=1)
    args = parser.parse_args()

    main()

    