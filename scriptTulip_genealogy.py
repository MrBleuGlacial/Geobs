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

# the updateVisualization(centerViews = True) function can be called
# during script execution to update the opened views

# the pauseScript() function can be called to pause the script execution.
# To resume the script execution, you will have to click on the "Run script " button.

# the runGraphScript(scriptFile, graph) function can be called to launch another edited script on a tlp.Graph object.
# The scriptFile parameter defines the script name to call (in the form [a-zA-Z0-9_]+.py)

# the main(graph) function must be defined 
# to run the script on the current graph

def do_tf(word,list_words):
	count = 0
	cleanedWord = word.strip().upper()
	
	for w in list_word:
		if(w.strip().upper() == cleanedWord):
			count += 1
	
	return float(count/len(list_words))
	
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
	
	return float(log(graph.numberOfNodes()/nmbrWithOccurence))

def do_tf_idf(graph,word,n):
	Genealogie = graph.getStringProperty("Genealogie")
	
	tf = do_tf(word,Genealogie[n])
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

#	for n in graph.getNodes():
#		print n

	print graph.numberOfNodes()
