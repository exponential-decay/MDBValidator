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