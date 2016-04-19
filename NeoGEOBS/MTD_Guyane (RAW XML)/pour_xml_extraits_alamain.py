#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

######################################################################################
# Projet GEOBS
# Regroupement des fichiers XML extraits manuellement d'un catalogue
# Version du 13/01/2015
#
# Quand on extrait les mÈtadonnÈes d'un catalogue
# ‡ la main, met toutes les mÈtadonnÈes extraites
# dans le mÍme dossier et les renomme par leur id
#
# Structure du dossier de dÈpart :
# - un dossier par extraction (MD 1 ‡ 100, puis 101 ‡ 200...)
# - dans chaque dossier extraction : un dossier par mÈtadonnÈe
# - dans ce dossier, un dossier metadata avec le fichier metadata.xml ‡ rÈcupÈrer
# - dans ce dossier, Ègalement un fichier info.xml avec l'id dans la balise <localId>
######################################################################################

# import des modules necessaires
import os
import shutil


######################################################################################
# VARIABLES A REMPLIR
######################################################################################

# emplacement du dossier de depart
# exemple : 'd://travail//geobs//extraction_xml'
depart = "C:\\GEOBS\\MTD_CEBA"
# Emplacement du dossier ou seront sauvegardes les fichiers XML (doit exister)
# exemple : 'd://travail//geobs//extraction_xml_regroupes'
dest = "C:\\GEOBS\\MTD_CEBA_dest"


######################################################################################
# SCRIPT
######################################################################################

# pour chaque dossier correspondant ‡ une extraction manuelle
for i in os.listdir(depart):
    # pour chaque mÈtadonnÈe dans ce dossier
    for j in os.listdir(depart + '\\' + i):
        # rÈcupËre la mÈtadonnÈe correspondante (fichier metadata.xml)
        md = depart + '\\' + i + '\\' + j + '\\metadata\\metadata.xml'
        #print j
        # si le fichier mÈtadonnÈe existe
        if os.path.isfile(md):
            print 'cool'
            # rÈcupËre l'identifiant
            input = open(depart + '\\' + i + '\\' + j + '\\info.xml', 'r')
            info = input.read()
            idlocal = info[info.index("<localId>") + 9:info.index("</localId>")]
            # copie la mÈtadonnÈe dans le dossier destination avec comme nom l'id
            futurmd = dest + '\\' + idlocal + '.xml'
            # Si le fichier existe dÈj‡, le renomme avec dupl devant
            if os.path.isfile(futurmd):
                shutil.copyfile(md, dest + '\\dupl_' + idlocal + '.xml')
            # sinon, le copie simplement
            else:
                shutil.copyfile(md, futurmd)
        #else:
         #   print ('pb avec le dossier ' + j)

# Et c'est tout!
print ("fini !")

