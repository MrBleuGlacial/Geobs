# coding: utf8

# Powered by Python 2.7

from tulip import *
from math import *
import time
import sys 

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

def comp(v1, v2):
    if v1[1]<v2[1]:
        return -1
    elif v1[1]>v2[1]:
        return 1
    else:
        return 0
        
def compareScore(scoreElem,maxScore,elem):
	#print scoreElem
	for i in range(len(maxScore)):
		if(scoreElem > maxScore[i][1]):
			tmpSc = maxScore[i][1]
			tmpStr = maxScore[i][0]
			
			maxScore[i][1] = scoreElem
			maxScore[i][0] = elem 
			#print maxScore		  
			for j in range(i+1,len(maxScore)):
				tmpSc2 = maxScore[j][1]
				tmpStr2 = maxScore[j][0]
				maxScore[j][1] = tmpSc
				maxScore[j][0] = tmpStr
				tmpSc = tmpSc2
				tmpStr= tmpStr2 
			
			break
	#print maxScore			
	maxScore = sorted(maxScore, reverse = True, cmp = comp)
	#print maxScore	
	

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

	print "Start at :"
	print(time.strftime("%H:%M:%S"))

	f = open("tf_idf_test2","w")
	
	#delete nodes without genealogy data
	for n in graph.getNodes():
		if(Genealogie[n]=="-"):
			graph.delNode(n)

	bestScorePerNode = []

	#tf-idf processing to obtain scores for words
	for n in graph.getNodes():
		str_split = Genealogie[n].split()
		#print str_split
		File_Score = {}
		for s in str_split:
			s_cleaned = s.strip().upper()
			#print(type(s_cleaned))
			if(not s_cleaned in File_Score):
				File_Score[s_cleaned] = do_tf_idf(graph,s_cleaned,n)
		#print >> f, File_Score, "\n------------------------------------------------------------------------------------------\n"
		
		maxScore = [["",0],["",0],["",0]]
		for elem in File_Score:
			compareScore(File_Score[elem],maxScore,elem)
			#print maxScore		
			#print "----------------------"  
		bestScorePerNode.append([n,maxScore])
	
	#print >> f, bestScorePerNode
	for s in bestScorePerNode:
		print >> f, s[0]
		print >> f, s[1]
		print >> f, "------------------------------------------------------------------------------------------------------------------" 	
	f.close()

	print "End at :"
	print(time.strftime("%H:%M:%S"))	
		
