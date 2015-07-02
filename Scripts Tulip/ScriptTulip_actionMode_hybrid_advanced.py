# Powered by Python 2.7

from tulip import *

#-----------------------------------------------------------------
#actionMode with "hybrid" option needed to perform this script
#-----------------------------------------------------------------


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
	TypeNode = graph.getStringProperty("TypeNode")
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

	print("--- Let's get started ---")
	
	
#	for n1 in graph.getNodes():
#		if(TypeNode[n1]=="Actor"):
#			for n2 in graph.getNodes():
#				if((TypeNode[n2]=="Actor") and (n1 != n2) and (not tlp.edge.isValid(graph.existEdge(n1,n2,False)))):
#					listn1 = tlp.reachableNodes(graph,n1,1,tlp.UNDIRECTED)
#					listn2 = tlp.reachableNodes(graph,n2,1,tlp.UNDIRECTED)
#					breakloop = False
#					for i1 in listn1:
#						if(breakloop == True):
#							break
#						for i2 in listn2:
#							if(i1 == i2):							
#								graph.addEdge(n1,n2)
#								breakloop = True
#	for n in graph.getNodes():
#		if(TypeNode[n]=="Keyword"):
#			graph.delNode(n)							
#									
	for n in graph.getNodes():
		if(TypeNode[n]=="Keyword"):
			listn = tlp.reachableNodes(graph,n,1,tlp.UNDIRECTED)
			for n1 in listn:
				for n2 in listn:
					if((n1!=n2) and (not tlp.edge.isValid(graph.existEdge(n1,n2,False)))):
						graph.addEdge(n1,n2)
	for n in graph.getNodes():
		if(TypeNode[n]=="Keyword"):
			graph.delNode(n)
			
	graph.applyLayoutAlgorithm("FM^3 (OGDF)",viewLayout)
	updateVisualization(centerViews = True)		
	
	print("--- Ended ---")
