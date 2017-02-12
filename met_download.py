


import urllib2
import sys
import getopt
import csv
import os


#returns list of csv lines that the artist matches
def match_artist(met_csv, artist):
	lines = []

	for row in met_csv:
		if (row[14] == artist):
			lines.append(row)

	return lines
	

def download_lines(lines, out_dir):
	image_names = []

	if not os.path.exists(out_dir):
		os.path.makedirs(out_dir)
	
	for line in lines:
		res = urllib2.urlopen('http://www.metmuseum.org/art/collection/search/' + str(line[3]))
		html = res.read()

		offset = html.find("utility-menu__item utility-menu__item--download")
		offset = html[offset:].find('http') + offset
		end = html[offset:].find('.jpg') + offset + 4

		image_link = html[offset:end]

		image_name = image_link.split('/')[-1]

		image_path = os.path.join(out_dir, image_name)

		image_file = urllib2.urlopen(image_link)

		with open(image_path, 'wb') as output:
			output.write(image_file.read())

		image_names.append(image_path)

		print(image_link)

	return image_names
		

def main(argv):
	opts, args = getopt.getopt(argv, "i:o:a:", ["csv=", "out=", "artist="])

	met_csv_file = ""
	out_dir = ""
	artist = ""

	for opt, arg in opts:
		if opt in ("--csv", "-i"):
			met_csv_file = arg
		elif opt in ("--out", "-o"):
			out_dir = arg
		elif opt in ("--artist", "-a"):
			artist = arg

	met_csv = csv.reader(open(met_csv_file, 'rb'), delimiter=',')

	csv_lines = match_artist(met_csv, artist)

	painting_names = download_lines(csv_lines, out_dir)

	with open(os.path.join(out_dir, "piece_info.csv"), 'wb') as csv_file:
		im_writer = csv.writer(csv_file, delimiter=',')

		for row in met_csv:
			im_writer.writerow(row + ['Image Location'])
			break

		for i, row in enumerate(csv_lines):
			im_writer.writerow(row + [painting_names[i]])

	return


if __name__ == "__main__":
	main(sys.argv[1:])
