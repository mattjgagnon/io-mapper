'''
    This program attempts to map input fields with output fields.

    Specifically, it tries to take fields from a CSV file and map them to
    web form fields and creates an XML file of the mappings.

    Name:       IO Mapper
    Creator:    Matt Gagnon <mattjgagnon@gmail.com>
    Created:    2012-08-22
    Revised:
    Version:    1.0
    Python:     2.6
    Dependency: None
'''

# =============
# CONFIGURATION
# =============
import datetime

# the program's name - used internally
programName     = 'io-mapper'

# the url of the form submission
LEAD_FORM       = 'http://www.crmtool.net/WebForm.asp?F=451&W=13858'

today = datetime.datetime.now().strftime("%m/%d/%Y")
today2 = datetime.datetime.now().strftime("%Y-%m-%d-%M-")

# the input file name and then the working file name
INPUT_FILE      = 'csv/zebra-fields.csv'
WORKING_FILE    = 'xml/'+today2+'mapping.xml'

# =========
# FUNCTIONS
# =========
def csv2xml(csvFile, xmlFile, rootTag = 'mapping', rowTag = 'field', encoding = 'utf-8'):
    '''
        Converts a CSV file to an XML file.

        The first row of the csv file must be the field names.
        csvFile     = the original CSV file (full path and filename)
        xmlFile     = the generated XML file (full path and filename)
        rootTag     = the root-level XML tag (defaults to leads)
        rowTag      = the record-level XML tag (defaults to lead)
        encoding    = the XML file encoding (defaults to utf-8)
    '''

    # get the csv module
    import csv

    # open the csv file
    try:
        # try to open the csv file in universal new-line mode
        # the rU means raw universal mode (more flexible)
        csvData = csv.reader(open(csvFile, 'rU'))
    except IOError, e:
        # a file error occurred
        print 'could not open the file ' + INPUT_FILE+': ',e
    else:
        print 'opened the file ' + INPUT_FILE

        # open the xml file in write mode
        xmlData = open(xmlFile, 'w')
        xmlData.write('<?xml version="1.0" encoding="'+encoding+'"?>' + "\n")

        # there must be only one top-level tag
        xmlData.write('<'+rootTag+'>' + "\n")

        rowNum = 0
        for row in csvData:
            if rowNum == 0:
                tags = row
                # replace spaces with underscores in tag names
                for i in range(len(tags)):
                    tags[i] = tags[i].replace('\xef\xbb\xbf', '')
                    tags[i] = tags[i].replace('"', '')
##                    tags[i] = tags[i].replace(' ', '_')
##                    tags[i] = tags[i].replace('(', '')
##                    tags[i] = tags[i].replace(')', '')
##                    tags[i] = tags[i].replace('/', '_')
##                    tags[i] = tags[i].replace('$', '')
##                    tags[i] = tags[i].replace('#', 'Num')
##                    tags[i] = tags[i].replace('__', '_')
            else:
                xmlData.write('    <input>'+"\n")
                x = 0

                for i in range(len(tags)):
                    xmlData.write('        <'+rowTag+'>'+"\n")
                    x += 10
                    xmlData.write('            <map>'+str(x)+'</map>'+"\n")
                    xmlData.write('            <name>'+tags[i]+'</name>'+"\n")
                    xmlData.write('        </'+rowTag+'>'+"\n")

                xmlData.write('    </input>'+"\n")

            rowNum +=1

        xmlData.write('</'+rootTag+'>'+"\n")
        xmlData.close()
        print 'closed the file '+INPUT_FILE

# =========
# MAIN CODE
# =========

# log the start of the program
print '--->program status: started'

# convert the csv file to xml
csv2xml(INPUT_FILE, WORKING_FILE)

# log the end of the program
print '--->program status: finished'
