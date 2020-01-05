import logging
from os import getcwd, path
from pathlib import Path

from werkzeug.utils import secure_filename

def save_temp_image(image):
    image_filename = secure_filename(image.filename)
    current_path = Path(getcwd())
    temp_image_path = path.join(current_path, 'eyechecker', 'image', 'images', image_filename)
    try:
        logging.info("Guardando imagen")
        image.save(temp_image_path)
        logging.info("Imagen %s ha sido guardada" % image_filename)
        return image_filename
    except Exception as e:
        logging.error("No se pudo guardar la imagen")
        logging.error(e)
        return None