# Powered by Python 2.7

from tulip import *
from math import sqrt
import time

THRESHOLD = 50
	
def analyseSurface(n1,n2):
	SurfaceNord = graph.getDoubleVectorProperty("SurfaceNord")	
	SurfaceCommune = graph.getIntegerProperty("SurfaceCommune")
	intersection = 0
	
	for i1 in range(len(SurfaceNord[n1])):
		for i2 in range(len(SurfaceNord[n2])):
			intersection += intersectionSurface(n1,n2,i1,i2)
	if(intersection > THRESHOLD):
		e = graph.addEdge(n1,n2)	
		SurfaceCommune[e] = intersection

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

def inclusionSurface(s1,s2):
	#s corresponds to a [North,South,West,Est] vector
	if(cmpr3Pts(s1[0],s2[0],s2[1]) == 0\
		and cmpr3Pts(s1[1],s2[0],s2[1]) == 0\
		and cmpr3Pts(s1[2],s2[2],s2[3]) == 0\
		and cmpr3Pts(s1[3],s2[2],s2[3]) == 0):
			return 1
	else:
		return 0

def distancePoints(p1,p2):
	return sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

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
	SurfaceCommune = graph.getIntegerProperty("SurfaceCommune")
	
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
	
	for n in graph.getNodes():
		if(SurfaceNord[n] == [] or SurfaceNord[n] == [0]):
			graph.delNode(n)	
			
	updateVisualization(centerViews = True)
	
	for n1 in graph.getNodes():
		for n2 in graph.getNodes():
			if(n1 != n2):
				if(not tlp.edge.isValid(graph.existEdge(n1,n2,False))):
					analyseSurface(n1,n2)	
	
	print "End at :"
	print(time.strftime("%H:%M:%S"))	
		
	
