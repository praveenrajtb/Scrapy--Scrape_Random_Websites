# Scrapy--Scrape_Random_Websites
http://www.eplanning.ie
We are scraping agents information in the planning applications received in all the counties in the last 48 days.
Steps:
Get all urls for the counties.
For each county Page find the 'Received Applications'  url.
In Received Applications Page Set time limit to 48 days (our target) from the default 7 days and search for applications
From the page showing 'Applications Received in the past 42 Days'  go to each applications and find the agents info from 
the page if thats available if not pass.
Do the same for remaining pages showing the 'Applications' eg: 7 of them, Do the same procedure
