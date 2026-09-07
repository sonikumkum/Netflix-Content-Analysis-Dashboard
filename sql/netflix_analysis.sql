-- Netflix Content Analysis

-- 1. Total number of titles
SELECT COUNT(*) AS total_titles
FROM netflix_titles;

-- 2. Movies vs TV Shows
SELECT type, COUNT(*) AS total
FROM netflix_titles
GROUP BY type;

-- 3. Content by release year
SELECT release_year, COUNT(*) AS total_titles
FROM netflix_titles
GROUP BY release_year
ORDER BY release_year;

-- 4. Top countries
SELECT country, COUNT(*) AS total_titles
FROM netflix_titles
WHERE country IS NOT NULL
GROUP BY country
ORDER BY total_titles DESC
LIMIT 10;

-- 5. Ratings distribution
SELECT rating, COUNT(*) AS total_titles
FROM netflix_titles
WHERE rating IS NOT NULL
GROUP BY rating
ORDER BY total_titles DESC;

-- 6. Content added by year
SELECT added_year, COUNT(*) AS total_titles
FROM netflix_titles
WHERE added_year IS NOT NULL
GROUP BY added_year
ORDER BY added_year;

-- 7. Movies vs TV Shows by release year
SELECT release_year, type, COUNT(*) AS total_titles
FROM netflix_titles
GROUP BY release_year, type
ORDER BY release_year;