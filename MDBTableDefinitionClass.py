import binascii
import struct

class MDBTableDefinitionValidator:

	IDOFF = 0x02
	IDLEN = 0x02

	tdef_id = ''

	DEFBLOCKOFF = 0x08
	DEFBLOCKLEN97 = 0x23
	DEFBLOCKLEN2K = 0x37

	def __init__(self):
		c = 'do nothing'
		
	def handleMDBTableDefinition(self, buf):
	
		self.tdef_id = binascii.hexlify(buf[self.IDOFF : self.IDOFF + self.IDLEN])		
		tddefblock = buf[self.DEFBLOCKOFF : self.DEFBLOCKOFF + self.DEFBLOCKLEN97]
		tdtype = binascii.hexlify(tddefblock[0xC])

	def __write2file__(self, name, buf):
		f = open(name, 'w+b')
		f.write(buf)
		f.close()