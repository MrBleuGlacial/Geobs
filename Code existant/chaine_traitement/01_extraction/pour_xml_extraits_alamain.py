#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

######################################################################################
# Projet GEOBS
# Regroupement des fichiers XML extraits manuellement d'un catalogue
# Version du 13/01/2015
#
# Quand on extrait les métadonnées d'un catalogue
# à la main, met toutes les métadonnées extraites
# dans le même dossier et les renomme par leur id
#
# Structure du dossier de départ :
# - un dossier par extraction (MD 1 à 100, puis 101 à 200...)
# - dans chaque dossier extraction : un dossier par métadonnée
# - dans ce dossier, un dossier metadata avec le fichier metadata.xml à récupérer
# - dans ce dossier, également un fichier info.xml avec l'id dans la balise <localId>
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
# FONCTIONS
######################################################################################

def get_subdir(repertoire):
    liste_subdir = []
    for i in os.listdir(repertoire):
        if os.path.isdir(os.path.join(repertoire, i)):
            liste_subdir.append(i)
    return liste_subdir


######################################################################################
# SCRIPT
######################################################################################

# pour savoir s'il y a eu ou non des doublons
doublon = 'non'
# pour chaque dossier correspondant à une extraction manuelle
for i in get_subdir(depart):
    # pour chaque métadonnée dans ce dossier
    for j in get_subdir(depart + "//" + i):
        # récupère la métadonnée correspondante (fichier metadata.xml)
        md = depart + "//" + i + "//" + j + "//metadata//metadata.xml"
        # si le fichier métadonnée existe
        if os.path.isfile(md):
            # récupère l'identifiant
            input = open(depart + "//" + i + "//" + j + "//info.xml", 'r')
            info = input.read()
            idlocal = info[info.index("<localId>") + 9:info.index("</localId>")]
            # copie la métadonnée dans le dossier destination avec comme nom l'id
            futurmd = dest + "//" + idlocal + ".xml"
            # Si le fichier existe déjà, le renomme avec dupl devant
            if os.path.isfile(futurmd):
                doublon = 'oui'
                shutil.copyfile(md, dest + "//dupl_" + idlocal + ".xml")
                print ('doublon pour ' + idlocal + ".xml")
            # sinon, le copie simplement
            else:
                shutil.copyfile(md, futurmd)
        else:
            print ('pb avec le dossier ' + j)

# informe l'utilisateur qu'il doit vérifier et supprimer lui-meme les éventuels doublons
if doublon == 'oui':
    print ('\nLes doublons n ont pas ete supprimes. Ils ont le prefixe "dupl_"')
    print ('A vous de les verifier et supprimer eventuellement !\n')

# Et c'est tout!
print ("fini !")

