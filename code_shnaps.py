# -*- coding: utf8 -*-

import urllib
import xml.etree.ElementTree as ET

connectBDD = "http://localhost:8080/exist/rest/db/"
query = "geobs?_query=declare%20namespace%20gmd=%22http://www.isotc211.org/2005/gmd%22;%20declare%20namespace%20gco=%22http://www.isotc211.org/2005/gco%22;%20for%20$herit%20at%20$pos%20in%20//gmd:statement/gco:CharacterString%20return%20concat($pos,%27%20-%20%27,$herit)"
number_res = "&_howmany=5000"

valHeaderValue = '<exist:value exist:type="xs:string">'

link = connectBDD + query + number_res
f = urllib.urlopen(link)
myQueryRes = f.read()

parsingWord = ""
parsingMode = 0
listValue = []

for char in myQueryRes:
    if(char == '<'):
        if(parsingWord != ""):
            listValue.append(parsingWord)
            parsingWord = ""
        parsingMode = 0
    if(parsingMode == 1):
        parsingWord = parsingWord + char
    if(char == '>'):
        parsingMode = 1
        
if(parsingWord != ""):
            listValue.append(parsingWord)
#print (listValue)

file = open("autoquery_lineage","w")  
for elem in listValue:
    file.write(elem)
print ('Done')
