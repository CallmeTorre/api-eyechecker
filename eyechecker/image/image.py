from feature.border import detect_borders
from feature.exposure import enhance_histogram
from morphology import binary
from util import util


# TODO: Create the sklearn module
#           Put the pickles in the classifier module
#           Erase skimage (added only for testing)
#           Erase all testing variables and logs 
#           Check the parameters to be used in all the methods
#           RCheck how to return the values (JSON and the images)
#           Check how to return each image (float or unit)
#           Check if we should use jit in histogram code
#           Check the types of data that we're creating in the modules (int or float)
#           Optimize and Refactor Morphologhy code

class Image:
    g_height = 1152
    g_width = 1500

    def __init__(self, url: str):
        self.image = util.scale_image(util.open_image(url),
                                      Image.g_height,
                                      Image.g_width)

    def get_microaneurysm_and_hemorrhage(self):
        green_channel = util.get_green_channel(self.image)
        enhanced_image = enhance_histogram.equalize_adapthist(green_channel)
        border_image = detect_borders.canny(enhanced_image)
        micro_and_hemo_and_boders = binary.fill_holes(border_image)
        micro_and_hemo = binary.opening2(micro_and_hemo_and_boders)

        util.view_image(micro_and_hemo)

    def get_hardexudate(self):
        pass


test = Image("images/bimg.jpg")
test.get_microaneurysm_and_hemorrhage()
