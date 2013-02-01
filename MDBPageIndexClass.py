# http://jabakobob.net/mdb/data-page.html

import binascii
import struct
from MDBDefinitionMarkers import MDBDefinitionMarkers

class MDBPageIndexValidator:

	ACCESS2KVERSIONSTRING = "410063006300650073007300560065007200730069006f006e"
	ACCESS97VERSIONSTRING = "41636365737356657273696f6e"
	
	MEMOJET3 = '\x4B\x4B\x44\x00'
	MEMOJET4 = '\x4D\x52\x32\x00'
	
	FREESPACE = 0x02
	FREESPACELEN = 0x02

	TDEF = 0x04
	TDEFLEN = 0x04
	
	NOROWS97  = 0x08
	NOROWS2K = 0x0C
	
	NOROWSLEN = 0x02	
	ROWSLEN = 0x02
	
	LONGVALUEPAGE = "LVAL"
	
	freespace = ''
	numberOfRows = 0

	def __init__(self, dbversion):
		self.dbversion = dbversion

	def handleMDBPageIndex(self, buf):
	
		tabledef = 0
	
		if self.dbversion == MDBDefinitionMarkers.VJET4:
			if self.ACCESS2KVERSIONSTRING in binascii.hexlify(buf) or self.ACCESS97VERSIONSTRING in binascii.hexlify(buf):
				self.__write2file__('ver.bin', buf)
				
				self.freespace = struct.unpack('<H', buf[self.FREESPACE : self.FREESPACE + self.FREESPACELEN])
				tabledef = buf[self.TDEF : self.TDEF + self.TDEFLEN]
				self.numberOfRows = struct.unpack('<H', buf[self.NOROWS2K : self.NOROWS2K + self.NOROWSLEN])[0]
			
				self.row_ptr = self.NOROWS2K + self.NOROWSLEN
		
		elif self.dbversion == MDBDefinitionMarkers.VJET3:
			if self.ACCESS97VERSIONSTRING in binascii.hexlify(buf):
				self.__write2file__('ver.bin', buf)
				
				self.freespace = struct.unpack('<H', buf[self.FREESPACE : self.FREESPACE + self.FREESPACELEN])
				tabledef = buf[self.TDEF : self.TDEF + self.TDEFLEN]
				self.numberOfRows = struct.unpack('<H', buf[self.NOROWS97 : self.NOROWS97 + self.NOROWSLEN])[0]

				self.row_ptr = self.NOROWS97 + self.NOROWSLEN
			
		if tabledef == self.LONGVALUEPAGE:
			self.handleLongValuePage(buf)

	def handleLongValuePage(self, buf):
	
		row_offsets = []
		for x in range(self.numberOfRows):
			val = struct.unpack('<H', buf[self.row_ptr : self.row_ptr + self.ROWSLEN])[0]
			if (val & 0x8000) == 0:		# high order bit used for flags: 0x8000: ignore
				row_offsets.append(val)
			self.row_ptr+=self.ROWSLEN
			
		self.__getMemoRowData__(row_offsets, buf)
	
	#http://jabakobob.net/mdb/lvprop.html
	
	def __getMemoRowData__(self, row_offsets, buf):
		y = len(buf)				# rows are written from end of page, range x:y
		for x in row_offsets:
			row = buf[x : y]
			if row[0:4] == self.MEMOJET3:
				if self.ACCESS97VERSIONSTRING in binascii.hexlify(row):
					self.__readJet3MemoRow__(row)
			elif row[0:4] == self.MEMOJET4:
				if self.ACCESS2KVERSIONSTRING in binascii.hexlify(row):
					self.__readJet4MemoRow__(row)
			y = x

	def __readJet3MemoRow__(self, row):
		self.__readMemoHeader__(row)

	def __readJet4MemoRow__(self, row):
		self.__readMemoHeader__(row)
		
	def __readMemoHeader__(self, row):			# handles JET3 and JET4
		
		UNKNOWNLEN = 12
		
		BLOCKLENOFF = 0x04
		BLOCKLENLEN = 0x04
		
		BLOCKTYPEOFF = 0x08
		BLOCKTYPELEN = 0x02
		
		TDVALUEBLOCK  = 0x0000		# Table Property Value Block
		COLPROPBLOCK  = 0x0001		# Column Property Value Block
		PROPNAMEBLOCK = 0x0080		# Property Name Block
		
		blocklen = struct.unpack('<I', row[BLOCKLENOFF : BLOCKLENOFF + BLOCKLENLEN])[0]
		blocktype = struct.unpack('<H', row[BLOCKTYPEOFF : BLOCKTYPEOFF + BLOCKTYPELEN])[0]
		
		namedata = row[BLOCKLENOFF : BLOCKLENOFF + blocklen]	# rest of block
		
		UNKNOWNOFF = BLOCKLENOFF + blocklen
		VALUEOFF = (UNKNOWNOFF) + UNKNOWNLEN
		
		unknowndata = binascii.hexlify(row[UNKNOWNOFF : UNKNOWNOFF + UNKNOWNLEN]) # for debug
		valuedata = row[VALUEOFF : ]
		
		if blocktype == PROPNAMEBLOCK:		# Want interesting MS Access metadata : version, buildno
			print "Namedata: " + binascii.hexlify(namedata)
			print "Valuedata: " + binascii.hexlify(valuedata) 
			print "Unknodndata: " + unknowndata
	def __write2file__(self, name, buf):
		f = open(name, 'w+b')
		f.write(buf)
		f.close()
	
