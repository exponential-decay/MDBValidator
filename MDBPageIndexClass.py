import binascii

class MDBPageIndexValidator:

	ACCESS2KVERSIONSTRING = "410063006300650073007300560065007200730069006f006e"
	ACCESS97VERSIONSTRING = "41636365737356657273696f6e"

	def handleMDBPageIndex(self, pageindexbuffer):
		if self.ACCESS2KVERSIONSTRING in binascii.hexlify(pageindexbuffer):
			self.__write2file__('ver.bin', pageindexbuffer)
		if self.ACCESS97VERSIONSTRING in binascii.hexlify(pageindexbuffer):
			self.__write2file__('ver.bin', pageindexbuffer)
			
	def __write2file__(self, name, pageindexbuffer):
		f = open(name, 'w+b')
		f.write(pageindexbuffer)
		f.close()