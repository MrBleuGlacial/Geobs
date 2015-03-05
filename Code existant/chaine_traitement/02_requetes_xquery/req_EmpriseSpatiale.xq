(: déclaration des espaces de noms utilisés dans les balises qui nous intéressent :)
declare namespace gmd="http://www.isotc211.org/2005/gmd";
declare namespace gco="http://www.isotc211.org/2005/gco";
declare namespace fra="http://www.cnig.gouv.fr/2005/fra";

declare function local:recupVal($val)
  { if (empty($val))
      then ''
      else data($val)};
      
declare function local:nomFichier($doc)
  { substring-after(base-uri($doc), '/')};
  
declare function local:concatCoord($seq1, $seq2, $seq3, $seq4)
  { for $i in (1 to count($seq1))
    return string-join(($seq1[$i], $seq2[$i], $seq3[$i], $seq4[$i]), ' ') };

(: répertoire où sont stockés les fichiers XML :)
let $repertoire :=  "/home/julie/Bureau/tests"
(: pour chaque fichier XML du répertoire :)
(: for $x in collection($repertoire)//gmd:MD_Metadata :)
(: ou pour travailler dans la BD ouverte dans BaseX :)
for $x in//gmd:MD_Metadata

  (: déclaration de b1, b2 etc. : les chemins vers les balises qui nous intéressent :)
  let $b1 := 
    $x/gmd:fileIdentifier
  let $b2 := 
    if (index-of((in-scope-prefixes($x)), "fra")) then
      for $coord in $x/gmd:identificationInfo/fra:FRA_DataIdentification/gmd:extent/gmd:EX_Extent/gmd:geographicElement/gmd:EX_GeographicBoundingBox/gmd:westBoundLongitude/gco:Decimal
             return local:recupVal($coord)
    else
      for $coord in $x/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:extent/gmd:EX_Extent/gmd:geographicElement/gmd:EX_GeographicBoundingBox/gmd:westBoundLongitude/gco:Decimal
             return local:recupVal($coord)
  let $b3 := 
    if (index-of((in-scope-prefixes($x)), "fra")) then
      for $coord in $x/gmd:identificationInfo/fra:FRA_DataIdentification/gmd:extent/gmd:EX_Extent/gmd:geographicElement/gmd:EX_GeographicBoundingBox/gmd:eastBoundLongitude/gco:Decimal
             return local:recupVal($coord)
    else
      for $coord in $x/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:extent/gmd:EX_Extent/gmd:geographicElement/gmd:EX_GeographicBoundingBox/gmd:eastBoundLongitude/gco:Decimal
             return local:recupVal($coord)
  let $b4 := 
    if (index-of((in-scope-prefixes($x)), "fra")) then
      for $coord in $x/gmd:identificationInfo/fra:FRA_DataIdentification/gmd:extent/gmd:EX_Extent/gmd:geographicElement/gmd:EX_GeographicBoundingBox/gmd:southBoundLatitude/gco:Decimal
             return local:recupVal($coord)
    else
      for $coord in $x/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:extent/gmd:EX_Extent/gmd:geographicElement/gmd:EX_GeographicBoundingBox/gmd:southBoundLatitude/gco:Decimal
             return local:recupVal($coord)
  let $b5 := 
     if (index-of((in-scope-prefixes($x)), "fra")) then
       for $coord in $x/gmd:identificationInfo/fra:FRA_DataIdentification/gmd:extent/gmd:EX_Extent/gmd:geographicElement/gmd:EX_GeographicBoundingBox/gmd:northBoundLatitude/gco:Decimal   
             return local:recupVal($coord)
     else
       for $coord in $x/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:extent/gmd:EX_Extent/gmd:geographicElement/gmd:EX_GeographicBoundingBox/gmd:northBoundLatitude/gco:Decimal   
             return local:recupVal($coord)  
             
  (: trie selon l'identifiant :)  
  order by $b1
  
  (: teste si c'est une métadonnée de service :)
  return if (not (index-of((in-scope-prefixes($x)), "srv")))
    (: si non, on récupère le contenu des balises :)
(:    then ( string-join( (concat('"', local:nomFichier($x)), local:recupVal($b1), local:recupVal($b2), local:recupVal($b3), local:recupVal($b4), local:recupVal($b5)), '";"'),text{'"&#10;'} ) :)
    then ( string-join( (concat('"', local:nomFichier($x)), local:recupVal($b1), local:concatCoord($b2, $b3, $b4, $b5)), '";"'),text{'"&#10;'} )
    (: si oui, passe à la suivante :)
    else ()
    
   
