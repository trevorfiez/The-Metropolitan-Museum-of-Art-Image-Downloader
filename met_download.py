


import urllib2
import sys
import getopt
import csv
import os
from selenium import webdriver


def check_artists(artist, artists):
    if (len(artists) == 0):
        return True
    else:
	    return artist in artists

def check_types(piece_type, types):
	if (len(types) == 0):
		return True
	else:
		return piece_type in types

def check_object_num(object_num, num_list):
	return object_num in num_list

#returns list of csv lines that the artist matches
def match_lines(met_csv, artists, types, list_file):
	lines = []

	print(artists)
	if (list_file != ""):
		f = open(list_file, 'r')
		obj_num_list = []
		for line in f:
			obj_num_list.append(line.strip())
			
		for row in met_csv:
			if (check_object_num(row[0], obj_num_list)):
				lines.append(row)
	else:
		for row in met_csv:
			if (check_artists(row[14], artists) and check_types(row[24], types)):
				lines.append(row)

	return lines
	

def download_lines(lines, out_dir, met_csv):
    image_names = []

    
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    with open(os.path.join(out_dir, "piece_info.csv"), 'wb') as csv_file:
        im_writer = csv.writer(csv_file, delimiter=',')

        for row in met_csv:
            im_writer.writerow(row + ['Image Location'])
            break

        # Note: you will need geckodriver.
        # See https://pypi.org/project/selenium.
        driver = webdriver.Firefox()
        for line in lines:
            res = ""
            try:
                driver.get('http://www.metmuseum.org/art/collection/search/' + line[3].strip())
                html = driver.page_source
            except urllib2.URLError, e:
                image_names.append(None)
                print("URL Error")
                continue

            offset = html.find("artwork__interaction artwork__interaction--download")

            print(offset)
            if (offset == -1):
                image_names.append(None)
                continue
            offset = html[offset:].find('http') + offset
            end = html[offset:].find('.jpg') + offset + 4

            if (end - offset > 300):
                image_names.append(None)
                print("URL Error")
                continue

            image_link = html[offset:end]
            print(image_link)

            image_name = image_link.split('/')[-1]

            image_path = os.path.join(out_dir, image_name)

            image_file = ""
            try:
                image_file = urllib2.urlopen(image_link)
            except urllib2.URLError, e:
                image_names.append(None)
                print("URL error")
                continue		

            with open(image_path, 'wb') as output:
                output.write(image_file.read())

            image_names.append(image_path)

            if (image_names[-1] == None):
                continue

            im_writer.writerow(line + [image_names[-1]])

            print(image_link)

    return image_names
		

def main(argv):
	opts, args = getopt.getopt(argv, "i:o:a:t:l:", ["csv=", "out=", "artist=", "type=", "list="])

	met_csv_file = ""
	out_dir = ""
	list_file = ""
	artists = []

	types = []

	for opt, arg in opts:
		if opt in ("--csv", "-i"):
			met_csv_file = arg
		elif opt in ("--out", "-o"):
			out_dir = arg
		elif opt in ("--artist", "-a"):
			artists = arg.split(':')
		elif opt in ("--type", "-t"):
			types = arg.split(":")
		elif opt in ("--list", "-l"):
			list_file = arg

	met_csv = csv.reader(open(met_csv_file, 'rb'), delimiter=',')

	csv_lines = match_lines(met_csv, artists, types, list_file)

	lines = 0
	for line in csv_lines:
		print(line[14] + " " + line[24] + " " + line[3])
		lines += 1

	print(lines)

	

	download_lines(csv_lines, out_dir, met_csv)

	


if __name__ == "__main__":
	main(sys.argv[1:])
