-- Author: Gadoskey
-- File: 2-fans.sql
-- A SQL script that ranks the country origins of bands by the number of (non-unique) fans
-- ordered by the count of fans in descending order.

SELECT origin, SUM(fans) AS nb_fans
FROM metal_bands
GROUP BY origin
ORDER BY nb_fans DESC;
