# Download imagemagick - https://imagemagick.org/script/download.php
# Download ghostscript - https://www.ghostscript.com/download/gsdnld.html
# Dowload tessarct - https://github.com/UB-Mannheim/tesseract/wiki or https://github.com/tesseract-ocr/tesseract/wiki/4.0-with-LSTM#400-alpha-for-windows

import os
import io
from PIL import Image
import pytesseract
from wand.image import Image as wi
import gc

#Image.Image.image_cmd = r"C:\Program Files\ImageMagick-7.0.8-Q16\magick.exe"

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

filename = r"C:\Users\username\Downloads\test_invoice.pdf"

pdf = wi(filename=filename, resolution=300)
pdfImg = pdf.convert('jpeg')


def Get_text_from_image(filename):
    pdf = wi(filename=filename, resolution=300)
    pdfImg = pdf.convert('jpeg')
    imgBlobs = []

    for img in pdfImg.sequence:
        page = wi(image=img)
        imgBlobs.append(page.make_blob('jpeg'))

    extracted_text = []

    for imgBlob in imgBlobs:
        im = Image.open(io.BytesIO(imgBlob))
        text = pytesseract.image_to_string(im, lang='eng')
        extracted_text.append(text)

    text = "\n".join(extracted_text)

    return(text)


print(Get_text_from_image(filename))
