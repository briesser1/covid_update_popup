SELECT
    state,
    county_name,
    confirmed,
    confirmed_per_100000,
    deaths
FROM `1_county_level_confirmed_cases`
WHERE state = 'South Carolina'
     AND
county_name IN (
    'Richland',
    'Greenville',
    'Lexington',
	'Horry',
	'Charleston'
) OR
state = 'North Carolina' 
    AND
county_name IN (
    'Forsyth', 
    'Durham',
    'Wake',
    'Brunswick'
) OR
state = 'California' 
    AND
county_name IN (
    'Los Angeles'
) OR
state = 'Ohio' 
    AND
county_name IN (
    'Licking',
    'Clark', 
    'Franklin'
) OR
state = 'Virginia' 
    AND
county_name IN (
    'Chesterfield'
) ORDER BY confirmed DESC;