# https://stackabuse.com/pytesseract-simple-python-optical-character-recognition/

# Download imagemagick - https://imagemagick.org/script/download.php
# Download ghostscript - https://www.ghostscript.com/download/gsdnld.html
# Dowload tessarct - https://github.com/UB-Mannheim/tesseract/wiki or https://github.com/tesseract-ocr/tesseract/wiki/4.0-with-LSTM#400-alpha-for-windows

import os
from flask import Flask, render_template, request

# import our OCR function - image
from ocr_core_image import ocr_core

# import OCR function - pdf
from ocr_core_pdf import Get_text_from_image

# define a folder to store and later serve the images
UPLOAD_FOLDER = '/static/uploads/'

# allow files of a specific type
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'pdf'])

app = Flask(__name__)

# function to check the file extension


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# route and function to handle the home page
@app.route('/')
def home_page():
    return render_template('index.html')

# route and function to handle the upload page
@app.route('/upload', methods=['GET', 'POST'])
def upload_page():
    if request.method == 'POST':
        # check if there is a file in the request
        if 'file' not in request.files:
            return render_template('upload.html', msg='No file selected')
        file = request.files['file']
        # if no file is selected
        if file.filename == '':
            return render_template('upload.html', msg='No file selected')

        if file and allowed_file(file.filename):

            if file.lower().endswith(('.png', '.jpg', '.jpeg')):

                # call the OCR function on it
                extracted_text = ocr_core(file)

            elif file.lower().endswith(('.pdf')):
                Get_text_from_image(file)

            else:
                return("Not a supported file format")

            # extract the text and display it
            return render_template('upload.html',
                                   msg='Successfully processed',
                                   extracted_text=extracted_text,
                                   img_src=UPLOAD_FOLDER + file.filename)
    elif request.method == 'GET':
        return render_template('upload.html')


if __name__ == '__main__':
    app.run()
