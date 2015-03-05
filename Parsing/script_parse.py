# -*- coding: cp1252 -*-
from collections import defaultdict

#Codes ASCII du champ majuscule
valLetterMinUpp = 65
valLetterMaxUpp = 90
valLetterMinLow = 97
valLetterMaxLow = 122
valNumberMin = 48
valNumberMax = 57


#Fichier à parser
lineage = open("lineage_res","r")
#Hashmap des mots commençant par une majuscule
lineagedico = {}

for line in lineage:
    splitline = line.split()
    #print splitline
    for word in splitline:
        #print word
        # --- traiter ici le mot --- #
        fstchar = ord(word[0])
        lstchar = ord(word[len(word)-1])
        #print word
        #print word[len(word)-1]
        if (valLetterMinUpp <= fstchar <= valLetterMaxUpp):
            if (valLetterMinLow > lstchar or lstchar > valLetterMaxLow) and (valLetterMinUpp > lstchar or lstchar > valLetterMaxUpp) and (valNumberMin > lstchar or lstchar > valNumberMax):
                #print 'avant :' + word
                word = word[:len(word)-1]
                #print 'après :' + word
            lineagedico[word] = lineagedico.get(word,0)+1
lineage.close()

listkey = lineagedico.keys()

fichier = open("list_uppercase_words","w")
for key in listkey:
    if(lineagedico[key] >= 6):
        fichier.write(key + ' : ' + str(lineagedico[key]) + '\n')
print 'ENDED'

fichier.close()
