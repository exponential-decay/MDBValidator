# http://www.fdrlab.com/files/accessfileformat.txt
# http://www.e-tech.ca/001-AccessFileFormat.asp
# http://jabakobob.net/mdb/data-page.html
# https://github.com/brianb/mdbtools/blob/master/HACKING
# http://jabakobob.net/mdb/first-page.html

import os
import sys
import struct
import binascii
from MDBDefinitionMarkers import MDBDefinitionMarkers
from time import strftime, gmtime
from operator import xor

class MDBDefinitionValidator:

	dbfile = ''	# File pointer
	dbpath = ''	# File path
	dbsize = ''	# Size of database @ dbpath
	
	magic = ''
	formatid = ''
	versiontext = ''
	
	dbversion = '' # if zero: exit()
	dbpagesize = ''	
	
	dbpwd = ''
	
	t_codepage = ''
	t_db_key = ''
	t_creationdate = ''

	def __init__(self, dbpath):
		if os.path.isfile(dbpath):
			self.dbfile = open(dbpath, "r+b")
			self.dbpath = dbpath
			self.stats = os.stat(self.dbpath)
		else:
			self.__stderr__("Database does not exist or path isn't valid: " + dbpath)
	
	def dbLoaded(self):
		if self.dbfile is not '':
			return True

	def handleDBDefinition(self):
		versionheader = self.dbfile.read(MDBDefinitionMarkers.MDB_DEFINITION_LEN)
		self.dbfile.seek(MDBDefinitionMarkers.MDB_BOF)
		
		self.__setMagic__(versionheader)
		self.__setJetVersion__(versionheader)
		self.__setDBVersion__(versionheader)
		self.__setPWD__(versionheader)
		self.__setAdditionalFields__(versionheader)
		
		self.__getDBDefinitionObjectData__()
	
	def __setMagic__(self, versionheader):
		self.magic = hex(struct.unpack('<I', versionheader[MDBDefinitionMarkers.MAGIC_OFF:MDBDefinitionMarkers.MAGIC_LEN])[0])
		
	def __setJetVersion__(self, versionheader):
		self.formatid = versionheader[MDBDefinitionMarkers.FORMAT_ID_OFF : MDBDefinitionMarkers.FORMAT_ID_OFF + MDBDefinitionMarkers.FORMAT_ID_LEN]
	
	def __setDBVersion__(self, versionheader):
		version = ord(versionheader[MDBDefinitionMarkers.MDB_VERSION_OFFSET])
		
		if version == MDBDefinitionMarkers.JET3:
			self.dbversion = MDBDefinitionMarkers.VJET3
		elif version >= MDBDefinitionMarkers.JET4:
			self.dbversion >= MDBDefinitionMarkers.VJET4
		else:
			self.dbversion = MDBDefinitionMarkers.VJETUNKNOWN
			
		self.versiontext = MDBDefinitionMarkers.JETVER.get(version, MDBDefinitionMarkers.NOID)
		
		self.__setPageSize__()	
		
	def __setPWD__(self, versionheader):
		if self.dbversion == MDBDefinitionMarkers.VJET3:			
			mdbPwdField = versionheader[MDBDefinitionMarkers.PWDOFFSET : MDBDefinitionMarkers.PWDOFFSET + MDBDefinitionMarkers.JET3PWDLEN]
			i = 0
			for x in MDBDefinitionMarkers.mdb97pwd:
				self.dbpwd = self.dbpwd + chr(xor(x, ord(mdbPwdField[i])))
				i+=1
			
		elif self.dbversion >= MDBDefinitionMarkers.VJET4:
			mdbPwdField = versionheader[MDBDefinitionMarkers.PWDOFFSET : MDBDefinitionMarkers.PWDOFFSET + MDBDefinitionMarkers.JET4PWDLEN]
			mdb2000key = struct.unpack('<H', versionheader[MDBDefinitionMarkers.PWDKEYOFFSET : MDBDefinitionMarkers.PWDKEYOFFSET + MDBDefinitionMarkers.PWDKEYLEN])[0]
			mdbKey = xor(MDBDefinitionMarkers.mdb2000xormask, mdb2000key)
						
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
			for defaultVal in MDBDefinitionMarkers.mdb2000pwd:
				val = xor(defaultVal, pwdlist[i])
				if val < 256:
					self.dbpwd = self.dbpwd + chr(val)
				else:
					self.dbpwd = self.dbpwd + chr(xor(val, mdbKey))
				i+=1
				
		if binascii.hexlify(self.dbpwd[0]) == '00':
			self.dbpwd = "Null"
			
	def __setAdditionalFields__(self, versionheader):
		self.t_codepage = binascii.hexlify(versionheader[MDBDefinitionMarkers.CODE_PAGE_OFF : MDBDefinitionMarkers.CODE_PAGE_OFF + MDBDefinitionMarkers.CODE_PAGE_LEN])
		self.t_dbkey = binascii.hexlify(versionheader[MDBDefinitionMarkers.KEY_OFFSET : MDBDefinitionMarkers.KEY_OFFSET + MDBDefinitionMarkers.KEY_LEN])
		self.t_creationdate = binascii.hexlify(versionheader[MDBDefinitionMarkers.DATE_OFF : MDBDefinitionMarkers.DATE_OFF + MDBDefinitionMarkers.DATE_LEN]) 

	def __returnFileSystemMetadata__(self):
		self.__stdout__("")
		self.__fmttime__("Created : ", self.stats.st_ctime)	#created
		self.__fmttime__("Modified: ", self.stats.st_mtime)	#modified
		self.__fmttime__("Accessed: ", self.stats.st_atime)	#accessed
		self.__stdout__("")
		self.__stdout__("Filesize: " + str(os.path.getsize(self.dbpath)) + " bytes")
		self.__stdout__("")

	def __getDBDefinitionObjectData__(self):
		self.__returnFileSystemMetadata__()
	
		self.__stdout__("Magic:     " + self.magic)
		self.__stdout__("Format ID: " + self.formatid)

		if self.versiontext == MDBDefinitionMarkers.NOID:
			self.__stdout__("Version: Unidentified JetDB version.")
		else:
			self.__stdout__("Version:   " + self.versiontext)
		
		self.__stdout__("")
		self.__stdout__("Password: " + self.dbpwd)
	
		self.__stdout__('')
		self.__stdout__('These fields are yet to be decoded correctly:')
		self.__stdout__('---')
		self.__stdout__("Code page    : " + self.t_codepage)
		self.__stdout__("DB key       : " + self.t_dbkey)
		self.__stdout__("Creation Date: " + self.t_creationdate) 
			
	def __setPageSize__(self):
		if self.dbversion == MDBDefinitionMarkers.VJET3:
			self.dbpagesize = MDBDefinitionMarkers.JET3PAGESIZE
		elif self.dbversion >= MDBDefinitionMarkers.VJET4:
			self.dbpagesize = MDBDefinitionMarkers.JET4PAGESIZE
		
	def __fmttime__(self, msg, time):
		sys.stdout.write(strftime(msg + "%a, %d %b %Y %H:%M:%S +0000" + "\n", gmtime(time)))
	
	def __stdout__(self, msg):
		sys.stdout.write(msg + "\n")
	
	def __stderr__(self, msg):
		sys.stderr.write(msg + "\n")
		
	def __del__(self):
		if self.dbfile is not '':
			self.dbfile.close()