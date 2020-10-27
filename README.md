# Web Scraping Challenge - Mission to Mars

![Image of MARS](https://github.com/giovannahayes/web-scraping-challenge/blob/main/Mission_to_Mars/Images/mission_to_mars.png)

## In this assignment, we built a web application that scrapes various websites for data related to the Mission to Mars and displays the information in a single HTML page.

#### We completed our initial scraping of multiple NASA websites using Jupyter Notebook, BeautifulSoup, Pandas, and Requests/Splinter.

#### Next we used MongoDB with Flask templating to create a new HTML page that displays all of the information that was scraped from the URLs above.

####  We converted the Jupyter notebook into a Python script called scrape_mars2.py with a function called scrape that executes all the scraping code from above and returns one Python dictionary containing all of the scraped data.

#### Next, we created a route called /scrape that imports the scrape_mars2.py script and call the  scrape function.

#### We store the return value in Mongo as a Python dictionary and create a root route / that queries the Mongo database and passes the mars data into an HTML template to display the data.

#### We then created a template HTML file called index2.html that takes the mars data dictionary and displays all of the data in the appropriate HTML elements. 

#### Below are some screen shots of the final application

![Image of SCRN1](https://github.com/giovannahayes/web-scraping-challenge/blob/main/Mission_to_Mars/Images/Screenshot1.PNG)

![Image of SCRN2](hhttps://github.com/giovannahayes/web-scraping-challenge/blob/main/Mission_to_Mars/Images/Screenshot2.PNG)

