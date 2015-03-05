(: déclaration des espaces de noms utilisés dans les balises qui nous intéressent :)
declare namespace gmd="http://www.isotc211.org/2005/gmd";
declare namespace gco="http://www.isotc211.org/2005/gco";
      
declare function local:recupVal($val)
  { if (empty($val) = true())
      then ''
      else if (empty($val/@codeListValue) = false())
        then data($val/@codeListValue)
        else data($val)};

declare function local:nomFichier($doc)
  { substring-after(base-uri($doc), '/')};

(: répertoire où sont stockés les fichiers XML :)
let $repertoire := "/home/julie/Bureau/geobolivia"
(: pour chaque fichier XML du répertoire :)
(: for $x in collection($repertoire)//gmd:MD_Metadata :)
(: ou pour travailler dans la BD ouverte dans BaseX :)
for $x in//gmd:MD_Metadata

  (: déclaration de b1, b2 etc. : les chemins vers les balises qui nous intéressent :)
  let $b1 := $x/gmd:fileIdentifier
  let $b2 := $x/gmd:identificationInfo/gmd:MD_DataIdentification/gmd:topicCategory/gmd:MD_TopicCategoryCode

  (: trie selon l'identifiant :)  
  order by $b1
  
  (: teste si c'est une métadonnée de service :)
  return if (not (index-of((in-scope-prefixes($x)), "srv")))
    (: si non, on récupère le contenu des balises :)
    then ( string-join( (concat('"', local:nomFichier($x)), local:recupVal($b1), local:recupVal($b2)), '";"'),text{'"&#10;'} )
    (: si oui, passe à la suivante :)
    else ()
    
   
