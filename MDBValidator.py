# TODO: Should become MDBValidatorClass rather than main()

# http://www.fdrlab.com/files/accessfileformat.txt
# http://www.e-tech.ca/001-AccessFileFormat.asp
# http://jabakobob.net/mdb/data-page.html
# https://github.com/brianb/mdbtools/blob/master/HACKING
# http://jabakobob.net/mdb/first-page.html

import os
import sys
import argparse
import binascii
from MDBDefinitionClass import MDBDefinitionValidator
from MDBDataPageClass import MDBDataPageValidator
from MDBTableDefinitionClass import MDBTableDefinitionValidator
from MDBValidatorMarkers import MDBValidatorMarkers
from MDBUtilityClass import MDBUtilityClass

# MDBValidatorClass

class MDBValidatorClass:

	expectedpages = ''
	validsize = ''
	db = ''

	def __init__(self, mdb):
		self.mdb = mdb
		self.db = MDBDefinitionValidator(self.mdb)
		if self.db.processDBDefinition() is True:
			if (self.db.dbfilesize % self.db.dbpagesize) is 0:
				self.validsize = "True"
			else:
				self.validsize = "False"
		else:
			return 1
			
	def validateMDB(self):
				
		self.db.dbfile.seek(0)
		
		i = 0
		while self.db.dbfile.tell() < self.db.dbfilesize:
			buf = self.db.dbfile.read(self.db.dbpagesize)
			
			type = ord(buf[0])
			
			if type in MDBValidatorMarkers.DBPAGEINDEX:
				self.updatecount(type)
				
				if type == MDBValidatorMarkers.DBDATAPAGE:
					mdbDP = MDBDataPageValidator(self.db.dbversion)
					mdbDP.handleMDBDataPage(buf)	
					
				elif type == MDBValidatorMarkers.DBTABLEDEFINITION:
				
					if i == MDBValidatorMarkers.MSYSOBJECTSPAGE:		# want MSysObjects #from design view
						mdbTDEF = MDBTableDefinitionValidator()		# definitions table 2nd page of DB
						mdbTDEF.handleMDBTableDefinition(buf)
					
				#TODO:
				#if type == MDBValidatorMarkers.DBDEFINITION:
				#elif type == MDBValidatorMarkers.DBINTERINDEXPAGE:
				#elif type == MDBValidatorMarkers.DBLEAFINDEXPAGE:
				#elif type == MDBValidatorMarkers.DBPAGEUSAGEBMP:
				#elif type == MDBValidatorMarkers.DBPAGENOID: 

			else:
				self.updatecount(-1)

			i+=1
		
		# Write to stdout...
		#self.db.outputObjectData()
		self.outputObjectData()

	def updatecount(self, type):
		c = MDBValidatorMarkers.DBPAGECOUNT[type]
		c+=1
		MDBValidatorMarkers.DBPAGECOUNT[type] = c	

	def __writeAll2File__():
		doSomething = 0
		
		#for each object... (put all page objects into an array?)
			# object.__write2file__()
			# object.__write2file__()
			# object.__write2file__()
			# object.__write2file__()

	# Output code

	def outputObjectData(self):
		mdbutil = MDBUtilityClass()
		
		# File system metadata
		stats = os.stat(self.mdb)
		
		mdbutil.__stdout__("")
		mdbutil.__fmttime__("Created : ", stats.st_ctime)	#created
		mdbutil.__fmttime__("Modified: ", stats.st_mtime)	#modified
		mdbutil.__fmttime__("Accessed: ", stats.st_atime)	#accessed
		mdbutil.__stdout__("")
		mdbutil.__stdout__("Filesize: " + str(self.db.dbfilesize) + " bytes")
		mdbutil.__stdout__("")

		mdbutil.__stdout__("Magic:     " + self.db.magic)
		mdbutil.__stdout__("Format ID: " + self.db.formatid)

		mdbutil.__stdout__("Version:   " + self.db.versiontext)
		
		mdbutil.__stdout__("")
		mdbutil.__stdout__("Password: " + self.db.dbpwd)
	
		mdbutil.__stdout__('')
		mdbutil.__stdout__('These fields are yet to be decoded correctly:')
		mdbutil.__stdout__('---')
		mdbutil.__stdout__("Code page    : " + self.db.t_codepage)
		mdbutil.__stdout__("DB key       : " + self.db.t_dbkey)
		mdbutil.__stdout__("Creation Date: " + self.db.t_creationdate) 


		x = MDBValidatorMarkers.DBPAGEINDEX.itervalues()
		mdbutil.__stdout__("")
		mdbutil.__stdout__("Page count")
		mdbutil.__stdout__("---")
		
		count = 0
		for v in x:
			c = MDBValidatorMarkers.DBPAGECOUNT.get(v)
			count = count + c
			mdbutil.__stdout__(MDBValidatorMarkers.DBPAGETYPE.get(v) + ": " + str(c))
		
		expectedpages = self.db.dbfilesize / self.db.dbpagesize
		
		mdbutil.__stdout__("---")
		mdbutil.__stdout__("Total (count/expected): " + str(count) + " / " + str(expectedpages)) 
		
# main

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
	mdbVC = MDBValidatorClass(args.mdb)
	if mdbVC.validateMDB() == 0:
		sys.exit(0)
	else:
		sys.exit(1)	# TODO: see sysexits.h for exit codes
		
if __name__ == "__main__":
	main()