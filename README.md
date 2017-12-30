# What This Is:

  This project was to help my uncle label images of carpet swatches by what color they were
    and create a .csv file for him to incorporate into his database.


# Running the Code:

Using Python 2.7 and OpenCV2

The appropriate environment can be installed w/ conda using

    conda env create -f environment.yml
    source activate CarpetColorProject

The script can then be run with

    python label_picture_color.py k path_to_picture_directory target_color_file csv_file
    
* k -> The number of clusters to use for k-means clustering (2 is recommended, but you can experiment with 1 or 3)    
* path_to_picture_directory -> Path to the directory containing the carpet swatch pictures
* target_color_file -> Path to the text file containing the target colors to use for labelling
* csv_file -> Path to write the output .csv file to

## Target Color File

The Target Color File is a text file that specifies the desired labels for the average and dominant colors.
Each target color should be on its own line in the following format:

        color_name red_channel_value green_channel_value blue_channel_value
        
Example:

        red 255 0 0
        green 0 255 0
        
# How It Works

For the average color, I simply find the arithmetic mean for each RGB channel separately over all pixels
For the dominant color, I use kmeans clustering on the pixels of each image. After clustering, the centroid of the
 largest cluster is called the dominant color of the image.
 
To give a human-readable label to RGB values (e.g. (0, 255, 0) -> "Green" ) I select the target color closest
 to the input RGB tuple in RGB space (using Euclidean distance as the distance measure)

# Windows Users:

The environment.yml file is meant for Linux distros. For Windows users, you should
  install the conda environment from windows_environment.yml instead of environment.yml.
  The conda environment from windows_environment.yml will be named "carpet-windows"
  by default.
