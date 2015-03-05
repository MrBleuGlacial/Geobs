#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

#################################################
# Projet GEOBS
# Extraction des métadonnées d'un géocatalogue
# Version du 12/01/2015
#################################################

# import des modules nécessaires
import urllib2, re


######################################################################################
# VARIABLES A REMPLIR
######################################################################################

# début de l'URL de chaque métadonnée (partie fixe)
# exemple IGN : 'http://www.geocatalogue.fr/getMetadata?format=XML&id='
deburl = 'tapez ici la partie fixe de l url du catalogue'
# Emplacement où seront sauvegardées les fichiers XML
# exemple : 'xml', 'd://travail//geobs//extraction_xml'
dest = 'tapez ici le chemin vers le dossier ou vous voulez sauvegarder les xml'
# identifiant min d'une métadonnée (il variera entre cette valeur et le max)
# exemple : 0
minid = 0
# identifiant max d'une métadonnée (il variera entre le min et cette valeur)
# exemple : 10000
maxid = 300000


######################################################################################
# SCRIPT
######################################################################################

# pour chaque valeur de l'identifiant
for i in range(minid,maxid):
    print i
    # reconsitue l'url de la métadonnée correspondant à cet id
    url = '%s%d' % (deburl, i)
    try:
        # met dans une variable le fichier xml
        xml = urllib2.urlopen(url)
        xml_content = xml.read()
        # s'il ne s'agit pas d'un fichier html
        if xml_content.startswith('<?xml'):
            # crée un fichier dans dest dont le nom est id.xml
            fichier = '%s%d.xml' % (dest, i)
            # ouvre ce fichier en écriture (b pour binary)
            output = open(fichier, 'wb')
            # écrit le contenu de la métadonnée dans ce fichier
            output.write(xml_content)
            # ferme le fichier
            output.close()
    # si la métadonnée correspondant à cet id n'existe pas :
    except:
        # passe à la suivante
        pass
    # et on recommence jusqu'à maxid

print ("fini!")
        
