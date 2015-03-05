#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

######################################################################################
# Projet GEOBS
# Regroupement des fichiers XML extraits manuellement d'un catalogue
# Version du 13/01/2015
#
# Quand on extrait les m�tadonn�es d'un catalogue
# � la main, met toutes les m�tadonn�es extraites
# dans le m�me dossier et les renomme par leur id
#
# Structure du dossier de d�part :
# - un dossier par extraction (MD 1 � 100, puis 101 � 200...)
# - dans chaque dossier extraction : un dossier par m�tadonn�e
# - dans ce dossier, un dossier metadata avec le fichier metadata.xml � r�cup�rer
# - dans ce dossier, �galement un fichier info.xml avec l'id dans la balise <localId>
######################################################################################

# import des modules necessaires
import os, shutil


######################################################################################
# VARIABLES A REMPLIR
######################################################################################

# emplacement du dossier de depart
# exemple : 'd://travail//geobs//extraction_xml'
depart = '//mnt//Travail//Baguala//temp//unzip'
# Emplacement du dossier ou seront sauvegardes les fichiers XML (doit exister)
# exemple : 'd://travail//geobs//extraction_xml_regroupes'
dest = '//home//julie//Bureau//bolivia_res'


######################################################################################
# SCRIPT
######################################################################################

# pour chaque dossier correspondant � une extraction manuelle
for i in os.listdir(depart):
    # pour chaque m�tadonn�e dans ce dossier
    for j in os.listdir(depart + "//" + i):
        # r�cup�re la m�tadonn�e correspondante (fichier metadata.xml)
        md = depart + "//" + i + "//" + j + "//metadata//metadata.xml"
        print md
        # si le fichier m�tadonn�e existe
        if os.path.isfile(md):
            # r�cup�re l'identifiant
            input = open(depart + "//" + i + "//" + j + "//info.xml", 'r')
            info = input.read()
            idlocal = info[info.index("<localId>") + 9:info.index("</localId>")]
            # copie la m�tadonn�e dans le dossier destination avec comme nom l'id
            futurmd = dest + "//" + idlocal + ".xml"
            # Si le fichier existe d�j�, le renomme avec dupl devant
            if os.path.isfile(futurmd):
                shutil.copyfile(md, dest + "//dupl_" + idlocal + ".xml")
            # sinon, le copie simplement
            else:
                shutil.copyfile(md, futurmd)
        else:
            print ('pb avec le dossier ' + j)

# Et c'est tout!
print ("fini !")

