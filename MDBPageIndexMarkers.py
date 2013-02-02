# https://raw.github.com/brianb/mdbtools/master/HACKING

class MDBPageIndexMarkers:

	# from https://raw.github.com/brianb/mdbtools/master/HACKING
	BOOL            = 0x01	# Boolean         ( 1 bit ) 
	BYTE            = 0x02  # Byte            ( 8 bits) 
	INT             = 0x03  # Integer         (16 bits) 
	LONGINT         = 0x04  # Long Integer    (32 bits) 
	MONEY           = 0x05  # Currency        (64 bits)
	FLOAT           = 0x06  # Single          (32 bits) 
	DOUBLE          = 0x07  # Double          (64 bits) 
	DATETIME        = 0x08 
	BINARY          = 0x09 
	TEXT            = 0x0A 
	OLE             = 0x0B 
	MEMO            = 0x0C 
	UNKNOWN_0D      = 0x0D
	UNKNOWN_0E      = 0x0E
	REPID           = 0x0F	# GUID
	NUMERIC         = 0x10	# Scaled decimal	(17 bytes)
	
	# Datatype sizes
	ZEROOFF = 0x00
	SHORTVAL = 0x02
	
	MEMOJET3 = '\x4B\x4B\x44\x00'		# memo id for jet3
	MEMOJET4 = '\x4D\x52\x32\x00'		# memo id for jet4
	
	FREESPACE = 0x02			# free space offset
	FREESPACELEN = 0x02		# free space length

	TDEF = 0x04					# table definition offset
	TDEFLEN = 0x04				# table definition length
	
	NOROWS97  = 0x08			# number of rows offset
	NOROWS2K = 0x0C
	
	NOROWSLEN = 0x02			# number of rows length
	ROWSLEN = 0x02
	
	LONGVALUEPAGE = "LVAL"	# ID for long value page indexes
	
	# Access version strings - shortcut to ID the correct page index quickly
	ACCESS2KVERSIONSTRING = "410063006300650073007300560065007200730069006f006e"
	ACCESS97VERSIONSTRING = "41636365737356657273696f6e"
