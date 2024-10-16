-- Rank country origins of bands ordered by the number of non-unique fans
SELECT origin, SUM(fans) AS fans FROM metal_bands
GROUP BY origin
ORDER BY fans DESC
