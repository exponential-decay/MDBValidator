# TODO: Should become MDBValidatorClass rather than main()

# http://www.fdrlab.com/files/accessfileformat.txt
# http://www.e-tech.ca/001-AccessFileFormat.asp
# http://jabakobob.net/mdb/data-page.html
# https://github.com/brianb/mdbtools/blob/master/HACKING
# http://jabakobob.net/mdb/first-page.html

import sys
import argparse
import binascii
from MDBDefinitionClass import MDBDefinitionValidator
from MDBPageIndexClass import MDBPageIndexValidator
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
			self.expectedpages = self.db.dbfilesize / self.db.dbpagesize
		else:
			# TODO: Can't have this here. File handling needs to go somewhere
			# and then be fed into the supporting classes. Need to figure out
			# pattern for doing this.
			sys.exit(66)	# sysexits.h - EX_NOINPUT
			
	def validateMDB(self):
				
		self.db.dbfile.seek(0)
		
		i = 0
		while self.db.dbfile.tell() < self.db.dbfilesize:
			buf = self.db.dbfile.read(self.db.dbpagesize)
			
			type = ord(buf[0])
			
			if type in MDBValidatorMarkers.DBPAGEINDEX:
				self.updatecount(type)
				
				#TODO:
				#if type == MDBValidatorMarkers.DBDEFINITION:
				
				if type == MDBValidatorMarkers.DBDATAPAGE:
					mdbPI = MDBPageIndexValidator()
					#mdbPI.handleMDBPageIndex(buf)	
					
				#Properties
				#----------
				#Design View table definitions are stored in LvProp column of MSysObjects as OLE
				#fields. They contain default values, description, format, required ...
				elif type == MDBValidatorMarkers.DBTABLEDEFINITION:
				
					if i == MDBValidatorMarkers.MSYSOBJECTSPAGE:		# want MSysObjects
						mdbTDEF = MDBTableDefinitionValidator()
						mdbTDEF.handleMDBTableDefinition(buf)
					
				#TODO:
				#elif type == MDBValidatorMarkers.DBINTERINDEXPAGE:
				#elif type == MDBValidatorMarkers.DBLEAFINDEXPAGE:
				#elif type == MDBValidatorMarkers.DBPAGEUSAGEBMP:
				#elif type == MDBValidatorMarkers.DBPAGENOID: 
			else:
				self.updatecount(-1)

			i+=1
		
		# Write to stdout...
		# self.db.outputObjectData()
		# self.outputObjectData()

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
		mdbUC = MDBUtilityClass()

		x = MDBValidatorMarkers.DBPAGEINDEX.itervalues()
		mdbUC.__stdout__("")
		mdbUC.__stdout__("Page count")
		mdbUC.__stdout__("---")
		
		count = 0
		for v in x:
			c = MDBValidatorMarkers.DBPAGECOUNT.get(v)
			count = count + c
			mdbUC.__stdout__(MDBValidatorMarkers.DBPAGETYPE.get(v) + ": " + str(c))
		
		mdbUC.__stdout__("---")
		mdbUC.__stdout__("Total: " + str(count)) 





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
	mdbVC.validateMDB()
		
if __name__ == "__main__":
	main()