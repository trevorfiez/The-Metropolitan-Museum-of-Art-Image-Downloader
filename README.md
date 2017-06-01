# The Met Image Downloader #

Script to download Met painting images by artist name, type, or a list of object numbers. Requires that you have already
 downloaded the entire csv file created by The Met which can be downloaded here: https://github.com/metmuseum/openaccess.

The script searches the csv file, given your search choices, and then goes to a webpage on the met website to find a link to download the image. Once it
 has found the image link, it proceeds to download the images you have selected.

To get object number of paintings, you can go to http://www.metmuseum.org/art/collection, set the filters you are interested
in, and then copy the ascension number and paste it into a text file. Each line needs to have only one ascension number. Since,
many of the pieces are not public domain, I recommend you select the public domain artworks filter.

An example downloading paintings using the ascension number is the `paintings.txt` file.

If you do anything cool with the images you download, I would love to hear about it! Email me if you get the chance.

## How to run the program ##

You must provide the path to the csv file you downloaded from the met, a directory to download the images into, and an artist to search for.

An example on how to run the script to download all the pieces created by Claude Monet is below:

`python met_download.py --csv=/path/to/met/csv.csv --out=some_directory --artist="Claude Monet"`

Or an example on how to download the images from `painting.txt` is:

`python met_download.py --csv=/path/to/met/csv.csv --out=some_directory --list=paintings.txt`

## Search Options ##

### -l, --list ###

Given a list of acsension numbers, the script will download the images

### -a, --artist ###

Given an artist, or artists, the script will download all pieces associated with that artist. Multiple artists can
be named at once by splitting their names with a ":". For example, -a "Claude Monet":"Vincent Van Gogh":"Paul Klee"

### -t, --type ###

Maybe you just want oil paintings, you can select those options using -t "Oil paintings". Be careful all spelling is taken
verbatim so if you do not capitalize "oil", for instance, it will not make any paintings.






