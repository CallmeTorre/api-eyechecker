import logging
from os import getcwd, path
from pathlib import Path

from werkzeug.utils import secure_filename

from eyechecker.image.image import Image
from eyechecker.utils.formatter import format_eye_analysis

def save_temp_image(image):
    """
    Function that receives an image as a FileStorage Class and
    saves it in a temporary folder.
    """
    image_filename = secure_filename(image.filename)
    current_path = Path(getcwd())
    temp_image_path = path.join(current_path, 'eyechecker', 'image', 'images', image_filename)
    try:
        logging.info("Guardando imagen")
        image.save(temp_image_path)
        logging.info("Imagen %s ha sido guardada" % image_filename)
        return temp_image_path
    except Exception as e:
        logging.error("No se pudo guardar la imagen")
        logging.error(e)
        return None


def image_analysis(eye_key, params):
    if(eye_key in params):
        eye_path = save_temp_image(params[eye_key])
        if(eye_path):
            eye_class = Image(eye_path)
            eye_micros, eye_hemorrhages = eye_class.get_microaneurysms_and_hemorrhages()
            return format_eye_analysis(eye_key, eye_micros, eye_hemorrhages)
    else:
        return {}