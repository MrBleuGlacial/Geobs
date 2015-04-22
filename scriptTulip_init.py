# -*- coding: utf8 -*-

import urllib
import xml.etree.ElementTree as ET

#----------------------- SETUP VALUES -----------------------
debugValue = 0
nameBase = "geobs"
#------------------------------------------------------------

def main(graph): 
	viewBorderColor =  graph.getColorProperty("viewBorderColor")
	viewBorderWidth =  graph.getDoubleProperty("viewBorderWidth")
	viewColor =	 graph.getColorProperty("viewColor")
	viewFont =	graph.getStringProperty("viewFont")
	viewFontSize =	graph.getIntegerProperty("viewFontSize")
	viewLabel =	 graph.getStringProperty("viewLabel")
	viewLabelBorderColor =	graph.getColorProperty("viewLabelBorderColor")
	viewLabelBorderWidth =	graph.getDoubleProperty("viewLabelBorderWidth")
	viewLabelColor =  graph.getColorProperty("viewLabelColor")
	viewLabelPosition =	 graph.getIntegerProperty("viewLabelPosition")
	viewLayout =  graph.getLayoutProperty("viewLayout")
	viewMetaGraph =	 graph.getGraphProperty("viewMetaGraph")
	viewMetric =  graph.getDoubleProperty("viewMetric")
	viewRotation =	graph.getDoubleProperty("viewRotation")
	viewSelection =	 graph.getBooleanProperty("viewSelection")
	viewShape =	 graph.getIntegerProperty("viewShape")
	viewSize =	graph.getSizeProperty("viewSize")
	viewSrcAnchorShape =  graph.getIntegerProperty("viewSrcAnchorShape")
	viewSrcAnchorSize =	 graph.getSizeProperty("viewSrcAnchorSize")
	viewTexture =  graph.getStringProperty("viewTexture")
	viewTgtAnchorShape =  graph.getIntegerProperty("viewTgtAnchorShape")
	viewTgtAnchorSize =	 graph.getSizeProperty("viewTgtAnchorSize")
	
	ID_Fiche = graph.getStringProperty("ID_Fiche")
	Langage = graph.getStringProperty("Langage")
	Hierarchie = graph.getStringProperty("Hierarchie")
	CreationXML = graph.getStringProperty("CreationXML")
	OrganisationName = graph.getStringVectorProperty("OrganisationName")
	OrganisationRole = graph.getStringVectorProperty("OrganisationRole")
	Tags = graph.getStringProperty("Tags")
	Genealogie = graph.getStringProperty("Genealogie")
	Acces = graph.getStringProperty("Acces")
	Titre = graph.getStringProperty("Titre")
	Role = graph.getStringProperty("Role")
	SurfaceNord = graph.getDoubleVectorProperty("SurfaceNord")
	SurfaceSud = graph.getDoubleVectorProperty("SurfaceSud")
	SurfaceOuest = graph.getDoubleVectorProperty("SurfaceOuest")
	SurfaceEst = graph.getDoubleVectorProperty("SurfaceEst")

	#-----------------------------------
	print("--- Let's get started ---")
	#-----------------------------------

	#Querying to the REST database
	connectBDD = "http://localhost:8080/exist/rest/db/"
	query = '?_query=declare%20namespace%20gmd="http://www.isotc211.org/2005/gmd";%20declare%20namespace%20gco="http://www.isotc211.org/2005/gco";%20declare%20namespace%20fra="http://www.cnig.gouv.fr/2005/fra";%20let%20$mdMetadata%20:=%20//gmd:MD_Metadata%20return%20<result>%20{%20for%20$root%20in%20$mdMetadata%20let%20$fIdentifier%20:=%20string($root/gmd:fIdentifier)%20let%20$langage%20:=%20data($root/gmd:language/gmd:LanguageCode/@codeListValue)%20let%20$typeOfData%20:=%20lower-case(string($root/gmd:hierarchyLevelName[1]))%20let%20$dateCreation%20:=%20string($root/gmd:dateStamp)%20let%20$identificationInfo%20:=%20$root/gmd:identificationInfo/fra:FRA_DataIdentification%20let%20$keyWords%20:=%20$identificationInfo/gmd:descriptiveKeywords/gmd:MD_Keywords/gmd:keyword%20let%20$lineage%20:=%20string($root/gmd:dataQualityInfo[1]/gmd:DQ_DataQuality/gmd:lineage/gmd:LI_Lineage/gmd:statement[1])%20let%20$title%20:=%20string($identificationInfo/gmd:citation/gmd:CI_Citation/gmd:title[1])%20let%20$restrain%20:=%20$identificationInfo/gmd:resourceConstraints/fra:FRA_LegalConstraints/gmd:useLimitation%20return%20<Fiche>%20<ID_Fiche>-{$fIdentifier}</ID_Fiche>%20<langage>-{$langage}</langage>%20<Hierarchie>-{$typeOfData}</Hierarchie>%20<CreationXML>-{$dateCreation}</CreationXML>%20<Titre>-{$title}</Titre>%20{%20for%20$responsable%20in%20$identificationInfo/gmd:pointOfContact/gmd:CI_ResponsibleParty%20let%20$roleResponsable%20:=%20$responsable/gmd:role/gmd:CI_RoleCode/@codeListValue%20let%20$nameResponsable%20:=%20$responsable/gmd:organisationName%20where%20$roleResponsable%20=%20%27owner%27%20or%20$roleResponsable%20=%20%27pointOfContact%27%20return%20<Organisation>%20<OrganisationName>{string($nameResponsable)}</OrganisationName>%20<OrganisationRole>{data($roleResponsable)}</OrganisationRole>%20</Organisation>%20}%20{%20for%20$geographicElement%20in%20$identificationInfo/gmd:extent/gmd:EX_Extent/gmd:geographicElement/gmd:EX_GeographicBoundingBox%20return%20<Surface>%20<Nord>{number($geographicElement/gmd:northBoundLatitude)}</Nord>%20<Sud>{number($geographicElement/gmd:southBoundLatitude)}</Sud>%20<Ouest>{number($geographicElement/gmd:westBoundLongitude)}</Ouest>%20<Est>{number($geographicElement/gmd:eastBoundLongitude)}</Est>%20</Surface>%20}%20<Tags>-{%20for%20$tag%20at%20$pos%20in%20$keyWords%20return%20upper-case(concat($tag,%27;;%27))%20}%20</Tags>%20<Acces>-{%20for%20$rest%20in%20$restrain%20return%20concat($rest,%27;;%27)%20}%20</Acces>%20<Genealogie>-{($lineage)}</Genealogie>%20</Fiche>%20}%20</result>'
	number_res = "&_howmany=5000"

	link = connectBDD + nameBase + query + number_res
	f = urllib.urlopen(link)
	myQueryRes = f.read()

	#Beginning of the process
	root = ET.fromstring(myQueryRes)

	#-----------------------------------
	print("- Extraction ready")
	#-----------------------------------

	#List of .xml's informations
	listFileXml = []
	numberFile = len(root[0])

	print("- " + str(len(root[0])) + " fs found")

	for i in range(0,numberFile):
		fileXml = {"Organisation":[],"Surface":[]}
		
		#Covering all the elements of the fileXml(.xml)		
		for j in range(0,len(root[0][i])): #root[0][i] = <fiche>
			fragment = root[0][i][j]
	##		print(type(fragment.text))
	##		print(fragment.text)	
	##		print(fragment.tag)
					
			if(fragment.tag == 'Surface'):
				if(not root[0][i][j][0].text is None):
					#print (float(root[0][i][j][0].text))
					surfaceValue = {'Nord': (float(root[0][i][j][0].text)),'Sud':(float(root[0][i][j][1].text)),'Ouest':(float(root[0][i][j][2].text)),'Est':(float(root[0][i][j][3].text))}
					fileXml["Surface"].append(surfaceValue)
					#print fileXml['Surface']
			
			elif(fragment.tag == 'Organisation'):
				#print root[0][i][j][1]
				if(not root[0][i][j][0].text is None):
					organisationValue = {'Name':root[0][i][j][0].text.encode("utf-8"),'Role':root[0][i][j][1].text.encode("utf-8")}
					#print organisationValue
					fileXml['Organisation'].append(organisationValue)
					#print fileXml['Organisation']
				
			else:
				fileXml[fragment.tag] =(fragment.text).encode("utf-8")
		listFileXml.append(fileXml)

	#-----------------------------------
	#			  Debugging
	#-----------------------------------
	if(debugValue == 1):
		f = open("testScriptTulip","w")
		for i in range(0,numberFile):
			for j in listFileXml[i]:
				if(j == 'Organisation'):
					f.write('Organisation :')
					if(listFileXml[i][j] != []):
						f.write('\n------------')
						for k in listFileXml[i][j]:
							f.write('\n\t'+'Name : '+ k['Name'] + '\n\t')
							f.write('Role : '+ k['Role']+'\n------------')
						f.write('\n')
					else:
						f.write(' -\n')
				else:
					f.write(j + " : ")
					f.write(listFileXml[i][j] + "\n")
				#print(type((listFileXml[0][ind])))
			f.write("----------------------------------------------------------------------------\n")
		print("- Test written")
		f.close()
	#-----------------------------------
	print("--- Ended ---")
	
	#Creation and initilisation of xml fs nodes
	for i in range(numberFile):
		tmp = graph.addNode()
		#OrganisationName[tmp]=[]
		OrganisationNameTmp = []
		OrganisationRoleTmp = []	
		SurfaceNordTmp = []
		SurfaceSudTmp = []
		SurfaceOuestTmp = []
		SurfaceEstTmp = []
		for j in listFileXml[i]:
			if(j == 'Organisation'):
				if(listFileXml[i][j] != []):
					for k in listFileXml[i][j]:
						OrganisationNameTmp.append(k['Name'].upper())
						OrganisationRoleTmp.append(k['Role'])		
				OrganisationName[tmp] = OrganisationNameTmp
				OrganisationRole[tmp] = OrganisationRoleTmp
			elif(j == 'Surface'):
				if(listFileXml[i][j] != []):	
					#print	listFileXml[i][j]		
					for k in listFileXml[i][j]:	
						SurfaceNordTmp.append(k['Nord'])
						SurfaceSudTmp.append(k['Sud'])
						SurfaceOuestTmp.append(k['Ouest'])
						SurfaceEstTmp.append(k['Est'])
				#print SurfaceNordTmp		
				SurfaceNord[tmp] = SurfaceNordTmp
				SurfaceSud[tmp] = SurfaceSudTmp
				SurfaceOuest[tmp] = SurfaceOuestTmp
				SurfaceEst[tmp] = SurfaceEstTmp
			elif(j == 'ID_Fiche'):
				ID_Fiche[tmp] = listFileXml[i][j]
			elif(j == 'langage'):
				Langage[tmp] = listFileXml[i][j]
			elif(j == 'Hierarchie'):
				Hierarchie[tmp] = listFileXml[i][j]
			elif(j == 'CreationXML'):
				CreationXML[tmp] = listFileXml[i][j]
			elif(j == 'Tags'):
				Tags[tmp] = listFileXml[i][j]
			elif(j == 'Genealogie'):
				Genealogie[tmp] = listFileXml[i][j]
			elif(j == 'Titre'):
				Titre[tmp] = listFileXml[i][j]
			elif(j == 'Acces'):
				Acces[tmp] = listFileXml[i][j]
		#viewLabel[tmp] = str(tmp.id)
	
	graph.applyLayoutAlgorithm("Random layout",viewLayout)
	
