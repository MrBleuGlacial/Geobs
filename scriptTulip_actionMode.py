# Powered by Python 2.7

from tulip import *

#----------------------- SETUP VALUES -----------------------
actionMode = "keyword" #keyword or actor
#------------------------------------------------------------

def main(graph): 
	Acces = graph.getStringProperty("Acces")
	CreationXML = graph.getStringProperty("CreationXML")
	Genealogie = graph.getStringProperty("Genealogie")
	Hierarchie = graph.getStringProperty("Hierarchie")
	ID_Fiche = graph.getStringProperty("ID_Fiche")
	Langage = graph.getStringProperty("Langage")
	OrganisationName = graph.getStringVectorProperty("OrganisationName")
	OrganisationRole = graph.getStringVectorProperty("OrganisationRole")
	Role = graph.getStringProperty("Role")
	Tags = graph.getStringProperty("Tags")
	Titre = graph.getStringProperty("Titre")
	
	viewBorderColor = graph.getColorProperty("viewBorderColor")
	viewBorderWidth = graph.getDoubleProperty("viewBorderWidth")
	viewColor = graph.getColorProperty("viewColor")
	viewFont = graph.getStringProperty("viewFont")
	viewFontAwesomeIcon = graph.getStringProperty("viewFontAwesomeIcon")
	viewFontSize = graph.getIntegerProperty("viewFontSize")
	viewLabel = graph.getStringProperty("viewLabel")
	viewLabelBorderColor = graph.getColorProperty("viewLabelBorderColor")
	viewLabelBorderWidth = graph.getDoubleProperty("viewLabelBorderWidth")
	viewLabelColor = graph.getColorProperty("viewLabelColor")
	viewLabelPosition = graph.getIntegerProperty("viewLabelPosition")
	viewLayout = graph.getLayoutProperty("viewLayout")
	viewMetric = graph.getDoubleProperty("viewMetric")
	viewRotation = graph.getDoubleProperty("viewRotation")
	viewSelection = graph.getBooleanProperty("viewSelection")
	viewShape = graph.getIntegerProperty("viewShape")
	viewSize = graph.getSizeProperty("viewSize")
	viewSrcAnchorShape = graph.getIntegerProperty("viewSrcAnchorShape")
	viewSrcAnchorSize = graph.getSizeProperty("viewSrcAnchorSize")
	viewTexture = graph.getStringProperty("viewTexture")
	viewTgtAnchorShape = graph.getIntegerProperty("viewTgtAnchorShape")
	viewTgtAnchorSize = graph.getSizeProperty("viewTgtAnchorSize")

	if(actionMode == "keyword"):
		#Creation of keyword nodes
		tagFamilies = {}
		for n in graph.getNodes():
			tmpString =  (Tags[n][1:]).split(';;')
			#print tmpString
			for s in tmpString:
				tagFamilies.setdefault(s.strip(),[]).append(n)
		#Creation of edges between xml nodes and keyword nodes
		for s in tagFamilies:
			if(len(s) > 2):		
				tmpNode = graph.addNode()
				viewLabel[tmpNode] = s
				viewColor[tmpNode] = tlp.Color(100,255,100)
				for n in tagFamilies[s]:
					graph.addEdge(tmpNode,n)
		
	if(actionMode == "actor"):
		#Creation of actor nodes
		actorFamilies = {}
		for n in graph.getNodes():
			for i in range(len(OrganisationName[n])):
				actorFamilies.setdefault(OrganisationName[n][i],[]).append([n,OrganisationRole[n][i]])
		for t in actorFamilies:			
			tmpNode = graph.addNode()
			viewShape[tmpNode] = tlp.NodeShape.Triangle
			viewLabel[tmpNode] = t
			for i in  actorFamilies[t]:
				e = graph.addEdge(i[0],tmpNode)
				Role[e] = i[1]
