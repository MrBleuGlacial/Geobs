(: déclaration des espaces de noms utilisés dans les balises qui nous intéressent :)
declare namespace gmd="http://www.isotc211.org/2005/gmd";
declare namespace gco="http://www.isotc211.org/2005/gco";
declare namespace functx = "http://www.functx.com";

declare function local:recupVal($val)
  { if (empty($val) = true())
      then ''
      else if (empty($val/@codeListValue) = false())
        then data($val/@codeListValue)
        else data($val)};
        
(: fonction "officielle" utilisée pour trier :)
declare function functx:sort 
  ( $seq as item()* )  as item()* {
       
   for $item in $seq
   order by $item
   return $item
 } ;

(: répertoire où sont stockés les fichiers XML :)
(: let $repertoire := "/home/julie/ET/baguala/Extraction_XML/XML_20130402/geobrazil" :)
(:let $repertoire := "/home/julie/ET/baguala/Extraction_XML/XML_20130402/geocatalogue":)
(: let $repertoire := "/home/julie/ET/baguala/Extraction_XML/XML_20131028/argentine" :)
(: ou pour travailler dans la BD ouverte dans BaseX :)

let $liste_categ_tout := 
  (: pour chaque fichier XML du répertoire :)
  (: for $x in collection($repertoire)//gmd:MD_Metadata :)
  (: ou pour travailler dans la BD ouverte dans BaseX :)
  for $x in//gmd:MD_Metadata
    return (local:recupVal($x/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:topicCategory/gmd:MD_TopicCategoryCode))

let $liste_categ_distinct :=  functx:sort(distinct-values($liste_categ_tout))

  for $categ in $liste_categ_distinct
  
    return ( $categ, count(index-of($liste_categ_tout, $categ)), '&#xA;')

    