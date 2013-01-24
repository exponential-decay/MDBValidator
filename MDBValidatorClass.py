# http://www.fdrlab.com/files/accessfileformat.txt
# http://www.e-tech.ca/001-AccessFileFormat.asp
# http://jabakobob.net/mdb/data-page.html
# https://github.com/brianb/mdbtools/blob/master/HACKING
# http://jabakobob.net/mdb/first-page.html

import os
import sys
import struct
import binascii
from MDBMarkers import MDBMarkers
from time import strftime, gmtime

class MDBValidator:

	dbfile = ''
	dbpath = ''
	dbsize = ''
		
	pagesize = ''	# if zero: exit()

	def __init__(self, dbpath):
		if os.path.isfile(dbpath):
			self.dbfile = open(dbpath, "r+b")
			self.dbpath = dbpath
		else:
			self.__stderr__("Database does not exist or path isn't valid: " + dbpath)
	
	def dbLoaded(self):
		if self.dbfile is not '':
			return True
	
	def returnFileSystemMetadata(self):
		stats = os.stat(self.dbpath)

		self.__stdout__("")

		self.__fmttime__("Created : ", stats.st_ctime)	#created
		self.__fmttime__("Modified: ", stats.st_mtime)	#modified
		self.__fmttime__("Accessed: ", stats.st_atime)	#accessed
		
		self.__stdout__("")
		
		self.__stdout__("Filesize: " + str(os.path.getsize(self.dbpath)) + " bytes")

		self.__stdout__("")
	
	def handleDBDefinition(self):
		versionheader = self.dbfile.read(MDBMarkers.MDB_VERSION_HEADER_LEN)
		self.dbfile.seek(MDBMarkers.MDB_BOF)
		
		self.__getMagic__(versionheader)
		self.__getJetText__(versionheader)
		self.__getDBVersion__(versionheader)
	
	def __getMagic__(self, versionheader):
		self.__stdout__("Magic:     " + hex(struct.unpack('<I', versionheader[MDBMarkers.MAGIC_OFF:MDBMarkers.MAGIC_LEN])[0]))
		
	def __getJetText__(self, versionheader):
		self.__stdout__("Format ID: " + versionheader[MDBMarkers.FORMAT_ID_OFF : MDBMarkers.FORMAT_ID_OFF + MDBMarkers.FORMAT_ID_LEN])
	
	def __getDBVersion__(self, versionheader):
		version = versionheader[MDBMarkers.MDB_VERSION_OFFSET]
		versiontext = MDBMarkers.JETVER.get(ord(version), MDBMarkers.NOID)
		
		if versiontext == MDBMarkers.NOID:
			self.__stdout__("Version: Unidentified JetDB version.")
		else:
			self.__stdout__("Version:   " + versiontext)
		self.__setPageSize__(version)	
			
	def __setPageSize__(self, version): 	# depends on 'version' set asap
		if version == MDBMarkers.NOID:
			self.pagesize = MDBMarkers.PAGESIZEZERO
		elif version == MDBMarkers.JET3:
			self.pagesize == MDBMarkers.JET3PAGESIZE
		elif version >= MDBMarkers.JET4:
			self.pagesize == MDBMarkers.JET4PAGESIZE
	
	def __fmttime__(self, msg, time):
		sys.stdout.write(strftime(msg + "%a, %d %b %Y %H:%M:%S +0000" + "\n", gmtime(time)))
	
	def __stdout__(self, msg):
		sys.stdout.write(msg + "\n")
	
	def __stderr__(self, msg):
		sys.stderr.write(msg + "\n")
		
	def __del__(self):
		if self.dbfile is not '':
			self.dbfile.close()