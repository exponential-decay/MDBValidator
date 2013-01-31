class MDBValidatorMarkers:

	DBDEFINITION      = 0x00 	# Database definition page
	DBDATAPAGE        = 0x01 	# Data page
	DBTABLEDEFINITION = 0x02 	# Table definition
	DBINTERINDEXPAGE  = 0x03 	# Intermediate Index pages
	DBLEAFINDEXPAGE   = 0x04 	# Leaf Index pages 
	DBPAGEUSAGEBMP    = 0x05 	# Page Usage Bitmaps
	DBPAGENOID			= -1		# Pages we cannot identify...

	DBPAGETYPE = { DBDEFINITION : "Database definition page",
						DBDATAPAGE   : "Data page",
						DBTABLEDEFINITION : "Table definition",
						DBINTERINDEXPAGE : "Intermediate index page",
						DBLEAFINDEXPAGE : "Leaf index page", 
						DBPAGEUSAGEBMP : "Page usage bitmap", 
						DBPAGENOID : "Unidentified page type" }

	DBPAGECOUNT = { DBDEFINITION : 0,
						 DBDATAPAGE   : 0,
						 DBTABLEDEFINITION : 0,
						 DBINTERINDEXPAGE : 0,
						 DBLEAFINDEXPAGE : 0, 
						 DBPAGEUSAGEBMP : 0, 
						 DBPAGENOID : 0 }

	DBPAGEINDEX = { DBDEFINITION : DBDEFINITION,
						 DBDATAPAGE   : DBDATAPAGE,
						 DBTABLEDEFINITION : DBTABLEDEFINITION,
						 DBINTERINDEXPAGE : DBINTERINDEXPAGE,
						 DBLEAFINDEXPAGE : DBLEAFINDEXPAGE, 
						 DBPAGEUSAGEBMP : DBPAGEUSAGEBMP, 
						 DBPAGENOID : DBPAGENOID }
						 
	MSYSOBJECTSPAGE = 0x02