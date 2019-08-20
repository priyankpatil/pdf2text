# https://stackabuse.com/pytesseract-simple-python-optical-character-recognition/

# Download imagemagick - https://imagemagick.org/script/download.php
# Download ghostscript - https://www.ghostscript.com/download/gsdnld.html
# Dowload tessarct - https://github.com/UB-Mannheim/tesseract/wiki or https://github.com/tesseract-ocr/tesseract/wiki/4.0-with-LSTM#400-alpha-for-windows

import os
from flask import Flask, render_template, request

# import our OCR function - image
from ocr_core_image import ocr_core_image

# import OCR function - pdf
from ocr_core_pdf import ocr_core_pdf

# define a folder to store and later serve the images
UPLOAD_FOLDER = '/static/uploads/'

# allow files of a specific type
ALLOWED_EXTENSIONS1 = set(['png', 'jpg', 'jpeg'])
ALLOWED_EXTENSIONS2 = set(['pdf'])

app = Flask(__name__)

# function to check the file extension


def allowed_file1(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS1


def allowed_file2(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS2

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

        if file and allowed_file1(file.filename):

            # call the OCR function on it
            extracted_text = ocr_core_image(file)

            # extract the text and display it
            return render_template('upload.html',
                                   msg='Successfully processed',
                                   extracted_text=extracted_text,
                                   img_src=UPLOAD_FOLDER + file.filename)

        elif file and allowed_file2(file.filename):

            # call the OCR function on it
            extracted_text = ocr_core_pdf(file)

            # extract the text and display it
            return render_template('upload.html',
                                   msg='Successfully processed',
                                   extracted_text=extracted_text,
                                   img_src=UPLOAD_FOLDER + file.filename)

        else:
            return render_template('upload.html',
                                   msg='Filetype not supported')

    elif request.method == 'GET':
        return render_template('upload.html')


if __name__ == '__main__':
    app.run()
