# -*- coding: iso-8859-1 -*-#!/usr/bin/python

###################################################
# Projet GEOBS
# Date de création et publication des données sous forme de graphique
# Version du 13/01/2015
#
# Ce script permet de voir le nombre de données
# créées et publiées au fil du temps,
# pour un seul géocatalogue à la fois,
# à partir de fichiers CSV.
#
# Les min et max des axes des dates sont toujours
# définis en fonction des valeurs min et max de chaque catalogue.
#
# Les min et max en Y (nb de fiches) sont définis
# en fonction du catalogue représenté.
#
# Possibilité de :
# - faire un graphique cumulé ou non cumulé
# - choisir le nombre de séries de données
###################################################

###################################################
# Fichier CSV de départ : 3 colonnes
# - 1ère colonne : année
# - 2è colonne : mois
# - 3è colonne : nb de données publiées ou créées
# Ex. :
# 1901;01;42
# 1974;01;3
# 1976;01;1
# 1979;12;1
###################################################


########################
# Import de modules
########################

from pylab import *
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
import datetime
import itertools


########################
# VARIABLES A REMPLIR
########################

# emplacement des fichiers CSV de la base
liste_csv_crea = ['//home//julie//Bureau//csv//dateD_creation.csv']
liste_csv_publi = ['//home//julie//Bureau//csv//dateD_publication.csv']
# etiquettes
liste_label = ['pigma']
# couleur du graph (noms HTML par ex.) ('Cyan', 'Blue', 'Red, 'DarkRed', LawnGreen', 'DarkGreen')
liste_couleur_crea = ['Cyan']
liste_couleur_publi = ['Blue']


########################
# VARIABLES A REMPLIR EVENTUELLEMENT
########################

# séparateur utilisé par le fichier CSV
sep = ';'
# cumulatif ou non
cumul = 'non'
# titre de l'axe des Y
titre_y = 'Nb fiches'
# titre de l'axe des X
titre_x = 'Date'
# type de graph : o pour un nuage de points
type_crea = 'o'
type_publi = 'o'


########################
# Vérif variables
########################

# variable cumul
if cumul not in ['oui', 'non']:
    print ('la variable "cumul" est mal definie')
    sys.exit()
# autant de csv creation que publication
if len(liste_csv_crea) != len(liste_csv_publi):
    print ('le nombre de fichiers csv pour les dates de creation ne correspond pas au nombre de fichiers csv pour les dates de publication')
    sys.exit()
# autant d'etiquettes que de fichiers csv
if len(liste_label) != len(liste_csv_crea):
    print ('le nombre d etiquettes (liste_label) ne correspond pas au nombre de fichiers csv')
    sys.exit()
# autant de couleurs que de csv
if len(liste_couleur_crea) != len(liste_csv_crea) or len(liste_couleur_publi) != len(liste_csv_crea):
    print ('le nombre de couleurs ne correspond pas au nombre de fichier csv')
    sys.exit()


########################
# Fonctions
########################

def prepaGraph(fichier, nettoyage):
# Lecture du fichier en entrée
    input = open(fichier, 'r')
    # Le fichier est stocké sous forme de liste, ligne par ligne
    liste_lignes = [i.rstrip() for i in input.readlines()]
    # La liste est transformée en liste de liste, élément par élément
    liste_lignes = [i.split(sep) for i in liste_lignes]
    # si dates à nettoyer (brésil)
    if nettoyage == 'oui':
        liste_date = [i[0] for i in liste_lignes]
        liste_nb = [i[1] for i in liste_lignes]
        liste_annees = nettoyageDates(liste_date, liste_nb)[0]
        liste_mois = nettoyageDates(liste_date, liste_nb)[1]
        liste_nb = nettoyageDates(liste_date, liste_nb)[2]
        liste_lignes = []
        for i in range(len(liste_annees)):
            liste_lignes.append([liste_annees[i], liste_mois[i], liste_nb[i]])
    # supprime les lignes n'ayant pas les 3 éléments remplis
    liste_lignes = [i for i in liste_lignes if len(i) == 3]
    # supprime les lignes où au moins un des 3 éléments (année, mois, nb) n'est pas un nombre
    liste_lignes = [i for i in liste_lignes if i[0].isdigit() and i[1].isdigit() and i[2].isdigit()]
    # vérif sur mois et année
    liste_lignes = [i for i in liste_lignes if int(i[0]) in range(1700, datetime.date.today().year) and int(i[1]) in range(1,13)]
    # crée un dico vide
    dico = {}

    # crée une liste des dates à partir de la 1ère et la 2ème colonne du fichier CSV (année et mois)
    dico['dates'] = [datetime.date( int(i[0]), int(i[1]), 1) for i in liste_lignes]
    # crée une liste des nb de métadonnées à partir de la 3ème colonne du fichier CSV
    nb = [int(i[2]) for i in liste_lignes]
    # si le graph doit être cumulatif
    if cumul == 'oui':
        # la valeur en Y sera le nb de fiches créées ou publiées jusqu'à cette année-là y compris
        dico['nb'] = [sum(nb[:i+1]) for i in range(len(nb))]
    # si le graph est non cumulatif
    else:
        # la valeur en Y sera simplement le nb de fiches créées ou publiées cette année-là
        dico['nb'] = nb
    # retourne le dico
    return dico


# prend une liste de dates et en sort le mois et l'année (pour le Brésil)
def nettoyageDates(liste_date, liste_nb):
    annee = []
    mois = []
    nb = []
    for i in liste_date:
        # type 31/12/2010 ou 31-12-2010
        if len(i) == 10:
            annee.append(i[6:])
            mois.append(i[3:5])
            nb.append(liste_nb[liste_date.index(i)])
        # type 12-2010 ou 12/2010
        elif len(i) == 7:
            annee.append(i[3:])
            mois.append(i[:2])
            nb.append(liste_nb[liste_date.index(i)])
        # type 1891-01-16T00:00:00;1
        elif len(i) == 21:
            annee.append(i[:4])
            mois.append(i[5:7])
            nb.append(liste_nb[liste_date.index(i)])
        # type 2010
        elif len(i) == 4:
            annee.append(i)
            mois.append('')
            nb.append(liste_nb[liste_date.index(i)])
        # type 20041130
        elif len(i) == 8 and '-' not in i:
            annee.append(i[:4])
            mois.append(i[4:6])
            nb.append(liste_nb[liste_date.index(i)])
        # type 01-01-09
        elif len(i) == 8 and '-' in i:
            if int(i[6:]) <= datetime.date.today().year - 2000:
                annee.append('20' + i[6:])
            else:
                annee.append('19' + i[6:])
            mois.append(i[3:5])
            nb.append(liste_nb[liste_date.index(i)])
                            
    return annee, mois, nb
        
    
########################
# Script
########################

# appel de la fonction de mise en forme des données
liste_dico_crea = [prepaGraph(i, 'non') for i in liste_csv_crea]
liste_dico_publi = [prepaGraph(i, 'non') for i in liste_csv_publi]

# création de la figure vide
fig = plt.figure(1)
ax = fig.add_subplot(111)
# ajout des graphs
liste_graph_crea = [plt.plot(liste_dico_crea[i]['dates'], liste_dico_crea[i]['nb'], type_crea, color = liste_couleur_crea[i], label = 'creation ' + liste_label[i]) for i in range(len(liste_csv_crea))]
liste_graph_publi = [plt.plot(liste_dico_publi[i]['dates'], liste_dico_publi[i]['nb'], type_publi, color = liste_couleur_publi[i], label = 'publication ' + liste_label[i]) for i in range(len(liste_csv_publi))]

# titre de l'axe des Y
ax.set_ylabel(titre_y)
# titre de l'axe des X
ax.set_xlabel(titre_x)
# intervalle axe des X
ax.xaxis_date()
# définit les min et max de l'axe des X, en fonction des min et max des différents csv
liste_date_publi = [i for i in itertools.chain.from_iterable([j['dates'] for j in liste_dico_publi])]
date_min_publi = min(liste_date_publi)
date_max_publi = max(liste_date_publi)
liste_date_crea = [i for i in itertools.chain.from_iterable([j['dates'] for j in liste_dico_crea])]
date_min_crea = min(liste_date_crea)
date_max_crea = max(liste_date_crea)
date_min = min(date_min_publi, date_min_crea)
date_max = max(date_max_publi, date_max_crea)

# applique ces min et max
ax.set_xlim(date_min, date_max)
# Applique le format des dates
ax.xaxis.set_major_locator(mdates.YearLocator(25))
# Pour avoir les dates en diagonale (optionnel)
##fig.autofmt_xdate()
# placement de la légende : en haut à gauche
leg = plt.legend(loc = 2, frameon = None)
# suppression du cadre de la légende
leg.draw_frame(False)
leg.set_frame_on = False
leg.get_frame().set_alpha(0)

# affichage de la figure
plt.show()


