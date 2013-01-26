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
	
	# Password offset
	PWDOFFSET = 0x42
	PWDKEYOFFSET = 0x66		# KEY WHICH MASKS PASSWORD MAY BE DAYS SINCE 1900
	
	# Password length
	JET3PWDLEN = 20
	JET4PWDLEN = 40
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