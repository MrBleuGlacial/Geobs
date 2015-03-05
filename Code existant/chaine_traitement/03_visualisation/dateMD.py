# -*- coding: iso-8859-1 -*-#!/usr/bin/python

###################################################
# Projet GEOBS
# Visualisation des dates de métadonnées sous forme de graphique
# Version du 13/01/2015
#
# Ce script permet de voir le nombre de métadonnées
# créées au fil du temps pour plusieurs géocatalogues,
# à partir de fichiers CSV, sous forme d'une
# courbe cumulée. 
###################################################

###################################################
# Fichier CSV de départ : 3 colonnes
# - 1ère colonne : année
# - 2è colonne : mois
# - 3è colonne : nb de métadonnées créés
# Ex. :
# 2004;04;3
# 2005;03;3
# 2008;11;2
###################################################


########################
# Import de modules
########################

from pylab import *
import matplotlib.pyplot as plt

import matplotlib.ticker as ticker
from matplotlib.dates import DateFormatter
import datetime


########################
# VARIABLES A REMPLIR
########################

# emplacement des fichiers CSV de la base (ex. : ['//home//julie//csv//dateMD_1.csv','//home//julie//csv//dateMD_2.csv']
# cette liste peut contenir 1 ou + fichiers CSV
liste_csv = ['//home//julie//Bureau//csv//dateD_creation.csv']
# etiquettes (ex. : ['pigma','geopal']
# cette liste doit contenir autant d'elements que liste_csv
liste_label = ['pigma']
# couleurs des courbes (ex. : ['b','g']) ('b' pour bleu, 'r' pour rouge, 'g' pour vert...)
# cette liste doit contenir autant d'elements que liste_csv
liste_couleur = ['b']


########################
# VARIABLES A REMPLIR EVENTUELLEMENT
########################

# séparateur utilisé par le fichier CSV
sep = ';'
# liste cumulative du nb de MD créées par année (doit etre vide)
nb_cumul = []
# titre de l'axe des Y
titre_y = 'Nb fiches cumule'
# titre de l'axe des X
titre_x = 'Date'
# Format des dates
format_date = DateFormatter('%Y')


########################
# Fonctions
########################

# A partir du fichier CSV, crée un dico pour faire le graph
# Le dico contient 2 clé : une qui stocke la liste des dates uniques, classées
# et une qui stocke le nb de MD cumulé pour chacune de ces dates, dans le même ordre
def prepaGraph(fichier):
# Lecture du fichier en entrée
    input = open(fichier, 'r')
    # Le fichier est stocké sous forme de liste, ligne par ligne
    liste_lignes = [i.rstrip() for i in input.readlines()]
    # La liste est transformée en liste de liste, élément par élément
    liste_lignes = [i.split(sep) for i in liste_lignes]
    # crée un dico vide
    dico = {}
    # crée une liste des dates à partir de la 1ère et la 2ème colonne du fichier CSV
    dico['dates'] = [datetime.date( int(i[0]), int(i[1]), 1) for i in liste_lignes]
    # crée une liste des nb de métadonnées à partir de la 3ème colonne du fichier CSV
    nb = [int(i[2]) for i in liste_lignes]
    # crée une liset cumulative des nb de métadonnées
    dico['nb_cumul'] = [sum(nb[:i+1]) for i in range(len(nb))]
    # retourne le dico créé
    return dico

# crée une série de dates à un an d'intervalle, entre 2 dates
def serieDates(debut, fin):
    # l'intervalle : un an en secondes
    step = datetime.timedelta(seconds=31536000)
    serie = []
    while debut < fin:
        serie.append(debut.strftime('%Y-%m-%d %H:%M:%S'))
        debut = debut + step
    return serie


########################
# Script
########################

# Création des dicos et graphs pour chacun des catalogues
fig = plt.figure(1)
ax = fig.add_subplot(111)
liste_dico = [prepaGraph(i) for i in liste_csv]
liste_p = [plt.plot(liste_dico[i]['dates'], liste_dico[i]['nb_cumul'], liste_couleur[i], label = liste_label[i]) for i in range(len(liste_csv))]
# titre de l'axe des Y
ax.set_ylabel(titre_y)
# titre de l'axe des X
ax.set_xlabel(titre_x)
# Applique le format des dates
ax.xaxis.set_major_formatter(format_date)
# pour afficher les dates sur l'axe des X en diagonale (optionnel)
##fig.autofmt_xdate()
# définit les min et max de l'axe des X (sinon sont définis en fonction valeurs)
##date_min = datetime.datetime(2002,5,1)
##date_max = datetime.datetime(2013,4,1)
##ax.set_xlim(date_min, date_max)
# la légende, dans le coin en haut à gauche
leg = plt.legend(loc = 2)
# suppression du cadre autour de la légende
leg.draw_frame(False)

plt.show()


