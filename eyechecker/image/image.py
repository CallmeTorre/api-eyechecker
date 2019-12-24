from io.file import *

from image.feature.border import detect_borders
from image.feature.exposure import enhance_histogram
from image.util import util


# TODO: Create the sklearn module
#           Put the pickles in the module
#
class Image:
    g_height = 1152
    g_width = 1500

    def __init__(self, url: str):
        self.image = util.scale_image(util.open_image(url),
                                      Image.g_height,
                                      Image.g_width)

    def get_microaneurysm(self):
        # TODO: Check the parameters to be used in border_image
        green_channel = util.get_green_channel(self.image)
        enhanced_image = enhance_histogram.equalize_adapthist(green_channel)
        border_image = detect_borders.canny(enhanced_image)

    def get_hardexudates(self):
        pass
