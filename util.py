""" Utility funcitons for data_manager """
import os
from werkzeug.utils import secure_filename

from datetime import datetime

""" File upload """
UPLOAD_FOLDER = "static/images/"
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def upload_file(imported_file, old_picture=None):
    if allowed_file(imported_file.filename):
        filename = secure_filename(imported_file.filename)
        if old_picture:
            os.remove(os.path.join(UPLOAD_FOLDER, old_picture))
        imported_file.save(os.path.join(UPLOAD_FOLDER, filename))

        return filename


""" Common date formating """


def submission_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
