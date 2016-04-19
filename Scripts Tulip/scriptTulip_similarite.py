# Powered by Python 2.7

# To cancel the modifications performed by the script
# on the current graph, click on the undo button.

from tulip import *
import time
from math import sqrt

#file = open("testSimi.txt","w")

#----------------------- SETUP VALUES -----------------------
THRESHOLD = 0.55        # between 0 (all) and 1 (nothing)
cleanBeforeAction = 1  # 0 or 1
#------------------------------------------------------------

def fillVector(elem,ch,vct):
	if(elem in ch):
		vct.append(1)
		return True
	else:
		vct.append(0)
		return False

def cleanString(ch):
	for i in range(len(ch)):		
		ch[i] = ch[i].strip()

def getCosValue(vct1,vct2):
	num = 0.0
	denum = 0.0	
	tmp1 = 0.0
	tmp2 = 0.0
	for i in range(0,len(vct1)):
		num += (vct1[i]*vct2[i])
		tmp1 += vct1[i]
		tmp2 += vct2[i]
	denum = sqrt(tmp1)*sqrt(tmp2)
	return(num/denum)	
	
def getSimilarite(n1,n2,graph):
	Tags = graph.getStringProperty("Tags")
	sameTags = ""	
	
	ch1 =  Tags[n1][1:-2].split(";;")
	ch2 = Tags[n2][1:-2].split(";;")	
	vct1 = []
	vct2 = []	
	unionKey = []	
	cleanString(ch1)
	cleanString(ch2)	
	#print ch1	
	#print ch2
	
	for i in ch1:
		if(not(i in unionKey)):
			unionKey.append(i)
	for i in ch2:
		if(not(i in unionKey)):
			unionKey.append(i)
						
	for i in range(0,len(unionKey)):
		tmpBool1 = fillVector(unionKey[i],ch1,vct1)
		tmpBool2 = fillVector(unionKey[i],ch2,vct2)
		if(tmpBool1 & tmpBool2):
			sameTags += (unionKey[i] + " ; ")
	#if(sameTags != ""):
		#file.write(sameTags + "\n")
	return [(getCosValue(vct1,vct2)), sameTags]
	#print unionKey 
	#print vct1
	#print vct2


def main(graph): 
	Acces = graph.getStringProperty("Acces")
	CreationXML = graph.getStringProperty("CreationXML")
	Degree = graph.getDoubleProperty("Degree")
	Genealogie = graph.getStringProperty("Genealogie")
	Hierarchie = graph.getStringProperty("Hierarchie")
	ID_Fiche = graph.getStringProperty("ID_Fiche")
	Langage = graph.getStringProperty("Langage")
	OrganisationName = graph.getStringVectorProperty("OrganisationName")
	OrganisationRole = graph.getStringVectorProperty("OrganisationRole")
	Tags = graph.getStringProperty("Tags")
	Titre = graph.getStringProperty("Titre")
	
	viewBorderColor = graph.getColorProperty("viewBorderColor")
	viewBorderWidth = graph.getDoubleProperty("viewBorderWidth")
	viewColor = graph.getColorProperty("viewColor")
	viewFont = graph.getStringProperty("viewFont")
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

	#On edge
	Similarite = graph.getDoubleProperty("Similarite")
	Tags_Communs = graph.getStringProperty("Tags_Communs")

	################################################################

	print("--- Started ---")	
	print(time.strftime("%H:%M:%S"))
	
	if(cleanBeforeAction == 1):
		for n in graph.getNodes():
			if(ID_Fiche[n] == ""):
				graph.delNode(n)

	for n1 in graph.getNodes():
		for n2 in graph.getNodes():
			if((ID_Fiche[n1] != "") and (ID_Fiche[n2] != "") and (n1 != n2)):
				if(not tlp.edge.isValid(graph.existEdge(n1,n2,False))):
					resTab = getSimilarite(n1,n2,graph)	
					dist = resTab[0]
					sameTags = resTab[1]
					if(sameTags != " ; "):
						if(dist > THRESHOLD):
							dist = round(dist,6)
							e = graph.addEdge(n1,n2)
							Similarite[e] = dist
							Tags_Communs[e] = sameTags
							#viewLabel[e] = repr(dist)

	print(time.strftime("%H:%M:%S"))	
	
	graph.applyLayoutAlgorithm("FM^3 (OGDF)",viewLayout)
	updateVisualization(centerViews = True)
	
	print("--- Ended ---")

	
