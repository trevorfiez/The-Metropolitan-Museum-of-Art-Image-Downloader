from __future__ import absolute_import
from __future__ import print_function
import urllib.request, urllib.error, urllib.parse
import sys
import getopt
import csv
import inspect
from datetime import datetime, date
from tqdm import tqdm
import os
import http.client
from selenium import webdriver

LINES_TO_DOWNLOAD = "lines_to_download_" + str(datetime.now()) + ".txt"
FAILED_URLS = "failed_urls_" + str(datetime.now()) + ".txt"

def check_artists(source_artist, user_request):
	if (len(user_request) == 0):
		return True
	else:
		for artist in user_request:
			if artist.lower() in source_artist.lower():
				return True
		return False

def check_types(source_type, user_request):
	if (len(user_request) == 0):
		return True
	else:
		for user_type in user_request:
			if user_type.lower() in source_type.lower():
				return True
		return False

def check_highlight(highlight, user_request):
	if user_request is None:
		return True
	if highlight == user_request:
		return True
	
	return False

def check_timeline(timeline, user_request):
	if user_request is None:
		return True
	if timeline == user_request:
		return True

	return False

def check_object_num(object_num, num_list):
	return object_num in num_list

def match_lines(met_csv, artists, types, list_file, is_highlight, is_timeline_work):
	""" Returns list of csv lines that the match the user request """

	print('{} Finding matching lines...'.format(str(datetime.now())))

	lines = []

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
			# Each function will return True if there is no user input
			if (
				check_artists(row[18], artists) and
				check_types(row[8], types) and
				check_highlight(row[1], is_highlight) and
				check_timeline(row[2], is_timeline_work)
			):
				lines.append(row)

	return lines
	

def download_lines(lines, out_dir, met_csv):
    # Log file is used to log errors
    failed_log_location = out_dir + FAILED_URLS if out_dir.endswith("/") else out_dir + "/" + FAILED_URLS
    with open(failed_log_location, mode="a") as log_file:
        # Note: you will need geckodriver.
        # See https://pypi.org/project/selenium.
        print('{} Launching selenium webdriver...'.format(str(datetime.now())))
        driver = webdriver.Firefox()
        for line in tqdm(lines):
            res = ""
            try:
            	# The URL to the image is the CSV file (Link Resource)
                driver.get(line[47].strip())
                html = driver.page_source
            except urllib.error.URLError as e:
            	log_file.write("URL error, original url: " + str(line[47].strip()) + "\n" + str(e) + "\n\n")
            	continue

            offset = html.find("artwork__interaction artwork__interaction--download")

            if (offset == -1):
                image_names.append(None)
                continue
            offset = html[offset:].find('http') + offset
            end = html[offset:].find('.jpg') + offset + 4

            if (end - offset > 300):
            	log_file.write("URL error, original url: " + str(line[47].strip()) + "\n\n")
            	continue

            image_link = html[offset:end]

            image_name = image_link.split('/')[-1]

            # Compose file name based on name, type, date. If too long, cut from the beginning
            artist_name = line[18] or ""
            art_type = line[9] or ""
            file_name = artist_name + "_" + art_type + "_" + str(date.today()) + "_" + image_name
            while (len(file_name) > 250):
            	file_name = file_name[1:len(file_name)]

            image_path = os.path.join(out_dir, file_name)
            image_file = ""

            try:
                image_file = urllib.request.urlopen(image_link)
            except (urllib.error.URLError, http.client.InvalidURL, ValueError) as e:
            	log_file.write("URL error: " + str(image_link) + "\noriginal url: " + str(line[47].strip()) + "\n" + str(e) + "\n\n")
            	continue

            try:
            	# Not sure why this failed one time, but with this exception it will continue
            	with open(image_path, 'wb') as output:
            		output.write(image_file.read())
            except Exception as error:
                log_file.write("File saving error: " + str(image_path) + "\noriginal url: " + str(line[47].strip()) + "\n" + str(error) + "\n\n")
                continue

        driver.close()
    
    # Delete log file with errors if it's empty
    if os.path.getsize(failed_log_location) == 0:
        os.remove(failed_log_location)

def main(argv):
	print('\n\n{} Checking your arguments...'.format(str(datetime.now())))

	opts, args = getopt.getopt(argv, "i:o:a:t:l:h:w", ["csv=", "out=", "artist=", "type=", "list=", "is_highlight=", "is_timeline_work="])
	met_csv_file = ""
	out_dir = ""
	list_file = ""
	artists = []
	is_highlight = None
	is_timeline_work = None

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
		elif opt in ("--is_highlight", "-h"):
			is_highlight = arg
		elif opt in ("--is_timeline_work", "-w"):
			is_timeline_work = arg

	# Validations
	if met_csv_file == "": 
		print("Please specify the CSV file from the Met: --csv=Location\n")
		return
	if out_dir == "": 
		print("Please specify output location: --out=Location\n")
		return
	if not os.path.exists(out_dir):
		os.makedirs(out_dir)

	met_csv = csv.reader(open(met_csv_file, 'r+'), delimiter=',')

	csv_lines = match_lines(met_csv, artists, types, list_file, is_highlight, is_timeline_work)
	len_csv_lines = len(csv_lines)
	if len_csv_lines == 0:
		print("No lines matched.")
		return

	# Log all lines to be downloaded
	log_file_location = out_dir + LINES_TO_DOWNLOAD if out_dir.endswith("/") else out_dir + "/" + LINES_TO_DOWNLOAD
	with open(log_file_location, mode="a") as log_file:
		[log_file.write(str(line) + '\n') for line in csv_lines]

	print(str(datetime.now()) + " Number of lines to download: " + str(len_csv_lines) + '\n')

	download_lines(csv_lines, out_dir, met_csv)

	print('\n{} All done. Files saved into {}\n\n'.format(str(datetime.now()), out_dir))


if __name__ == "__main__":
	main(sys.argv[1:])
