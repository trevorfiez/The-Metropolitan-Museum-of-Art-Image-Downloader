


import urllib2
import sys
import getopt
import csv





#returns list of csv lines that the artist matches
def match_artist(met_csv, artist):
	lines = []

	for row in met_csv:
		if (row[14] == artist):
			lines.append(row)

	return lines
	






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

	print((met_csv_file, out_dir, artist))
	met_csv = csv.reader(open(met_csv_file, 'rb'), delimiter=',')

	'''
	for row in met_csv:
		for i in range(len(row)):
			print((i, row[i]))

		return
	'''
	csv_lines = match_artist(met_csv, artist)

	for line in csv_lines:
		print(csv_lines)

	return










if __name__ == "__main__":
	main(sys.argv[1:])
