import os

import numpy as np
from flask import request
from flask_restful import Resource
from werkzeug.utils import secure_filename

from image import Image
import transform

ALLOW_EXTENSIONS = ['png']#, 'jpg', 'jpeg']
UPLOAD_FOLDER = 'static/input/'
OUTPUT_FOLDER = 'static/output/'


def file_extensions(filename: str) -> str:
    return filename.split('.')[-1].lower()


class BrightenHandler(Resource):
    def post(self):
        factor = request.form['factor']
        file = request.files['file']
        filename = secure_filename(file.filename)
        # print("filename =", filename)
        if file_extensions(filename) not in ALLOW_EXTENSIONS:
            return {'status': 'fail', 'message': 'format not support!'}
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        im = Image(filename=filename)
        im.write_image("origin." + file_extensions(filename))

        brighten_im = transform.brighten(im, float(factor))
        brighten_im.write_image('brighten_image.' + file_extensions(filename))


        return {'status': 'success', 'message': 'brightened'}


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
        print('mark1')
        im.write_image("origin." + file_extensions(filename))
        print('mark2')

        contrast_im = transform.adjust_contrast(im, float(factor), float(mid))
        contrast_im.write_image('contrast_image.' + file_extensions(filename))

        return {'status': 'success', 'message': 'adjusted contrast'}


class BlurHandler(Resource):
    def post(self):
        kernel_size = request.form['kernel']
        file = request.files['file']
        filename = secure_filename(file.filename)
        # print("filename =", filename)
        if file_extensions(filename) not in ALLOW_EXTENSIONS:
            return {'status': 'fail', 'message': 'format not support!'}
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        im = Image(filename=filename)
        im.write_image("origin." + file_extensions(filename))

        blur_im = transform.blur(im, int(kernel_size))
        blur_im.write_image('blur_image.' + file_extensions(filename))

        return {'status': 'success', 'message': 'blured'}


class ApplyKernelHandler(Resource):
    def post(self):
        kernel_size = request.form['kernel']
        file = request.files['file']
        filename = secure_filename(file.filename)
        if file_extensions(filename) not in ALLOW_EXTENSIONS:
            return {'status': 'fail', 'message': 'format not support!'}
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        im = Image(filename=filename)
        im.write_image("origin." + file_extensions(filename))

        kernel_im = transform.apply_kernel(im, np.fromstring(kernel_size, dtype=int, sep=',').reshape(-1, 3))
        kernel_im.write_image('kernel_image.' + file_extensions(filename))

        return {'status': 'success', 'message': 'applied kernel'}


class CombineImageHandler(Resource):
    def post(self):
        file1 = request.files['file1']
        filename1 = secure_filename(file1.filename)
        file2 = request.files['file2']
        filename2 = secure_filename(file2.filename)
        if file_extensions(filename1) not in ALLOW_EXTENSIONS or file_extensions(filename2) not in ALLOW_EXTENSIONS:
            return {'status': 'fail', 'message': 'format not support!'}
        if file_extensions(filename1) != file_extensions(filename2):
            return {'status': 'fail', 'message': 'images have different formats'}
        file1.save(os.path.join(UPLOAD_FOLDER, filename1))
        file2.save(os.path.join(UPLOAD_FOLDER, filename2))
        im1 = Image(filename=filename1)
        im1.write_image("origin1." + file_extensions(filename1))
        im2 = Image(filename=filename2)
        im2.write_image("origin2." + file_extensions(filename2))

        combined_im = transform.combine_images(im1, im2)
        combined_im.write_image('combined_image.' + file_extensions(filename1))

        return {'status': 'success', 'message': 'combined image'}