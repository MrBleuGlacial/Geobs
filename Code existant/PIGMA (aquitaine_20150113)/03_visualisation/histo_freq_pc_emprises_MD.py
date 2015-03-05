# -*- coding: iso-8859-1 -*-#!/usr/bin/python

###################################################
# Projet GEOBS
# Visualisation des histo de fr�quences des superpositions d'emprises
# Version du 13/01/2015
#
# un script pour visualiser les histo de fr�quences
# � partir d'un fichier CSV AVEC EN-TETES.
# Possibilit� de :
# - faire le graph pour un des pays au choix, ou pour les 3
# - faire le graph en cumul� ou non
# - avoir un axe des Y avec les % ou les nb
# - avoir un graphique de plusieurs couleurs, suivant
# des bornes et des couleurs d�finies par l'utilisateur
###################################################

###################################################
# Fichier CSV de d�part : 3 colonnes
# - 1�re colonne : les valeurs de 1 � nb max emprises superpos�es
# - 2� colonne : le nb de rectangles avec cette valeur
# Ex. :
# val,nb_val
# 1,1
# 2,2
# 3,15
# 4,24
###################################################


########################
# Import de modules
########################

from __future__ import division
import matplotlib.pyplot as plt
import numpy as np
import sys


########################
# VARIABLES A REMPLIR
########################

# emplacement des fichiers CSV de la base
# ex. : ['//home//julie//geojson//emprise1_nb.csv','//home//julie//geojson//emprise2_nb.csv']
liste_csv = ['//home//julie//Bureau//geojson//pigma_aplat_histogramme.csv']
# �tiquettes (ex. : ['pigma','geopal'])
liste_label = ['pigma']


########################
# VARIABLES A REMPLIR EVENTUELLEMENT
########################

# s�parateur utilis� par le fichier CSV
sep = ','
#largeur des barres du graphiques
width = 1.0
# graph cumul� ou non
cumule = 'oui'
# graph en nb ('non') ou en % ('oui')
pc = 'oui'
# titre de l'axe des Y
if pc == 'oui':
    titre_y = "% d'occurrences"
else:
    titre_y = "Nb d'occurrences"
# titre de l'axe des X
titre_x = u"Nombre d'emprises superpos\u00e9es"
# graph d'une seule couleur, ou de plusieurs couleurs suivant des bornes
multicouleur = 'non'
# dans le cas o� les graphiques sont monocouleur :
if multicouleur == 'non':
    # liste des couleurs, autant que de CSV (ex. : ['b','g'])
    liste_couleur = ['b']
# dans les cas o� les graphiques sont multicolores :
else:
    # liste des limites o� changer de couleur
    # liste de listes, un �l�ment par CSV, et dans chaque �l�ment plusieurs bornes
    # 1�re borne  = min, derni�re borne = max
    # ex. : [[1,16,30,198,224,230,250,268,296,318], [1,3,9,17,22,30,42,48,51]]
    liste_bornes = [[1,100,200,350]]
    # liste des couleurs, une de moins que de bornes donc
    # ex. : [['#F7FBFF','#DEEBF7','#C7DCEF','#A2CCE2','#72B4D7', '#4997C9','#2878B8','#0D57A1','#08306B'], ['#F7FCF5', '#E5F5E0', '#A5DA9F', '#7AC77B','#4AAF61', '#29924A', '#077331', '#00441B']]
    liste_multicouleur = [['r','g','b']]


########################
# V�rif variables
########################

# variable pc
if pc not in ['oui', 'non']:
    print ('la variable "pc" est mal definie')
    sys.exit()
# variable cumule
if cumule not in ['oui', 'non']:
    print ('la variable "cumule" est mal definie')
    sys.exit()
if multicouleur not in ['oui', 'non']:
    print ('la variable "multicouleur" est mal definie')
    sys.exit()
# longueur des listes
if len(liste_csv) != len(liste_label):
    print ('le nb d etiquettes dans liste_label ne correspond pas au nb de fichier csv dans liste_csv')
    sys.exit()
if multicouleur == 'non' and len(liste_couleur) != len(liste_csv):
    print ('le nombre de couleurs dans liste_couleur ne correspond pas au nb de fichiers csv dans liste_csv')
    sys.exit()
if multicouleur == 'oui' and (len(liste_bornes) != len(liste_csv) or len(liste_multicouleur) != len(liste_csv)):
    print ('le nombre de bornes dans liste_bornes ou de couleurs dans liste_multicouleur ne correspond pas au nb de fichiers csv dans liste_csv')
    sys.exit()


########################
# Fonctions
########################

# Fonction pour lire le fichier CSV et en sortir 2 liste
# une pour le nb d'emprises superpos�es : 1�re colonne (liste_val)
# et une pour le nb d'occurrences de ce nb d'emprises : 2� colonne (liste_nbval)
def prepaGraph(fichier):
    # Lecture du fichier en entr�e
    input = open(fichier, 'r')
    # Le fichier est stock� sous forme de liste, ligne par ligne
    liste_lignes = [i.rstrip() for i in input.readlines()]
    # Chaque �l�ment de la liste(= ligne) est s�par� en 2
    liste_lignes = [i.split(sep) for i in liste_lignes]
    # la 1�re liste est donc constitu�e de la 1�re colonne, sans l'en-t�te
    liste_val_X = [int(i[0]) for i in liste_lignes[1:]]
    # et la 2�me de la 2�me colonne, sans l'en-t�te
    liste_val_Y = [int(i[1]) for i in liste_lignes[1:]]
    # si on veut des %
    if pc == 'oui':
        liste_val_Y = [i/sum(liste_val_Y)*100 for i in liste_val_Y]
    # si graph cumul�
    if cumule == 'oui':
        liste_val_Y_cumule = []
        total = 0
        for item in liste_val_Y:
            total = total + item
            liste_val_Y_cumule.append(total)
        liste_val_Y = liste_val_Y_cumule            
    # retourne les 2 listes, valeurs et nb d'occurrence
    return liste_val_X, liste_val_Y


# transforme une liste de couleurs et de valeurs de bornes en  liste
# de couleur pour chacune des barres du graphique
def multiCouleur(valeurs, bornes, liste_couleur):
    # pour trouver les valeurs correspondantes dans la liste de valeur (approx.)
    bornes = [min(valeurs, key=lambda x:abs(x-i)) for i in bornes]
    # trouve la position des ces limites de classe
    bornes = [valeurs.index(i) for i in bornes]
    # fait la soustraction de i - (i-1) : passe de [0,25,100] � [25,75] par ex.
    bornes = [i - bornes[bornes.index(i)-1] for i in bornes[1:]]
    # assigne les couleurs aux barres
    couleur = []
    for i, j in zip(liste_couleur, bornes):
        couleur = couleur + [i]*j
    # retourne la liste de couleurs, un �l�ment par barre du graphique
    return couleur


########################
# Script
########################

# r�cup�re les valeurs avec la fonction prepaGraph
liste_val_X = [prepaGraph(csv)[0] for csv in liste_csv]
liste_val_Y = [prepaGraph(csv)[1] for csv in liste_csv]
# d�finit les max des axes en fonction du ou des pays choisis
xmax = max(map(max,liste_val_X))
ymax = max(map(max,liste_val_Y))
# Fait appel � la fonction multiCouleur si tel est le souhait de l'utilisateur
if multicouleur == 'oui':
    liste_couleur = [multiCouleur(liste_val_X[i], liste_bornes[i], liste_multicouleur[i]) for i in range(len(liste_csv))]
# cr�e la figure
fig = plt.figure(1)
ax = fig.add_subplot(111)
# d�finit les max pour les axes X et Y
ax.set_xlim(0,xmax)
ax.set_ylim(0,ymax)
# cr�e le(s) graphique(s)
liste_p = [plt.bar(liste_val_X[i], liste_val_Y[i], width, color = liste_couleur[i], edgecolor = 'none', label = liste_label[i]) for i in range(len(liste_csv))]
# titre de l'axe des Y
ax.set_ylabel(titre_y)
# titre de l'axe des X
ax.set_xlabel(titre_x)
# la l�gende, 9 pour au milieu en haut, 2 pour en haut � gauche...
leg = plt.legend(loc = 2)
# suppression du cadre autour de la l�gende
leg.draw_frame(False)
# montre le graphique
plt.show()

