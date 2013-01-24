class MDBMarkers:
	
	MDB_BOF = 0x00
	MDB_VERSION_OFFSET = 0x14
	MDB_VERSION_HEADER_LEN = 0x15 # 0x14 + 0x01
	
	DEFINITION_OFFSET = 128
	
	JET3 = 0x00	# Access 97
	JET4 = 0x01	# Access 2000/2002
	JET5 = 0x02
	JETX = 0x03	# Access 2010
	
	NOID = -1	# Error for an unidentified version
	
	JETVER = {JET3 : "Jet 3, Access 97", JET4 : "Jet 4, Access 2000/2002", JET5 : "Jet 5, Unknown", JETX : "Jet Unknown, Access 2010"}
	
	JET3PAGESIZE = 2048
	JET4PAGESIZE = 4096
	PAGESIZEZERO = 0
	
	MAGIC_OFF = 0x00
	MAGIC_LEN = 4
	
	FORMAT_ID_OFF = 0x04	
	FORMAT_ID_LEN = 16
	
	# UNUSED Plain Text Format ID [0x04 : 0x14]:
	# MDB format (Access 97-2003): "Standard Jet DB"
	# ACCDB format (Access 2007-2010): "Standard ACE DB"