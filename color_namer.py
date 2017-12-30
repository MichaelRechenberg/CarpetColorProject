import numpy as np
from scipy.spatial import distance
from scipy.stats import itemfreq
import cv2


#
# Note: OpenCV opens images in BGR format, not RGB
#
class ColorNamer:
    """Class for naming a given RGB tuple (5, 230, 7) to a human name like "green"

    """

    def __init__(self):
        pass

    @classmethod
    def name_color(cls, input_color_tuple, target_colors):
        """Return the label of the closest color that input_tuple is to a color in target_colors
            (determined using Euclidean distance in RGB space)

        :param input_color_tuple: An RGB tuple of the color you want to name
        :param target_colors: A list of Colors to use for labelling
        :return: The name of the Color closest to the input_tuple
        """
        target_rgb_list = [color.rgb for color in target_colors]
        distances_from_input = [distance.euclidean(input_color_tuple, target_rgb) for target_rgb in target_rgb_list]

        closest_target_color_idx = np.argmin(distances_from_input)
        return target_colors[closest_target_color_idx].name

    @classmethod
    def read_target_color_file(cls, filename):
        """Read in a target color file into a list of Colors

        Each line of the target color file should be of the form

        <color_name> <R> <G> <B>

        For example:

            green 0 255 0
            red 255 0 0

        :param filename: The file containing the target colors
        :return: The target colors of the target color file as a list of Colors
        """

        target_color_list = []
        with open(filename, 'r') as target_color_file:
            lines = [line.strip() for line in target_color_file.readlines()]

            for line in lines:
                split_str_list = line.split(' ')
                color_name = split_str_list[0]
                rgb_tuple = [int(channel_value) for channel_value in split_str_list[1:]]
                target_color_list.append(Color(rgb_tuple, color_name))

        return target_color_list


    @classmethod
    def dominant_color(cls, img, k):
        """Return an RGB tuple of the dominant color in an image

        Performs k-means clustering on the image's pixels, then selects the centroid
            of the largest cluster to be the dominant color of the image

        Uses kmeans++ for cluster initialization

        :param img: The image to analyze, read in via cv2.imread()
        :param k: The number of clusters to use
        :return: The RGB tuple of the dominant color in the image
        """

        img_as_float32 = np.float32(img)
        pixels = img_as_float32.reshape((-1, 3))
        # Stop after MAX_ITER iterations OR accuracy EPS (epsilon) is reached
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, 0.1)
        # Use kmeans++ center initialization
        flags = cv2.KMEANS_PP_CENTERS
        # Amount of times the algorithm is attempted
        attempts = 10

        _, labels, centroids = cv2.kmeans(pixels, k, criteria, attempts, flags)

        candidate_dominant_colors = np.uint8(centroids)
        # The dominant color is the cluster with the largest number of members/pixels
        dominant_color_idx = np.argmax(itemfreq(labels)[:, -1])
        dominant_color_tuple = candidate_dominant_colors[dominant_color_idx]

        d_blue = dominant_color_tuple[0]
        d_green = dominant_color_tuple[1]
        d_red = dominant_color_tuple[2]

        return (d_red, d_green, d_blue)

    @classmethod
    def avg_color(cls, img):
        """Return RGB tuple of the average color of the image (arithmetic mean for each RGB channel)

        :param img: The image to analyze, read in via cv2.imread()
        :return: The RGB tuple of the average color in the image
        """
        avg_color_per_row = np.average(img, axis=0)
        avg_color = np.average(avg_color_per_row, axis=0)
        a_blue = int(avg_color[0])
        a_green = int(avg_color[1])
        a_red = int(avg_color[2])

        return (a_red, a_green, a_blue)


class Color:
    """Container for a Color (an RGB tuple and a human name like "green")
    """

    def __init__(self, rgb_tuple, name):
        self.rgb = rgb_tuple
        self.name = name

