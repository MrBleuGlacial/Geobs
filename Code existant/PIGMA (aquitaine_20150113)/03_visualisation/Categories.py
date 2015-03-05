# -*- coding: iso-8859-1 -*-#!/usr/bin/python

###################################################
# Projet GEOBS
# Visualisation des cat�gories sous forme de graphique
# Version du 13/01/2015
#
# Ce script permet de voir les cat�gories ISO 19115
# renseign�es pour les fiches XML d'un g�ocatalogue,
# sous forme d'un graphique en barres horizontales.
# Le fichier de d�part de ce script est le r�sultat
# d'une requ�te XQuery
# Il est possible de :
# - cr�er le graph pour une ou + s�rie de donn�es
# - avoir en X le nb de fiches, ou le % de fiches
# - trier les cat par ordre croissant, suivant les
# valeurs pour un catalogue au choix
###################################################

###################################################
# Fichier CSV de d�part :
# - une ligne par fichier XML
# - une colonne (n'importe o�) avec les cat�gories
# renseign�es pour ce fichier XML
# Ex. :
# "7650.xml";"00-869";""
# "70102.xml";"0000fef7-7fa2-4a11-b405-073729177be9";"biota"
# "23351.xml";"0001c61c-ece7-4ef7-9d65-b87a9ee35f86";"boundaries";"imageryBaseMapsEarthCover";"planningCadastre";"structure"
# "22885.xml";"0001dbf0-7e42-4f1c-8474-98e7ca547449";"boundaries";"imageryBaseMapsEarthCover";"planningCadastre";"structure"
###################################################


########################
# Import de modules
########################

from __future__ import division

from pylab import *
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import datetime
import sys


########################
# VARIABLES A REMPLIR
########################

# emplacement des fichiers CSV de la base
liste_csv = ['//home//julie//Bureau//csv//categories.csv']
# etiquettes
liste_label = ['pigma']
# couleurs des barres ('b' pour bleu, 'r' pour rouge, 'g' pour vert)
liste_couleur = ['b']
# csv selon lequel trier les cat�gories (1 pour le 1er de liste_csv, etc.)
tri = '1'
# fichier log tenant compte du nb de fiches avec 0, 1, 2, etc. cat�gories remplies
log = '//home//julie//Bureau//csv//log_categories.csv'


########################
# VARIABLES A REMPLIR EVENTUELLEMENT
########################

# s�parateur utilis� par le fichier CSV
sep = ';'
# largeur des barres du graphique
width = 0.7
# oui si on veut des %, non si on veut des valeurs absolues
pc = 'oui'
# titre de l'axe des X et max de l'axe des X
if pc == 'non':
    titre_x = 'Nb fiches'
else:
    titre_x = '% fiches'
# titre de l'axe des Y
titre_y = 'Categories ISO 19115'
# liste des categories, avec leur traduction (ISO 19115)
dico_categ = {'farming' : 'agriculture',
              'biota' : 'biote',
              'boundaries' : 'limites',
              'climatologyMeeorologyAtmosphere' : u'climatologie/m\u00e9t\u00e9orologie/atmosph\u00e8re',
              'economy' : u'\u00e9conomie',
              'elevation' : 'altitude',
              'environment' : 'environnement',
              'geoscientificInformation' : u'informations g\u00e9oscientifiques',
              'health' : u'sant\u00e9',
              'imageryBaseMapsEarthCover' : 'imagerie/cartes de base/occupation des terres',
              'intelligenceMilitary' : 'renseignement/secteur militaire',
              'inlandWaters' : u'eaux int\u00e9rieures',
              'location' : 'localisation',
              'oceans' : u'oc\u00e9ans',
              'planningCadastre' : 'planification/cadastre',
              'society' : u'societ\u00e9',
              'structure' : 'structure',
              'transportation' : 'transport',
              'utilitiesCommunication' : u"services d'utilit\u00e9 publique/communication"}


########################
# V�rif des variables
########################

# le nombre d'�tiquettes doit correspondre au nombre de fichiers CSV
if len(liste_label) != len(liste_csv):
    print ("Le nombre d etiquettes dans liste_label ne correspond pas au nombre de fichiers CSV dans liste_csv")
    sys.exit()
# le nombre de couleurs doit correspondre au nombre de fichiers CSV
if len(liste_couleur) != len(liste_csv):
    print ("Le nombre de couleurs dans liste_couleur ne correspond pas au nombre de fichiers CSV dans liste_csv")
    sys.exit()
# le fichier selon lequel trier les valeurs doit exister dans la liste
if int(tri) > len(liste_csv):
    print ("Le fichier CSV selon lequel trier les valeurs (tri) n'existe pas")
    sys.exit()
    

########################
# Fonctions
########################

# A partir du fichier CSV, cr�e une liste de valeurs pour faire le graph
# Cette liste correspond aux nb d'occurrences de chaque cat�gorie
def prepaGraph(fichier, liste, pc):
    # Lecture du fichier en entr�e
    input = open(fichier, 'r')
    # Le fichier est stock� sous forme de liste, ligne par ligne
    liste_lignes = [i.rstrip() for i in input.readlines()]
    # r�cup�re le nb de fiches
    nb_fiches = len(liste_lignes)
    # cr�e une liste contenant autant d'�l�ments vides que de cat�gories ISO
    valeurs = [0] * len(liste)
    # pour chaque ligne du CSV
    for ligne in liste_lignes:
        # recherche pour chaque cat�gorie si elle est pr�sente
        for cat in liste:
            # si oui, la valeur pour cette cat�gorie augmente de 1
            if cat in ligne:
                valeurs[liste.index(cat)] = valeurs[liste.index(cat)] + 1
    # si on veut les %, recalcule les valeurs
    if pc == 'oui':
        valeurs = [i/nb_fiches*100 for i in valeurs]
    # cr�e une liste ou chaque �l�ment est un tuple (valeur, cat�gorie)
    l_val_cat = zip(valeurs, liste)
    # trie cette liste par ordre d�croissant de valeurs
    l_val_cat.sort(reverse = True)
    # retourne la liste tri�e
    return l_val_cat


# cr�e une liste o� chaque �l�ment correspond au nombre de cat d'une fiche
# ex. : [1,1,0,1,1,3,2,1] pour 8 fiches (8 �l�ments), la 6� a 3 cat renseign�es
def nbCat(fichier, sep):
    # Lecture du fichier en entr�e
    input = open(fichier, 'r')
    # Le fichier est stock� sous forme de liste, ligne par ligne
    liste_lignes = [i.rstrip() for i in input.readlines()]
    # La liste est transform�e en liste de liste, �l�ment par �l�ment
    liste_lignes = [i.split(sep) for i in liste_lignes]
    # on supprime les valeurs vides
    liste_lignes_nonvide = []
    for ligne in liste_lignes:
        ligne = [i for i in ligne[2:] if i != '""'] # les 2 1�res valeurs ne sont pas des cat
        liste_lignes_nonvide.append(ligne)
    # cr�e une liste correspondant aux nombres de cat renseign�es pour chaque ligne du CSV
    liste_nbcat = [len(i) for i in liste_lignes_nonvide]
    # retourne cette liste
    return liste_nbcat


# � partir d'une liste de nombre de cat, retourne le nombre d'occurrences de chaque
# nb de cat, au format CSV. Ex. : 0;412;79.4 pour indiquer que
# 412 fiches, soit 79.4% des fiches, ont 0 cat�gories renseign�es
def nbCatAnalyse(liste, fichier_sortie, num_cat):
    # cr�ation du fichier en sortie, en mode 'append' si d�j� existant
    output = open(fichier_sortie, 'a')
    # ajout d'un en-t�te avec la date
    output.write('-' * 30 + '\n')
    output.write(str(datetime.datetime.now()) + '\n')
    output.write('-' * 30 + '\n')
    # �criture du num du catalogue
    output.write(num_cat + '\n')
    # �criture des en-t�tes
    output.write('nb cat renseignees' + ';' + 'nb fiches' + ';' + '% fiches'  + '\n')
    # r�cup�ration du nb total de fiches
    tot = len(liste)
    # compte le nb de fiches avec 0, 1, 2... cat�gories renseign�es
    nb = [liste.count(i) for i in range(max(liste) + 1)]
    for i in range(max(liste) + 1):
        # �crit une ligne de type 0;412;79.4 dans le fichier de sortie
        output.write( str(i) + ';' + str(nb[i]) + ';' + str(nb[i]/tot*100) + '\n' )
    output.write('\n')
    # fermeture du fichier
    output.close()


# a partir d'une liste de cat�gories dans un certain ordre, et d'une liste de
# tuple(valeur, cat�gorie), sort la liste de valeurs dans le m�me ordre que
# la liste de cat�gories
def sortVal(categories, l):
    valeurs = []
    for cat in categories:
        for i in l:
            if cat in i:
                valeurs.append(i[0])
    return valeurs

    
########################
# Script
#######################

# Compte le nb de fiches avec 0, 1, 2... cat�gories renseign�es pour chaque catalogue
liste_nbcat = [nbCat(i, sep) for i in liste_csv]
liste_nb = [nbCatAnalyse(i, log, str(liste_nbcat.index(i) + 1)) for i in liste_nbcat]
# cr�e la liste des cat�gories en anglais � partir du dico
categories = dico_categ.keys()
# R�cup�re le nb d'occurrences de chaque cat�gorie
liste_l = [prepaGraph(i, categories, pc) for i in liste_csv]            
# les cat�gories sont tri�es selon le catalogue choisi
categories = [i[1] for i in liste_l[int(tri) - 1]]
# les valeurs pour les diff�rents catalogues sont tri�es selon la liste de cat�gories
liste_valeurs = [sortVal(categories, i) for i in liste_l]
# traduit les cat�gories pour le graphique, en fonction du dico
categories_translate = [dico_categ[cat] for cat in categories]

# cr�e la figure
fig = plt.figure(1)
ax = fig.add_subplot(111)
# valeurs de l'axe des Y
index_cat = [(categories.index(i)+1) * 3 for i in categories]
liste_index_cat = []
for i in range(len(liste_csv)):
    liste_index_cat.append([j - i*width for j in index_cat])
# max des X : 100% si on veut des %
if pc == 'oui':
    ax.set_xlim(0,100)

# cr�e une liste avec tous les graphiques
liste_p = [plt.barh(liste_index_cat[i], liste_valeurs[i], width, color = liste_couleur[i], align='center', label=liste_label[i]) for i in range(len(liste_valeurs))]
yticks(index_cat, categories_translate)

# cache les 'ticks' le long de l'axe des Y
plt.tick_params(\
    axis='y',          # changes apply to the xy-axis
    which='both',      # both major and minor ticks are affected
    left='off',      # ticks along the left edge are off
    right='off',         # ticks along the right edge are off
    labelleft='on') # labels along the left edge are on
# titre de l'axe des Y
ax.set_ylabel(titre_y)
# titre de l'axe des X
ax.set_xlabel(titre_x)
# la l�gende, dans le coin en haut � droite
leg = plt.legend(loc = 1)
# suppression du cadre autour de la l�gende
leg.draw_frame(False)
# montre la figure
plt.show()


