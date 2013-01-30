# http://www.fdrlab.com/files/accessfileformat.txt
# http://www.e-tech.ca/001-AccessFileFormat.asp
# http://jabakobob.net/mdb/data-page.html
# https://github.com/brianb/mdbtools/blob/master/HACKING
# http://jabakobob.net/mdb/first-page.html

import sys
import argparse
from MDBDefinitionClass import MDBDefinitionValidator

def parseArguments():
	parser = argparse.ArgumentParser(description='Validate MDB files.')
	parser.add_argument('--mdb', help='Optional: Single JPEG2000 image to read.')

	if len(sys.argv)==1:
		parser.print_help()
		sys.exit(1)
		
	args = parser.parse_args()
		
	return args

def main():
	args = parseArguments()
	db = MDBDefinitionValidator(args.mdb)
	if db.dbLoaded() is True:
		db.handleDBDefinition()
	else:
		sys.exit(66)	# sysexits.h - EX_NOINPUT
		
if __name__ == "__main__":
	main()