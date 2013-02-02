import binascii
import struct

class MDBTableDefinitionValidator:

	IDOFF = 0x02
	IDLEN = 0x02

	tdef_id = ''
	tdtype = ''

	DEFBLOCKOFF = 0x08			# table definition offset
	DEFBLOCKLEN97 = 0x23			# table definition length 97
	DEFBLOCKLEN2K = 0x37			# table definition length 2k
		
	def handleMDBTableDefinition(self, buf):
	
		self.tdef_id = binascii.hexlify(buf[self.IDOFF : self.IDOFF + self.IDLEN])		
		tddefblock = buf[self.DEFBLOCKOFF : self.DEFBLOCKOFF + self.DEFBLOCKLEN97]
		self.tdtype = binascii.hexlify(tddefblock[0xC])