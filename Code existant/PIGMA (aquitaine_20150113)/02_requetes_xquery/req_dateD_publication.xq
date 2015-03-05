(: déclaration des espaces de noms utilisés dans les balises qui nous intéressent :)
declare namespace gmd="http://www.isotc211.org/2005/gmd";
declare namespace gco="http://www.isotc211.org/2005/gco";
declare namespace functx = "http://www.functx.com";

(: fonction "officielle" utilisée pour trier les dates :)
declare function functx:sort 
  ( $seq as item()* )  as item()* {
       
   for $item in $seq
   order by $item
   return $item
 } ;
      
(: fonction pour extraire l'année de la date : les 4 1ers caractères :)  
declare function local:annee($item)
  { substring($item, 1, 4) };

(: fonction pour extraire le mois de la date : les 6è et 7è caractères :)
declare function local:mois($item)
  { substring($item, 6, 2) };

(: répertoire où sont stockés les fichiers XML :)
let $repertoire := "/media/Donnees/Travail/Baguala/geobolivia"

(: définit la variable liste_annee :)
let $liste_annee :=
  (: pour chaque fichier XML du répertoire :)
  (: for $x in collection($repertoire)//gmd:MD_Metadata :)
  (: ou pour travailler dans la BD ouverte dans BaseX :)
  for $x in//gmd:MD_Metadata
    (: on récupère pour chaque date :)
    return for $item in ($x/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:citation/gmd:CI_Citation/gmd:date/gmd:CI_Date/gmd:date)
      where $x/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:citation/gmd:CI_Citation/gmd:date/gmd:CI_Date/gmd:dateType/gmd:CI_DateTypeCode/@codeListValue = "publication"
      (: l'année et le mois :)
      return ( concat(local:annee($item), '-', local:mois($item)))
 
(: définition d'une liste contenant toutes les combinaisons uniques de mois et d'année, triées :)
let $liste_sort :=  functx:sort(distinct-values($liste_annee))
  (: pour chacune des valeurs de cette liste :)
  for $value in $liste_sort
    (: on récupère l'année, le mois, et le nombre de fois où la combinaison apparaît dans liste_annee :)
    return ( string-join( (local:annee(string($value)), local:mois($value), string(count(index-of($liste_annee, $value)))), ';'),text{'&#10;'} )
    