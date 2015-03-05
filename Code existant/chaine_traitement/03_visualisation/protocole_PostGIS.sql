-- Requêtes PostGIS pour transformer la couche d'emprises métadonnées
-- en couche "à plat", avec pour chaque polygone le nombre d'emprises superposées


----------------
-- Couche de base
----------------

-- issue : requête XQuery + script Python
-- avec colonne géométrie :
-- geom
-- et colonne id :
-- gid (facultatif)


--------------------------
-- 1/ multipart to singlepart
-- Départ : <multipart>
-- Résultat : <singlepart>
--------------------------

CREATE TABLE <singlepart> AS
SELECT (ST_Dump(geom)).geom FROM <multipart>;

ALTER TABLE <singlepart>
ADD COLUMN gid SERIAL PRIMARY KEY;

select populate_geometry_columns();


--------------------------
-- 2/ Union
-- Départ : <singlepart>
-- Résultat : <a_plat>
--------------------------

-- http://gis.stackexchange.com/questions/83/separate-polygons-based-on-intersection-using-postgis

CREATE TABLE <a_plat> AS
SELECT geom FROM ST_Dump((
    SELECT ST_Polygonize(geom) AS geom FROM (
        SELECT ST_Union(geom) AS geom FROM (
            SELECT ST_ExteriorRing(geom) AS geom FROM <singlepart>) AS lines
        ) AS noded_lines
    )
);

--------------------------
-- 3/ Ajoute clé primaire
-- couche depart : <a_plat>
--------------------------

ALTER TABLE <a_plat>
ADD COLUMN gid SERIAL PRIMARY KEY;

select populate_geometry_columns();


-----------------------------
-- 3 bis/ Vérifier la topologie
-- Départ : <a_plat>
-- Résultat : <topo_ok>
-----------------------------

select st_isvalidreason(geom), gid
from <a_plat>
where st_isvalid(geom) = false
order by st_isvalidreason;

-- S il y a des erreurs :

create table <topo_ok> as
select the_geom, st_isvalidreason(the_geom), gid from <a_plat>
where st_isvalid(the_geom) = true;


----------------------------------------------------------------------------------
-- 4/ crée un tableau contenant pour chaque rect de la couche à plat
-- le nb de rect de la couche sp l intersectant
-- Départ : <singlepart>, <a_plat>
-- S'il y avait des erreurs de topologie, remplacer <a_plat> par <topo_ok>
-- Résultat : <tab_nb_a_plat> (table)
----------------------------------------------------------------------------------

create table <tab_nb_a_plat> as
select aplat_id, count(*) as nb from (
select  sp.gid,  aplat.gid as aplat_id
from <a_plat> as aplat, <singlepart> as sp
where st_within(aplat.geom,sp.geom)) as derivedTable
group by aplat_id
order by aplat_id;


--------------------------------------
-- 5/ Jointure entre la couche "à plat"
-- et le tableau créé en 4/
-- pour obtenir le résultat final
-- Départ : <tab_nb_a_plat>, <a_plat>
-- S'il y avait des erreurs de topologie, remplacer <a_plat> par <topo_ok>
-- Résultat : <nb_a_plat>
--------------------------------------

create table <nb_a_plat> as
select aplat.geom, aplat.gid, tableau.nb
from <tab_nb_a_plat> as tableau, <a_plat> as aplat
where tableau.aplat_id = aplat.gid;





