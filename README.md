MDBValidator
============

**Features**

* Identifies databases with password protection and displays the password
* Identifies the version of Access used to create the database
* Identifies the build number of the version of Access used to create the database
* Displays frequency and count of 'pages' and page-'types' in the DB

**NOTES:**

As best as possible I've tried to keep good notes about the process of creating this tool, up to
its current state. I've used the Archive Team File Format wiki as my weapon of choice. Hopefully 
some of the notes on here will help you too: http://fileformats.archiveteam.org/wiki/Access 

**TODO:**

* Output database stats as YAML
* Seek other db 'stats' to output
* De-crypt the RC4 portion of the DB definition page
* Make generic to other Jet Databases if possible
* Increment Access DB version, 8.0 (2000) = 9.0 (2000) etc. Seek further documentation.
* Test Access build numbers and look for matching documented values

### License

Contact me for information on licensing. 

### Disclaimer

The code in this repository is intended for use on files on which users have full rights to. Either in a
personal or digital preservation context as custodians of a file which you may have lost authentication
details to. This work may be used for purposes which may be deemed illegal. The author takes no responsibility
for the use of this code in an illegal context.
