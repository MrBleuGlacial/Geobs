# -*- coding: utf8 -*-

# Powered by Python 2.7

# To cancel the modifications performed by the script
# on the current graph, click on the undo button.

# Some useful keyboards shortcuts : 
#   * Ctrl + D : comment selected lines.
#   * Ctrl + Shift + D  : uncomment selected lines.
#   * Ctrl + I : indent selected lines.
#   * Ctrl + Shift + I  : unindent selected lines.
#   * Ctrl + Return  : run script.
#   * Ctrl + F  : find selected text.
#   * Ctrl + R  : replace selected text.
#   * Ctrl + Space  : show auto-completion dialog.

from tulip import *
from math import *

def do_tf(word,list_words):
	count = 0
	cleanedWord = word.strip().upper()
	#print list_words
	
	for w in list_words:
		#print w.strip().upper()
		#print cleanedWord
		#print "---------------------"
		if(w.strip().upper() == cleanedWord):
			count += 1
	#print float(count)/float(len(list_words))		
	return float(count)/float(len(list_words))
	
def do_idf(graph,word):
	Genealogie = graph.getStringProperty("Genealogie")	
	nmbrWithOccurence = 0
	
	for n in graph.getNodes():
		strGen = Genealogie[n].split()
		hadOcccurence = False
		
		for s in strGen:
			if(s.strip().upper() == word):
				hadOcccurence = True
		if(hadOcccurence == True):
			nmbrWithOccurence += 1
	#print log(float(graph.numberOfNodes())/float(nmbrWithOccurence))
	return log(float(graph.numberOfNodes())/float(nmbrWithOccurence))

def do_tf_idf(graph,word,n):
	Genealogie = graph.getStringProperty("Genealogie")
	
	tf = do_tf(word,Genealogie[n].split())
	idf = do_idf(graph,word)
	
	return float(tf*idf)

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
	SurfaceEst = graph.getDoubleVectorProperty("SurfaceEst")
	SurfaceNord = graph.getDoubleVectorProperty("SurfaceNord")
	SurfaceOuest = graph.getDoubleVectorProperty("SurfaceOuest")
	SurfaceSud = graph.getDoubleVectorProperty("SurfaceSud")
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

	f = open("tf_idf_test","w")

	for n in graph.getNodes():
		if(Genealogie[n]=="-"):
			graph.delNode(n)

	for n in graph.getNodes():
		str_split = Genealogie[n].split()
		#print str_split
		File_Score = {}
		for s in str_split:
			s_cleaned = s.strip().upper()
			if(not s_cleaned in File_Score):
				File_Score[s_cleaned.encode("utf-8")] = do_tf_idf(graph,s_cleaned,n)
		print >> f, File_Score, "\n------------------------------------------------------------------------------------------\n"
		break	
		
		
