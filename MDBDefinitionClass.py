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
from operator import xor

class MDBValidator:

	dbfile = ''	# File pointer
	dbpath = ''	# File path
	dbsize = ''	# Size of database @ dbpath
	
	dbversion = '' # if zero: exit()
	pagesize  = ''	

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
		versionheader = self.dbfile.read(MDBMarkers.MDB_DEFINITION_LEN)
		self.dbfile.seek(MDBMarkers.MDB_BOF)
		
		self.__getMagic__(versionheader)
		self.__getJetText__(versionheader)
		self.__getDBVersion__(versionheader)
		
		self.__getPWD__(versionheader)
		
		self.__getAdditionalFields__(versionheader)
	
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
			
		self.__setVersion__(version)
		self.__setPageSize__()	
			
	def __getPWD__(self, versionheader):
		if self.dbversion == MDBMarkers.VJET3:
			self.__stderr__("Unable to handle JET3 at present.")
		elif self.dbversion >= MDBMarkers.VJET4:
			mdbPwdField = versionheader[MDBMarkers.PWDOFFSET : MDBMarkers.PWDOFFSET + MDBMarkers.JET4PWDLEN]
			mdb2000key = struct.unpack('<H', versionheader[MDBMarkers.PWDKEYOFFSET : MDBMarkers.PWDKEYOFFSET + MDBMarkers.PWDKEYLEN])[0]
			mdbKey = xor(MDBMarkers.mdb2000xormask, mdb2000key)
						
			# Convert password field to little endian shorts
			i = 0
			pwdlist = []
			while i < len(mdbPwdField):
				var = mdbPwdField[i:i+2]
				pwdlist.append(struct.unpack('<H', var)[0])	# also like var[:2][::-1] syntax
				i+=2

			# XOR Password field with default password field and then further XOR w/
			# mask which varies with each database (db creation date as short?)
			i = 0
			pwd = ''
			for defaultVal in MDBMarkers.mdb2000pwd:
				val = xor(defaultVal, pwdlist[i])
				if val < 256:
					pwd = pwd + chr(val)
				else:
					pwd = pwd + chr(xor(val, mdbKey))
				i+=1
			
			self.__stdout__("")
			
			if binascii.hexlify(pwd[0]) == '00':
				pwd = "Null"
				
			self.__stdout__("Password: " + pwd)

	def __getAdditionalFields__(self, versionheader):
		self.__stdout__('')
		self.__stdout__('These fields are yet to be decoded correctly:')
		self.__stdout__('---')
		self.__stdout__("Code page [beta]    : " + binascii.hexlify(versionheader[MDBMarkers.CODE_PAGE_OFF : MDBMarkers.CODE_PAGE_OFF + MDBMarkers.CODE_PAGE_LEN]))
		self.__stdout__("DB key [beta]       : " + binascii.hexlify(versionheader[MDBMarkers.KEY_OFFSET : MDBMarkers.KEY_OFFSET + MDBMarkers.KEY_LEN]))
		self.__stdout__("Creation Date [beta]: " + binascii.hexlify(versionheader[MDBMarkers.DATE_OFF : MDBMarkers.DATE_OFF + MDBMarkers.DATE_LEN])) 
	
	def __setVersion__(self, version):	
		if version == MDBMarkers.NOID:
			self.pagesize = MDBMarkers.VJETUNKNOWN
		elif version == MDBMarkers.JET3:
			self.dbversion == MDBMarkers.VJET3
		elif version >= MDBMarkers.JET4:
			self.dbversion >= MDBMarkers.VJET4
			
	def __setPageSize__(self):
		if self.dbversion == MDBMarkers.VJET3:
			self.pagesize == MDBMarkers.JET3PAGESIZE
		elif self.dbversion >= MDBMarkers.VJET4:
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