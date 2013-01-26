class MDBMarkers:
	
	MDB_BOF = 0x00
	MDB_VERSION_OFFSET = 0x14
	
	MDB_DEFINITION_LEN = 0x255	# length which contains the data we need
	
	# Internal byte values
	JET3 = 0x00	# Access 97
	JET4 = 0x01	# Access 2000/2002
	JET5 = 0x02 # Unknown
	JETX = 0x03	# Unknown
	
	NOID = -1	# Error for an unidentified version
	
	JETVER = {JET3 : "Jet 3, Access 97", JET4 : "Jet 4, Access 2000/2002", JET5 : "Jet 5, Unknown", JETX : "Jet Unknown, Unknown"}
	
	# Validator versions
	VJETUNKNOWN = 0x00
	VJET3 = 0x03
	VJET4 = 0x04
	
	# Page sizes
	JET3PAGESIZE = 2048
	JET4PAGESIZE = 4096
	
	# Global passwords
	# Already little endian : Opposite to what would be found in std hex stream
	mdb97pwd = [0x86, 0xFB, 0xEC, 0x37, 0x5D, 0x44, 0x9C, 0xFA, 0xC6, 0x5E, 0x28, 0xE6, 0x13, 0xB6, 0x8A, 0x60, 0x54, 0x94]
	mdb2000pwd = [0x6ABA, 0x37EC, 0xD561, 0xFA9C, 0xCFFA, 0xE628, 0x272F, 0x608A, 0x568, 0x367B, 0xE3C9, 0xB1DF, 0x654B, 0x4313, 0x3EF3, 0x33B1, 0xF008, 0x5B79, 0x24AE, 0x2A7C]
	mdb2000xormask = mdb2000pwd[18]
	
	# Password offset
	PWDOFFSET = 0x42
	
	# Password length
	JET3PWDLEN = 20
	JET4PWDLEN = 40
	
	# MDB2000 Keys
	PWDKEYOFFSET = 0x66		# KEY WHICH MASKS PASSWORD MAY BE DAYS SINCE 1900
	PWDKEYLEN = 2				# SHORT AS OPPOSED TO A DOUBLE AS IN SOME DOCS
	
	# Magic number offset and length
	MAGIC_OFF = 0x00
	MAGIC_LEN = 4
	
	# Format ID offset and length
	FORMAT_ID_OFF = 0x04	
	FORMAT_ID_LEN = 16
	
	# UNUSED Plain Text Format ID [0x04 : 0x14]:
	# MDB format (Access 97-2003): "Standard Jet DB"
	# ACCDB format (Access 2007-2010): "Standard ACE DB"