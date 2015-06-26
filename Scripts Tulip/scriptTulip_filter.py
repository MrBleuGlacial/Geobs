# Powered by Python 2.7
# -*- coding: utf8 -*-
from tulip import *

#----------------------- SETUP VALUES -----------------------
actionMode = "surface" #tags or surface
refTags = ["mer","littoral","mer et littoral","biodiversité"]
refBox = [45.5731,43.3067,-1.78601,-0.577148] #[N,S,W,E]
#------------------------------------------------------------

def intersectionSurface(n1,n2,i1,i2):
	SurfaceEst = graph.getDoubleVectorProperty("SurfaceEst")
	SurfaceNord = graph.getDoubleVectorProperty("SurfaceNord")
	SurfaceOuest = graph.getDoubleVectorProperty("SurfaceOuest")
	SurfaceSud = graph.getDoubleVectorProperty("SurfaceSud")		
	
	s1 = [SurfaceNord[n1][i1],SurfaceSud[n1][i1],SurfaceOuest[n1][i1],SurfaceEst[n1][i1]]
	s2 = [SurfaceNord[n2][i2],SurfaceSud[n2][i2],SurfaceOuest[n2][i2],SurfaceEst[n2][i2]]

	dx = cmprAxes(s1,s2,0)
	dy = cmprAxes(s1,s2,1)
	
	return dx*dy	

def cmprAxes(s1,s2,axe):
	#Axe : 0 = vertical (NORTH/SOUTH), else = horizontal (WEST/EST)
	if(axe == 0):
		a = 1
		b = 0
	else:
		a = 2
		b = 3
		
	if((cmpr3Pts(s1[a],s2[a],s2[b]) == 0) and (cmpr3Pts(s1[b],s2[a],s2[b])) == 1):
		d = abs(s1[a]-s2[b])
	elif((cmpr3Pts(s1[a],s2[a],s2[b]) == -1) and (cmpr3Pts(s1[b],s2[a],s2[b])) == 0):
		d = abs(s2[a]-s1[b])
	elif((cmpr3Pts(s1[a],s2[a],s2[b]) == 0) and (cmpr3Pts(s1[b],s2[a],s2[b])) == 0):
		d = abs(s1[a]-s1[b])
	elif((cmpr3Pts(s1[a],s2[a],s2[b]) == -1) and (cmpr3Pts(s1[b],s2[a],s2[b])) == 1):
		d = abs(s2[a]-s2[b])
	else:
		d = 0
	return d	

def cmpr3Pts(v,v1,v2):
	if(v2 < v1):
		tmp = v1
		v1 = v2
		v2 = tmp	
	if((v >= v1) and (v <= v2)):
		return 0
	elif((v < v1) and (v < v2)):
		return -1
	elif((v > v1) and (v > v2)):
		return 1	
	else:
		print "Error cmpr3Pts"
		print v
		print v1
		print v2
		return -2

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

	if(actionMode == "tags"):
		for n in graph.getNodes():
			validate = False
			s = Tags[n].split(";;")
			s[0] = s[0][1:]
			for i in s :
				for j in refTags :
					if(i.strip() == j.upper()):
						validate = True
						break;
			if(not validate):
				graph.delNode(n)
	
	if(actionMode == "surface"):
		box = graph.addNode()
		SurfaceNord[box]= [refBox[0]]
		SurfaceSud[box]= [refBox[1]]
		SurfaceOuest[box]= [refBox[2]]
		SurfaceEst[box]= [refBox[3]]
		
		for n in graph.getNodes():
			validate = False
			for i in range(len(SurfaceNord[n])):
				if(SurfaceSud[box][0] <= SurfaceNord[n][i] <= SurfaceNord[box][0]):
					validate = True
					break
				if(SurfaceSud[box][0] <= SurfaceSud[n][i] <= SurfaceNord[box][0]):
					validate = True
					break
				if(SurfaceOuest[box][0] <= SurfaceOuest[n][i] <= SurfaceEst[box][0]):
					validate = True
					break
				if(SurfaceOuest[box][0] <= SurfaceEst[n][i] <= SurfaceEst[box][0]):
					validate = True
					break	
			if(not validate):
				graph.delNode(n)	
		graph.delNode(box)	
