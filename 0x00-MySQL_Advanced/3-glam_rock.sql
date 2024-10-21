-- Author: Gadoskey
-- File: 3-glam_rock.sql
-- A SQL script that lists all bands with Glam rock as their main style, ranked by their longevity

SELECT band_name, 
       IFNULL(split, 2020) - IFNULL(formed, 0)
FROM bands
WHERE style = 'Glam rock'
ORDER BY lifespan DESC;
