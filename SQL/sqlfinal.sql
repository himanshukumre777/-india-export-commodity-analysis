-- creating table for top 15 commodities data (2024 vs 2025)

CREATE TABLE exports_v2 (
    id SERIAL PRIMARY KEY,
    commodity_group VARCHAR(60),
    month VARCHAR(3),
    month_num INT,
    unit VARCHAR(10),
    value_2024 NUMERIC,
    share_2024 NUMERIC,
    value_2025 NUMERIC,
    share_2025 NUMERIC,
    growth_pct NUMERIC,
    cum_value_2024 NUMERIC,
    cum_share_2024 NUMERIC,
    cum_value_2025 NUMERIC,
    cum_share_2025 NUMERIC,
    cum_growth_pct NUMERIC
);

-- check table created
SELECT * FROM exports_v2;

--Q1.

SELECT 
    SUM(value_2024) AS total_2024,
    SUM(value_2025) AS total_2025,
    ROUND(((SUM(value_2025) - SUM(value_2024)) / SUM(value_2024) * 100)::numeric, 2) AS overall_growth_pct
FROM exports_v2;

--Q2.

SELECT 
    commodity_group,
    SUM(value_2024) AS total_2024,
    SUM(value_2025) AS total_2025,
    ROUND(((SUM(value_2025) - SUM(value_2024)) / SUM(value_2024) * 100)::numeric, 2) AS growth_pct
FROM exports_v2
GROUP BY commodity_group
ORDER BY growth_pct DESC;

--Q3.

SELECT 
    commodity_group,
    SUM(value_2024) AS total_2024
FROM exports_v2
GROUP BY commodity_group
ORDER BY total_2024 DESC
LIMIT 1;

--Q4.

SELECT 
    commodity_group,
    SUM(value_2025) AS total_2025
FROM exports_v2
GROUP BY commodity_group
ORDER BY total_2025 DESC
LIMIT 1;

--Q6.

SELECT 
    commodity_group,
    ROUND(AVG(share_2024)::numeric, 2) AS avg_share_2024,
    ROUND(AVG(share_2025)::numeric, 2) AS avg_share_2025,
    ROUND((AVG(share_2025) - AVG(share_2024))::numeric, 2) AS share_change
FROM exports_v2
GROUP BY commodity_group
ORDER BY share_change DESC;