# -*- coding: utf8 -*-

import urllib
import xml.etree.ElementTree as ET

#-----------------------------------
print("--- Let's get started ---")
#-----------------------------------

#Querying to the REST database
connectBDD = "http://localhost:8080/exist/rest/db/"
query = 'geobs?_query=declare%20namespace%20gmd="http://www.isotc211.org/2005/gmd";%20declare%20namespace%20gco="http://www.isotc211.org/2005/gco";%20declare%20namespace%20fra="http://www.cnig.gouv.fr/2005/fra";%20let%20$mdMetadata%20:=%20//gmd:MD_Metadata%20return%20<result>%20{%20for%20$root%20in%20$mdMetadata%20let%20$fileIdentifier%20:=%20string($root/gmd:fileIdentifier)%20let%20$langage%20:=%20data($root/gmd:language/gmd:LanguageCode/@codeListValue)%20let%20$typeOfData%20:=%20lower-case(string($root/gmd:hierarchyLevelName[1]))%20let%20$dateCreation%20:=%20string($root/gmd:dateStamp)%20let%20$identificationInfo%20:=%20$root/gmd:identificationInfo/fra:FRA_DataIdentification%20let%20$keyWords%20:=%20$identificationInfo/gmd:descriptiveKeywords/gmd:MD_Keywords/gmd:keyword%20let%20$lineage%20:=%20string($root/gmd:dataQualityInfo[1]/gmd:DQ_DataQuality/gmd:lineage/gmd:LI_Lineage/gmd:statement[1])%20return%20<Fiche>%20<ID_Fiche>-{$fileIdentifier}</ID_Fiche>%20<langage>-{$langage}</langage>%20<Hierarchie>-{$typeOfData}</Hierarchie>%20<CreationXML>-{$dateCreation}</CreationXML>%20{%20for%20$responsable%20in%20$identificationInfo/gmd:pointOfContact/gmd:CI_ResponsibleParty%20let%20$roleResponsable%20:=%20$responsable/gmd:role/gmd:CI_RoleCode/@codeListValue%20let%20$nameResponsable%20:=%20$responsable/gmd:organisationName%20where%20$roleResponsable%20=%20%27owner%27%20or%20$roleResponsable%20=%20%27pointOfContact%27%20return%20<Organisation>%20<OrganisationName>{string($nameResponsable)}</OrganisationName>%20<OrganisationRole>{data($roleResponsable)}</OrganisationRole>%20</Organisation>%20}%20<Tags>-{%20for%20$tag%20at%20$pos%20in%20$keyWords%20return%20concat($tag,%27%20%27)%20}%20</Tags>%20<Genealogie>-{($lineage)}</Genealogie>%20</Fiche>%20}%20</result>'
number_res = "&_howmany=5000"

link = connectBDD + query + number_res
f = urllib.urlopen(link)
myQueryRes = f.read()

#Beginning of the process
root = ET.fromstring(myQueryRes)

#-----------------------------------
print("- datas found successfully")
#-----------------------------------

listCard = []
numberCard = len(root[0])

print("- " + str(len(root[0])) + " cards found")

for i in range(0,numberCard):
    card ={}
    for j in range(0,len(root[0][i])):
        fragment = root[0][i][j]
##        print(type(fragment.text))
##        print(fragment.text)
##        print(fragment.tag)
        card[fragment.tag] =(fragment.text).encode("utf-8")
    listCard.append(card)

#-----------------------------------
#             Debugging
#-----------------------------------
file = open("testScriptTulip","w")
for i in range(0,numberCard):
    for j in listCard[i]:
        file.write(j + " : ")
        file.write(listCard[i][j] + "\n")
        #print(type((listCard[0][ind])))
    file.write("-------------------------\n")
print("- Test written")
#-----------------------------------
print("--- Ended ---")
file.close()
