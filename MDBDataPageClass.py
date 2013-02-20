# http://jabakobob.net/mdb/data-page.html

# TODO: There is a lot of 'general' code in here which is good
# but the class exists to extract version number and build number
# from Access Databases so conversely there is a lot of specific 
# code used to drill down to two memo fields within the page index.
# This needs reversing as time permits. 

import binascii
import struct
from MDBDefinitionMarkers import MDBDefinitionMarkers
from MDBDataPageMarkers import MDBDataPageMarkers

class MDBDataPageValidator:
	
	versionno = ''
	buildno = ''
	
	freespace = ''				# free space in page index
	numberOfRows = 0			# number of rows in page index

	def __init__(self, dbversion):
		self.dbversion = dbversion

	def handleMDBDataPage(self, buf):
	
		tabledef = 0
	
		if self.dbversion == MDBDefinitionMarkers.VJET4:
			if MDBDataPageMarkers.ACCESS2KVERSIONSTRING in binascii.hexlify(buf) or MDBDataPageMarkers.ACCESS97VERSIONSTRING in binascii.hexlify(buf):

				self.freespace = struct.unpack('<H', buf[MDBDataPageMarkers.FREESPACE : MDBDataPageMarkers.FREESPACE + MDBDataPageMarkers.FREESPACELEN])
				tabledef = buf[MDBDataPageMarkers.TDEF : MDBDataPageMarkers.TDEF + MDBDataPageMarkers.TDEFLEN]
				self.numberOfRows = struct.unpack('<H', buf[MDBDataPageMarkers.NOROWS2K : MDBDataPageMarkers.NOROWS2K + MDBDataPageMarkers.NOROWSLEN])[0]
			
				self.row_ptr = MDBDataPageMarkers.NOROWS2K + MDBDataPageMarkers.NOROWSLEN
		
		elif self.dbversion == MDBDefinitionMarkers.VJET3:
			if MDBDataPageMarkers.ACCESS97VERSIONSTRING in binascii.hexlify(buf):
				
				self.freespace = struct.unpack('<H', buf[MDBDataPageMarkers.FREESPACE : MDBDataPageMarkers.FREESPACE + MDBDataPageMarkers.FREESPACELEN])
				tabledef = buf[MDBDataPageMarkers.TDEF : MDBDataPageMarkers.TDEF + MDBDataPageMarkers.TDEFLEN]
				self.numberOfRows = struct.unpack('<H', buf[MDBDataPageMarkers.NOROWS97 : MDBDataPageMarkers.NOROWS97 + MDBDataPageMarkers.NOROWSLEN])[0]

				self.row_ptr = MDBDataPageMarkers.NOROWS97 + MDBDataPageMarkers.NOROWSLEN
			
		if tabledef == MDBDataPageMarkers.LONGVALUEPAGE:
			self.handleLongValuePage(buf)

	def handleLongValuePage(self, buf):
	
		row_offsets = []
		for x in range(self.numberOfRows):
			val = struct.unpack('<H', buf[self.row_ptr : self.row_ptr + MDBDataPageMarkers.ROWSLEN])[0]
			if (val & 0x8000) == 0:		# high order bit used for flags: 0x8000: ignore
				row_offsets.append(val)
			self.row_ptr+=MDBDataPageMarkers.ROWSLEN
			
		self.__getMemoRowData__(row_offsets, buf)
	
	def __getMemoRowData__(self, row_offsets, buf):
		y = len(buf)				# rows are written from end of page, range x:y
		for x in row_offsets:
			row = buf[x : y]
			if row[0:4] == MDBDataPageMarkers.MEMOJET3:
				if MDBDataPageMarkers.ACCESS97VERSIONSTRING in binascii.hexlify(row):
					self.__readJet3MemoRow__(row)
			elif row[0:4] == MDBDataPageMarkers.MEMOJET4:
				if MDBDataPageMarkers.ACCESS2KVERSIONSTRING in binascii.hexlify(row):
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
		
		LENGTHTYPELEN = BLOCKLENLEN + BLOCKTYPELEN		# badname
		
		TDVALUEBLOCK  = 0x0000		# Table Property Value Block
		COLPROPBLOCK  = 0x0001		# Column Property Value Block
		PROPNAMEBLOCK = 0x0080		# Property Name Block
		
		namelen = struct.unpack('<I', row[BLOCKLENOFF : BLOCKLENOFF + BLOCKLENLEN])[0]
		blocktype = struct.unpack('<H', row[BLOCKTYPEOFF : BLOCKTYPEOFF + BLOCKTYPELEN])[0]
		
		NAMEOFF = BLOCKLENOFF + LENGTHTYPELEN
		NAMELEN = namelen - LENGTHTYPELEN
		
		namedata = row[NAMEOFF: NAMEOFF + NAMELEN]	# rest of block
		
		UNKNOWNOFF = BLOCKLENOFF + namelen
		VALUEOFF = (UNKNOWNOFF) + UNKNOWNLEN
		
		unknowndata = binascii.hexlify(row[UNKNOWNOFF : UNKNOWNOFF + UNKNOWNLEN]) # for debug
		valuedata = row[VALUEOFF : ]
		
		if blocktype == PROPNAMEBLOCK:		# Want interesting MS Access metadata : version, buildno
			
			namedatalen = len(namedata)
			valuedatalen = len(valuedata)
			
			index = 0
			while namedatalen > 0:
				namelen = struct.unpack('<H', namedata[MDBDataPageMarkers.ZEROOFF : MDBDataPageMarkers.SHORTVAL])[0]
				name = namedata[MDBDataPageMarkers.SHORTVAL : MDBDataPageMarkers.SHORTVAL + namelen]
				name = name.replace('\x00', '')										# for 2k databases
				namedataoff = MDBDataPageMarkers.SHORTVAL + namelen
				namedata = namedata[namedataoff : ]
				
				valuedatatemp = self.__getValue__(valuedata, index)
				valuedata = valuedatatemp[1]
				
				if name == 'AccessVersion':
					self.versiono = valuedatatemp[0]
				if name == 'Build':
					self.buildno = valuedatatemp[0]
				
				namedatalen = len(namedata)
				index+=1

	def __getValue__(self, valuedata, index):
	
		INDEXOFF    = MDBDataPageMarkers.SHORTVAL + MDBDataPageMarkers.SHORTVAL		# 2 bytes further along
		VALUELENOFF = INDEXOFF + MDBDataPageMarkers.SHORTVAL
		VALUEOFF    = VALUELENOFF + MDBDataPageMarkers.SHORTVAL
	
		partlen = struct.unpack('<H', valuedata[MDBDataPageMarkers.ZEROOFF : MDBDataPageMarkers.SHORTVAL])[0]	#length of block containing one value
		
		unknown = binascii.hexlify(valuedata[MDBDataPageMarkers.SHORTVAL])
		valuetype = ord(valuedata[MDBDataPageMarkers.SHORTVAL + 1 : MDBDataPageMarkers.SHORTVAL + 2])
		
		valueindex = struct.unpack('<H', valuedata[INDEXOFF : INDEXOFF + MDBDataPageMarkers.SHORTVAL])[0]
		valuelen = struct.unpack('<H', valuedata[VALUELENOFF : VALUELENOFF + MDBDataPageMarkers.SHORTVAL])[0]

		if valueindex == index:
			if valuetype == MDBDataPageMarkers.TEXT:
				value = valuedata[VALUEOFF : VALUEOFF + valuelen].replace('\x00', '')
			elif valuetype == MDBDataPageMarkers.LONGINT:
				value = str(struct.unpack('<I', valuedata[VALUEOFF : VALUEOFF + valuelen])[0])
			elif valuetype == MDBDataPageMarkers.BOOL:
				value = str(struct.unpack('?', valuedata[VALUEOFF : VALUEOFF + valuelen])[0])				
			else:
				value = "Unknown type: " + str(valuetype)
			valuedata = valuedata[VALUEOFF + valuelen : ]		# value, remaining value data pair
		else:	
			value = "Not set"
			valuedata = valuedata
			
		return [value, valuedata]		# value, remaining value data pair

