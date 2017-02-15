# Met Images

Script to download Met painting images by artist name. Requires that you have already downloaded the entire csv file created by The Met which can be downloaded here: https://github.com/metmuseum/openaccess.

The script searches the csv file and then goes to a webpage on the met website to find a link to download the image. Once it has found the image link, it proceeds to download the images for the artist.

## How to run the program

You must provide the path to the csv file you downloaded from the met, a directory to download the images to, and an artist to search for.

An example on how to run the script to download all the peices created by Claude Monet is below:

'python met_download.py --csv=/path/to/met/csv.csv --out=some_directory --artist="Claude Monet"'



