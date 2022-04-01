import os

from flask import request
from flask_restful import Resource
from werkzeug.utils import secure_filename

from utils.image import Image
from utils.transform import adjust_contrast

ALLOW_EXTENSIONS = ['png', 'jpg', 'jpeg']
UPLOAD_FOLDER = 'static/input/'
OUTPUT_FOLDER = 'static/output/'


def file_extensions(filename: str) -> str:
    return filename.split('.')[1].lower()


class AdjustContrastHandler(Resource):
    def post(self):
        factor = request.form['factor']
        mid = request.form['mid']
        file = request.files['file']
        filename = secure_filename(file.filename)
        print("filename =", filename)
        if file_extensions(filename) not in ALLOW_EXTENSIONS:
            return {'status': 'fail', 'message': 'format not support!'}
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        im = Image(filename=filename)
        im.write_image("origin." + file_extensions(filename))

        contrast_im = adjust_contrast(im, int(factor), float(mid))
        contrast_im.write_image('contrast_image.' + file_extensions(filename))

        return {'status': 'success', 'message': 'adjusted contrast'}