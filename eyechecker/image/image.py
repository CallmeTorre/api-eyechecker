from eyechecker.image.classifier.characteristic import distinction
from eyechecker.image.classifier.extraction import region
from eyechecker.image.classifier.model import classify
from eyechecker.image.feature.border import detect_borders
from eyechecker.image.feature.exposure import enhance_histogram, threshold
from eyechecker.image.morphology import binary
from eyechecker.image.util import util

# TODO: Create the sklearn module
#           Check the type of value that you return after the cropping the image
#           Check resize(preserve_range=False) argument
#           Erase all testing variables and logs
#           Check the parameters to be used in all the methods
#           RCheck how to return the values (JSON and the images)
#           Check how to return each image (float or unit)
#           Check the types of data that we're creating in the modules (int or float)
#           Create the unit test for Morphologhy code
#           Check if we should use FloodFills or skimage in region.py (CHECK THE TYPE OF CONNECTED PIXELS)
#           Create a decorator to handle exceptions
#           Check edge cases (None)
#           Check the new circle area for distinction.distinct_between_ma_ha
#           Check the parameters in the ML algorithm
#           Check the order of the items to be classified
#           Remember to get the green values from the original image to classify the lession
#           Missing the code to paint the real lesions in the image
class Image:
    g_height = 1152
    g_width = 1500

    def __init__(self, url: str):
        self.img = util.scale_image(util.open_image(url),
                                    Image.g_height,
                                    Image.g_width)
        self.ma_img = None
        self.he_img = None
        self.hr_img = None

    def get_microaneurysms_and_hemorrhages(self):
        green_channel = util.get_green_channel(self.img)
        enhanced_img = enhance_histogram.equalize_adapthist(green_channel, clip_limit=0.05)
        border_img = detect_borders.canny(enhanced_img, sigma=1.5, high_threshold=0.15)

        micro_hemo_and_borders = binary.fill_holes(border_img)
        micro_and_hemo = binary.remove_border(micro_hemo_and_borders, border_img)
        micro_and_hemo = binary.opening(micro_and_hemo)
        points_of_interest = region.get_coordinates_of_the_regions(micro_and_hemo)
        possible_micro, possible_hemo = distinction.distinct_between_ma_ha(points_of_interest)

        green_values_of_micro_points = region.get_green_values_from_coordinates(possible_micro, green_channel)
        green_values_of_hemo_points = region.get_green_values_from_coordinates(possible_hemo, green_channel)

        real_micro = classify.classify(green_values_of_micro_points, "ma")
        real_hemo = classify.classify(green_values_of_hemo_points, "hr")

        self.ma_img = util.paint_lesions(self.img, real_micro, possible_micro)
        self.hr_img = util.paint_lesions(self.img, real_hemo, possible_hemo)

        return util.save_image("imagen_final", self.ma_img), util.save_image("imagen_final_2", self.hr_img)

        ###################
        #util.view_image(self.ma_img)
        #util.view_image(self.hr_img)
        ###################

    def get_hardexudate(self):
        green_channel = util.get_green_channel(self.img)
        hsv_channel = util.get_HSV_channel(self.img)
        bright_regions = threshold.get_bright_regions(hsv_channel, green_channel)

        points_of_interest = region.get_coordinates_of_the_regions(bright_regions)        
        possible_hard_exu = distinction.distinct_betwen_disc_and_exudate(points_of_interest)
        green_values_of_points = region.get_green_values_from_coordinates(possible_hard_exu, green_channel)
        
        real_he = classify.classify(green_values_of_points, "he")
        
        self.he_img = util.paint_lesions(self.img, real_he, possible_hard_exu)
        return util.save_image("imagen_final_3", self.he_img)

        ###################
        # util.view_image(self.he_img)
        ###################


# test = Image("images/bimg.jpg")
#test = Image("images/timg.png")

#test.get_microaneurysms_and_hemorrhages()
# test.get_hardexudate()
