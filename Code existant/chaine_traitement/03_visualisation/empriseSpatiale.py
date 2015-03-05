# -*- coding: iso-8859-1 -*-#!/usr/bin/python

###################################################
# Projet GEOBS
# Cr�ation d'un GEOJSON d'emprises spatiales � partir CSV
# Version du 13/01/2015
#
# Ce script cr�e un fichier GeoJSON � partir d'un
# fichier CSV contenant une liste d'emprises.
# Le fichier de d�part de ce script est le r�sultat
# d'une requ�te XQuery.
#
# Le GeoJSON contient un polygone par fichier XML
# (donc un multipolygone si plusieurs emprises pour
# un m�me fichier XML), et 5 champs dans la table
# attributaire : file_name (nom du fichier XML)
# et les 4 coordonn�es O, E, N et S.
###################################################

###################################################
# Structure du fichier GeoJSON en entr�e :
# un dico "features" pour tout le fichier, qui contient :
# une liste de dico, dont chaque dico contient lui-m�me :
# un dico g�om�trie, un dico properties (attributs)
# et une cl� 'type' de valeur 'feature'.
# Ex. :
# Features : [
# { dico_geom : {...}, dico_attr : {...}, 'type' : 'Feature'},  /polygone 1
# { dico_geom : {...}, dico_attr : {...}, 'type' : 'Feature'}   /polygone 2
# ...                                                           /etc.
# ]
# Le dico g�om�trie contient une cl� 'type' (valeur
# MultiPolygon) et une cl� 'coordinates'.
# Le dico d'attributs contient une cl� par colonne.
###################################################

###################################################
# Fichier CSV de d�part : 3 colonnes
# "25867.xml";"004ad077-d5f0-4933-806b-c61ced37883f";"-0.31 -0.26 48.928 48.962"
# "25551.xml";"004cbdf8-d966-4602-b017-bf04d9437527";"1.848 1.995 47.562 47.679"
# "28516.xml";"004cc093-0a5c-4c87-a3c0-caef72418a06";"5.518 5.54 46.606 46.641"
# "72701.xml";"004e9316-2bcc-4ef3-9775-d14e2ba35e65";"-70 -60 10 20";"-70 -60 10 20";"-60 -50 0 10";"50 60 -30 -20";"44.9 45.3 -13.1 -12.6";"-178.12 -175.43 -13.72 -12.5"
###################################################



########################
# Import de modules
########################

import datetime


########################
# VARIABLES A REMPLIR
########################

# ATTENTION, METTRE DES '//' DANS LES CHEMINS

# emplacement du fichier CSV de d�part (ex. : "c://Travail//geobs//emprise_spatiale.csv")
fichier = '//home//julie//Bureau//csv//emprise_spatiale.csv'
# nom et emplacement du fichier GeoJSON qui sera cr�� (ex. : "c://Travail//geobs//emprise_spatiale.geojson")
geojson = '//home//julie//Bureau//geojson//emprise_spatiale.geojson'
# nom et emplacement du log qui sera cr�� (ex. : "c://Travail//geobs//emprise_spatiale.txt")
log = '//home//julie//Bureau//geojson//emprise_spatiale.txt'


########################
# VARIABLES A REMPLIR EVENTUELLEMENT
########################

# s�parateur du fichier CSV
sep = ';'
# nom du champ qui contiendra le nom du fichier XML
champ_nom = 'file_name'
# nom du champ qui contiendra le nombre de polygones de l'entit� (qui peut �tre un multipolygone)
champ_nb_polyg = 'nb'
# compte le nb de fichiers pour lesquels au moins une emprise est invalide (et au moins une valide)
# doit �tre �gal � z�ro
invalide = 0


########################
# Fonctions
########################

# Pour �crire les dicos dans le fichier GeoJSON comme il faut
def ecritureGeoJSON(liste_dico, fichier):
    # ouverture du geojson en �criture
    output = open(fichier, 'w')
    # �criture des 1�res lignes
    output.write('{\n"type": "FeatureCollection",\n\n"features": [\n')
    # �crit tous les dicos de la liste sauf le dernier, s�par�s par des ","
    for i in liste_dico[:-1]:
        output.write(str(i))
        output.write('\n,\n')
    # �crit le dernier dico de la liste
    output.write(str(liste_dico[-1]))
    # �crit les derni�res lignes
    output.write('\n\n]\n}')
    # Fermeture du fichier geojson
    output.close()

# Fonction pour r�cup�rer les coordonn�es des polygones � partir des 4 coord des emprises
def coordLigne(ligne):
    global invalide
    # initialise les coordonn�es
    coordinates = []
    liste_O = []
    liste_N = []
    liste_E = []
    liste_S = []
    # pour chaque jeu de coordonn�es d'une ligne
    for i in ligne[2:]:
        try:
            # on s�pare les 4 coordonn�es
            l = i.split(' ')
            # puis on les r�cup�re, en supprimant les "" et en rempla�ant les , par des .
            O = float(l[0][1:].replace(',','.'))
            N = float(l[3][:-1].replace(',','.'))
            E = float(l[1].replace(',','.'))
            S = float(l[2].replace(',','.'))
            # si les coord sont correctes
            if (-180 <= O <= 180) and (-180 <= E <= 180) and (-90 <= N <= 90) and (-90 <= S <= 90):
                # on ajoute l'ouest � la liste des coord ouest, etc. (utile si plusieurs emprises)
                liste_O.append(O)
                liste_N.append(N)
                liste_E.append(E)
                liste_S.append(S)
                # les coordonn�es des 4 points
                ON = [ O, N ]
                EN = [ E, N ]
                ES = [ E, S ]
                OS = [ O, S ]
                # il faut 5 jeux de coordonn�es pour fermer le rectangle
                coordinate = [[ON, EN , ES, OS, ON]]
                # ajout du jeu de coord � la liste
                coordinates.append(coordinate)
            # si les coordonn�es sont incorrectes
            else:
                output.write(str(liste_lignes.index(ligne)) + '\t' + ligne[0] + '\tcoord invalides\t' + str(i) + '\n')
                if len(ligne) > 3:
                    invalide = invalide + 1
        except:
            output.write(str(liste_lignes.index(ligne)) + '\t' + ligne[0] + '\tcoord invalides\t' + str(i) + '\n')
            if len(ligne) > 3:
                invalide = invalide + 1
            continue
    # ne cree que des geom de type multipolygone
    type_geom = 'MultiPolygon'
    # retourne la liste des jeux de coord, le type de g�om et les 4 coord
    return coordinates, type_geom, liste_O, liste_N, liste_E, liste_S

        
########################
# Script
#######################

# Lecture du fichier en entr�e
print ('Lecture fichier CSV...')
input = open(fichier, 'r')
# Le fichier est stock� sous forme de liste, ligne par ligne
print ('Stockage des valeurs...')
liste_lignes = [i.rstrip() for i in input.readlines()]
# Fermeture du fichier en entr�e
input.close()
# s�paration des diff�rents �l�ments de chaque ligne : on obtient une liste de liste
liste_lignes = [i.split(sep) for i in liste_lignes]
# cr�ation et remplissage des 3 dicos n�cessaires pour le geojson
print ('Preparation du GeoJSON...')
liste_dico_feat = []
# ouverture du log en �criture
output = open(log, 'w')
# ajout d'un en-t�te avec la date, le nom du script et le nom du fichier en entr�e dans le log
output.write('-' * 100 + '\n')
output.write(str(datetime.datetime.now()) + '\n')
output.write('Execution du script empriseSpatiale.py\n')
output.write('Fichier en entree : ' + fichier + '\n')
output.write('-' * 100 + '\n\n')
# ajout des en-t�tes de colonne
output.write('num_ligne\tfichier\tprobleme\tcoord\n')
# pour chaque ligne du CSV, = pour chaque fichier XML
for ligne in liste_lignes:
    # on prend en compte uniquement les lignes avec au moins un jeu de coord
    if len(coordLigne(ligne)[2]) > 0:
        try:
            # dico_geom
            dico_geom = {'type' : (coordLigne(ligne))[1], 'coordinates' : (coordLigne(ligne))[0]}
            # dico_attr : r�cup�ration des champs : nom du fichier, coordonn�es
            dico_attr = {champ_nom : ligne[0][1:-1],
                        champ_nb_polyg : len(coordLigne(ligne)[2]),
                        'O' : str(coordLigne(ligne)[2])[1:-1],
                        'N' : str(coordLigne(ligne)[3])[1:-1],
                        'E' : str(coordLigne(ligne)[4])[1:-1],
                        'S' : str(coordLigne(ligne)[5])[1:-1]}
            # dico_feat : c'est l'assemblage des autres dicos
            liste_dico_feat.append({'type' : 'Feature', 'properties' : dico_attr, 'geometry' : dico_geom})
        except:
            # les coord invalides sont deja prises en compte dans coordLigne
            pass
    # si pas de coordonn�es
    else:
        output.write(str(liste_lignes.index(ligne)) + '\t' + ligne[0] + '\tpas de coord\n')

# appel de la fonction qui �crit les dicos dans le geojson
print ('Ecriture du GeoJSON...')
ecritureGeoJSON(liste_dico_feat, geojson)
print (str(len(liste_lignes) - len(liste_dico_feat)) + '/' + str(len(liste_lignes)) +\
       " fichiers n'avaient pas de coordonnees ou des coordonnees invalides")
print (str(invalide) + " fichiers sur les " + str(len(liste_dico_feat)) + " restants avaient au moins une emprise invalide " \
    + " (et au moins une emprise valide qui a ete prise en compte)")
print ("(voir le log pour plus de details)")
print ("Fini!")

# ecrit les m�mes infos que sur la console dans le log
output.write ('\n' + '-' * 100)
output.write('\nBilan')
output.write ('\n' + '-' * 100)
output.write ('\n\n' + str(len(liste_lignes) - len(liste_dico_feat)) + '/' + str(len(liste_lignes)) +\
       " fichiers n'avaient pas de coordonnees ou des coordonnees invalides")
output.write ('\n' + str(invalide) + " fichiers sur les " + str(len(liste_dico_feat)) + " restants avaient au moins une emprise invalide " \
    + " (et au moins une emprise valide qui a ete prise en compte)")

# fermeture du log
output.close()



