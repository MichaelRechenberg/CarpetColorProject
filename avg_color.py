# Python script for Uncle Kevin

# Author: Michael Rechenberg

# Takes all of the images from a given directory
#   and finds the average and dominant color within them
# Average color - simply arithmetic mean over all pixels
# Dominant color - select larges cluster from k-means clustering

# Modified from http://stackoverflow.com/questions/43111029/how-to-find-the-average-colour-of-an-image-in-python-with-opencv


import cv2
import webcolors
import glob
import sys
import os
import numpy as np
from scipy.stats import itemfreq
import csv



#TODO: construct custom list of RGB values if I want, from color_notes.txt
#Coerce any RGB value to the closest color name webcolors likes,
#  using closest color in Euclidean distance
def closest_colour(requested_colour):
    min_colours = {}
    for key, name in webcolors.css3_hex_to_names.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - requested_colour[0]) ** 2
        gd = (g_c - requested_colour[1]) ** 2
        bd = (b_c - requested_colour[2]) ** 2
        min_colours[(rd + gd + bd)] = name
    return min_colours[min(min_colours.keys())]

def get_colour_name(requested_colour, spec='css3'):
    try:
        closest_name = actual_name = webcolors.rgb_to_name(requested_colour, spec)
    except ValueError:
        closest_name = closest_colour(requested_colour)
        actual_name = None
    return actual_name, closest_name

 


#Meat and Potatoes of the script

if(len(sys.argv) < 3):
  print("Usage: python avg_color.py path_to_picture_directory csv_name")
  exit()
 

#Get all of the filenames that end in certain file_extensions
#   within the desired directory
directory = sys.argv[1]
print(directory)
file_extensions = ['jpg', 'png']
images_to_process = []
for file_extension in file_extensions:
  glob_str = os.path.join(directory, "*{0}".format(file_extension))
  images_to_process.extend(glob.glob(glob_str))


#Open the CSV file and write the data to the CSV
with open(sys.argv[2], "w+") as csvfile: 
  csv_writer = csv.writer(csvfile)
  header = ['Image Filename',
            'Avg Color Name',
            'A_Red',
            'A_Green',
            'A_Blue',
            'Dominant Color Name',
            'D_Red',
            'D_Green',
            'D_Blue']
  csv_writer.writerow(header)

  #For every image in the directory, 
  # compute average and dominant color
  for image in images_to_process:
    
    print("Processing {0}".format(os.path.basename(image)))

    #Note: OpenCV opens image in BGR mode
    img = cv2.imread(image)

    #Average Color
    avg_color_per_row = np.average(img, axis=0)
    avg_color = np.average(avg_color_per_row, axis=0)
    a_blue = int(avg_color[0])
    a_green = int(avg_color[1])
    a_red = int(avg_color[2])
    rgb_triplet = (a_red, a_green, a_blue)
    avg_color_name = get_colour_name(rgb_triplet, 'css3')[1]
    print("Average Color: {0} -> {1}".format(rgb_triplet, avg_color_name))



    #Dominant Color, using K-means clustering
    #Code modified from StackOverflow post
    average_color = [img[:, :, i].mean() for i in range(img.shape[-1])]
    arr = np.float32(img)
    pixels = arr.reshape((-1, 3))

    #Number of clusters, k
    n_colors = 2
    #Stop after MAX_ITER iterations or accuracy EPS (epsilon) is reached
    # Second element is MAX_ITER, Third element is epsilon
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, 0.1)
    #Start off with random centers
    flags = cv2.KMEANS_RANDOM_CENTERS
    #Amount of times the algorithm is attempted
    attempts = 10 
    _, labels, centroids = cv2.kmeans(pixels, n_colors, criteria, attempts, flags)

    palette = np.uint8(centroids)
    quantized = palette[labels.flatten()]
    quantized = quantized.reshape(img.shape)
    #The dominant color is the cluster with the largest number of members/pixels
    dominant_color = palette[np.argmax(itemfreq(labels)[:, -1])]
    #OpenCV orders their colors differently than RGB :(
    d_blue = dominant_color[0]
    d_green = dominant_color[1]
    d_red = dominant_color[2]
    dominant_color_tuple = (d_red, d_green, d_blue)
    dominant_color_name = get_colour_name(dominant_color_tuple, 'css3')[1]
    print("Dominant Color: {0} -> {1}".format(dominant_color_tuple, dominant_color_name))

    row = [os.path.basename(image), 
        avg_color_name, 
        a_red, 
        a_green, 
        a_blue,
        dominant_color_name,
        d_red,
        d_green,
        d_blue]
    csv_writer.writerow(row)

