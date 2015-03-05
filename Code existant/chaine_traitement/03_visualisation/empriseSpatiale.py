# -*- coding: iso-8859-1 -*-#!/usr/bin/python

###################################################
# Projet GEOBS
# Création d'un GEOJSON d'emprises spatiales à partir CSV
# Version du 13/01/2015
#
# Ce script crée un fichier GeoJSON à partir d'un
# fichier CSV contenant une liste d'emprises.
# Le fichier de départ de ce script est le résultat
# d'une requête XQuery.
#
# Le GeoJSON contient un polygone par fichier XML
# (donc un multipolygone si plusieurs emprises pour
# un même fichier XML), et 5 champs dans la table
# attributaire : file_name (nom du fichier XML)
# et les 4 coordonnées O, E, N et S.
###################################################

###################################################
# Structure du fichier GeoJSON en entrée :
# un dico "features" pour tout le fichier, qui contient :
# une liste de dico, dont chaque dico contient lui-même :
# un dico géométrie, un dico properties (attributs)
# et une clé 'type' de valeur 'feature'.
# Ex. :
# Features : [
# { dico_geom : {...}, dico_attr : {...}, 'type' : 'Feature'},  /polygone 1
# { dico_geom : {...}, dico_attr : {...}, 'type' : 'Feature'}   /polygone 2
# ...                                                           /etc.
# ]
# Le dico géométrie contient une clé 'type' (valeur
# MultiPolygon) et une clé 'coordinates'.
# Le dico d'attributs contient une clé par colonne.
###################################################

###################################################
# Fichier CSV de départ : 3 colonnes
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

# emplacement du fichier CSV de départ (ex. : "c://Travail//geobs//emprise_spatiale.csv")
fichier = '//home//julie//Bureau//csv//emprise_spatiale.csv'
# nom et emplacement du fichier GeoJSON qui sera créé (ex. : "c://Travail//geobs//emprise_spatiale.geojson")
geojson = '//home//julie//Bureau//geojson//emprise_spatiale.geojson'
# nom et emplacement du log qui sera créé (ex. : "c://Travail//geobs//emprise_spatiale.txt")
log = '//home//julie//Bureau//geojson//emprise_spatiale.txt'


########################
# VARIABLES A REMPLIR EVENTUELLEMENT
########################

# séparateur du fichier CSV
sep = ';'
# nom du champ qui contiendra le nom du fichier XML
champ_nom = 'file_name'
# nom du champ qui contiendra le nombre de polygones de l'entité (qui peut être un multipolygone)
champ_nb_polyg = 'nb'
# compte le nb de fichiers pour lesquels au moins une emprise est invalide (et au moins une valide)
# doit être égal à zéro
invalide = 0


########################
# Fonctions
########################

# Pour écrire les dicos dans le fichier GeoJSON comme il faut
def ecritureGeoJSON(liste_dico, fichier):
    # ouverture du geojson en écriture
    output = open(fichier, 'w')
    # écriture des 1ères lignes
    output.write('{\n"type": "FeatureCollection",\n\n"features": [\n')
    # écrit tous les dicos de la liste sauf le dernier, séparés par des ","
    for i in liste_dico[:-1]:
        output.write(str(i))
        output.write('\n,\n')
    # écrit le dernier dico de la liste
    output.write(str(liste_dico[-1]))
    # écrit les dernières lignes
    output.write('\n\n]\n}')
    # Fermeture du fichier geojson
    output.close()

# Fonction pour récupérer les coordonnées des polygones à partir des 4 coord des emprises
def coordLigne(ligne):
    global invalide
    # initialise les coordonnées
    coordinates = []
    liste_O = []
    liste_N = []
    liste_E = []
    liste_S = []
    # pour chaque jeu de coordonnées d'une ligne
    for i in ligne[2:]:
        try:
            # on sépare les 4 coordonnées
            l = i.split(' ')
            # puis on les récupère, en supprimant les "" et en remplaçant les , par des .
            O = float(l[0][1:].replace(',','.'))
            N = float(l[3][:-1].replace(',','.'))
            E = float(l[1].replace(',','.'))
            S = float(l[2].replace(',','.'))
            # si les coord sont correctes
            if (-180 <= O <= 180) and (-180 <= E <= 180) and (-90 <= N <= 90) and (-90 <= S <= 90):
                # on ajoute l'ouest à la liste des coord ouest, etc. (utile si plusieurs emprises)
                liste_O.append(O)
                liste_N.append(N)
                liste_E.append(E)
                liste_S.append(S)
                # les coordonnées des 4 points
                ON = [ O, N ]
                EN = [ E, N ]
                ES = [ E, S ]
                OS = [ O, S ]
                # il faut 5 jeux de coordonnées pour fermer le rectangle
                coordinate = [[ON, EN , ES, OS, ON]]
                # ajout du jeu de coord à la liste
                coordinates.append(coordinate)
            # si les coordonnées sont incorrectes
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
    # retourne la liste des jeux de coord, le type de géom et les 4 coord
    return coordinates, type_geom, liste_O, liste_N, liste_E, liste_S

        
########################
# Script
#######################

# Lecture du fichier en entrée
print ('Lecture fichier CSV...')
input = open(fichier, 'r')
# Le fichier est stocké sous forme de liste, ligne par ligne
print ('Stockage des valeurs...')
liste_lignes = [i.rstrip() for i in input.readlines()]
# Fermeture du fichier en entrée
input.close()
# séparation des différents éléments de chaque ligne : on obtient une liste de liste
liste_lignes = [i.split(sep) for i in liste_lignes]
# création et remplissage des 3 dicos nécessaires pour le geojson
print ('Preparation du GeoJSON...')
liste_dico_feat = []
# ouverture du log en écriture
output = open(log, 'w')
# ajout d'un en-tête avec la date, le nom du script et le nom du fichier en entrée dans le log
output.write('-' * 100 + '\n')
output.write(str(datetime.datetime.now()) + '\n')
output.write('Execution du script empriseSpatiale.py\n')
output.write('Fichier en entree : ' + fichier + '\n')
output.write('-' * 100 + '\n\n')
# ajout des en-têtes de colonne
output.write('num_ligne\tfichier\tprobleme\tcoord\n')
# pour chaque ligne du CSV, = pour chaque fichier XML
for ligne in liste_lignes:
    # on prend en compte uniquement les lignes avec au moins un jeu de coord
    if len(coordLigne(ligne)[2]) > 0:
        try:
            # dico_geom
            dico_geom = {'type' : (coordLigne(ligne))[1], 'coordinates' : (coordLigne(ligne))[0]}
            # dico_attr : récupération des champs : nom du fichier, coordonnées
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
    # si pas de coordonnées
    else:
        output.write(str(liste_lignes.index(ligne)) + '\t' + ligne[0] + '\tpas de coord\n')

# appel de la fonction qui écrit les dicos dans le geojson
print ('Ecriture du GeoJSON...')
ecritureGeoJSON(liste_dico_feat, geojson)
print (str(len(liste_lignes) - len(liste_dico_feat)) + '/' + str(len(liste_lignes)) +\
       " fichiers n'avaient pas de coordonnees ou des coordonnees invalides")
print (str(invalide) + " fichiers sur les " + str(len(liste_dico_feat)) + " restants avaient au moins une emprise invalide " \
    + " (et au moins une emprise valide qui a ete prise en compte)")
print ("(voir le log pour plus de details)")
print ("Fini!")

# ecrit les mêmes infos que sur la console dans le log
output.write ('\n' + '-' * 100)
output.write('\nBilan')
output.write ('\n' + '-' * 100)
output.write ('\n\n' + str(len(liste_lignes) - len(liste_dico_feat)) + '/' + str(len(liste_lignes)) +\
       " fichiers n'avaient pas de coordonnees ou des coordonnees invalides")
output.write ('\n' + str(invalide) + " fichiers sur les " + str(len(liste_dico_feat)) + " restants avaient au moins une emprise invalide " \
    + " (et au moins une emprise valide qui a ete prise en compte)")

# fermeture du log
output.close()



