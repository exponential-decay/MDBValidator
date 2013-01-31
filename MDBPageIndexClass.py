# http://jabakobob.net/mdb/data-page.html

import binascii
import struct

class MDBPageIndexValidator:

	ACCESS2KVERSIONSTRING = "410063006300650073007300560065007200730069006f006e"
	ACCESS97VERSIONSTRING = "41636365737356657273696f6e"
	
	FREESPACE = 0x02
	FREESPACELEN = 0x02

	TDEF = 0x04
	TDEFLEN = 0x04
	
	NOROWS97  = 0x08
	NOROWS2K = 0x0C
	
	NOROWSLEN = 0x02	
	ROWSLEN = 0x02
	
	freespace = ''
	rows = 0

	def handleMDBPageIndex(self, buf):
	
		tabledef = 0
	
		if self.ACCESS2KVERSIONSTRING in binascii.hexlify(buf) or self.ACCESS97VERSIONSTRING in binascii.hexlify(buf):
			self.__write2file__('ver.bin', buf)
			
			self.freespace = struct.unpack('<H', buf[self.FREESPACE : self.FREESPACE + self.FREESPACELEN])
			tabledef = buf[self.TDEF : self.TDEF + self.TDEFLEN]
			self.rows = struct.unpack('<H', buf[self.NOROWS2K : self.NOROWS2K + self.NOROWSLEN])[0]
		
			self.row_ptr = self.NOROWS2K + self.NOROWSLEN
		
		if self.ACCESS97VERSIONSTRING in binascii.hexlify(buf):
			self.__write2file__('ver.bin', buf)
			
			self.freespace = struct.unpack('<H', buf[self.FREESPACE : self.FREESPACE + self.FREESPACELEN])
			tabledef = buf[self.TDEF : self.TDEF + self.TDEFLEN]
			self.rows = struct.unpack('<H', buf[self.NOROWS97 : self.NOROWS97 + self.NOROWSLEN])[0]

			self.row_ptr = self.NOROWS97 + self.NOROWSLEN
			
		if tabledef == "LVAL":
			self.handleLVAL(buf)

	def handleLVAL(self, buf):
		row_offs = []
		for x in range(self.rows):
			#print binascii.hexlify(buf[self.row_ptr : self.row_ptr + self.ROWSLEN])
			val = struct.unpack('<H', buf[self.row_ptr : self.row_ptr + self.ROWSLEN])[0]
			
			if (val & 0x8000) == 0:		# high order bit used for flags: 0x8000: ignore
				row_offs.append(val)

			self.row_ptr+=self.ROWSLEN
			
		self.__getRowData__(row_offs, buf)
			
	def __getRowData__(self, row_offs, buf):
		y = len(buf)				# rows are written from end of page, range x:y
		for x in row_offs:
			print binascii.hexlify(buf[x : y])	# print for now
			print " " 
			y = x

	def __write2file__(self, name, buf):
		f = open(name, 'w+b')
		f.write(buf)
		f.close()
	
