#
# Main driver script for labelling the carpet swatches' color
#
import sys
import os
import glob
import csv
import cv2
from color_namer import ColorNamer


def gather_picture_filepaths(input_directory, file_extensions):
    """Return a list of absolute paths to all pictures in input_directory
        that end in one of a specified list of file extensions

    :param input_directory: The input directory of the pictures
    :param file_extensions: A list of accepted file extensions (e.g. 'jpg', 'png')
    :return: A list of absolute paths to all pictures in input_directory with specified file extension
    """
    image_filepaths = []
    for file_extension in file_extensions:
        glob_str = os.path.join(input_directory, "*{0}".format(file_extension))
        image_filepaths.extend(glob.glob(glob_str))

    return image_filepaths


if __name__ == "__main__":

    if len(sys.argv) < 5:
        print("Usage: python {0} num_clusters path_to_picture_directory target_color_file csv_file".format(sys.argv[0]))
        exit()

    # Number of clusters (k) to use for k-means
    num_clusters = int(sys.argv[1])
    # Source directory for all the images to process
    picture_directory = sys.argv[2]
    # Filepath to the target color file
    target_color_filepath = sys.argv[3]
    # Filepath to where to write the output csv
    output_csv_filepath = sys.argv[4]

    accepted_file_extensions = ['jpg', 'jpeg', 'png', 'bmp']
    image_filepaths = gather_picture_filepaths(picture_directory, accepted_file_extensions)

    target_colors = ColorNamer.read_target_color_file(target_color_filepath)

    #Open the CSV file and write the data to the CSV
    with open(output_csv_filepath, "w+") as csvfile:

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

        for image_filepath in image_filepaths:

            print("Processing {0}".format(image_filepath))

            img = cv2.imread(image_filepath)

            avg_color_rgb = ColorNamer.avg_color(img)
            avg_color_name = ColorNamer.name_color(avg_color_rgb, target_colors)
            print("Average Color: {0} -> {1}".format(avg_color_rgb, avg_color_name))

            dominant_color_rgb = ColorNamer.dominant_color(img, num_clusters)
            dominant_color_name = ColorNamer.name_color(dominant_color_rgb, target_colors)
            print("Dominant Color: {0} -> {1}".format(dominant_color_rgb, dominant_color_name))

            # Write the row of picture information to the CSV
            row = [os.path.basename(image_filepath),
                   avg_color_name,
                   avg_color_rgb[0],
                   avg_color_rgb[1],
                   avg_color_rgb[2],
                   dominant_color_name,
                   dominant_color_rgb[0],
                   dominant_color_rgb[1],
                   dominant_color_rgb[2]
            ]

            csv_writer.writerow(row)
