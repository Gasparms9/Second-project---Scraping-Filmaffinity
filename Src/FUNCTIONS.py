import requests
from bs4 import BeautifulSoup
import pandas as pd
import requests
import re

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

## importing databases

GSAF = r"C:\Users\lenovo\Desktop\Ironhack\Second project - IMDB-FA\Src\imdb_top_1000.csv"

df = pd.read_csv(GSAF, encoding = "ISO-8859-1")

GSAF = r"C:\Users\lenovo\Desktop\Ironhack\Second project - IMDB-FA\Src\data.tsv"

df_originalnames = pd.read_csv(GSAF, sep='\t')



## title must be in spanish, so we get matches in the filmaffinity database.
## this function works 98% of the time. Sometimes it returns me an incorrect movie becouse of the title_main in title_scraping.
## must be a better way to do it. i think it would work if i apply strip to title_scraping. Sometimes filmaff puts a blank
# space to the end of the title, givine me something like: "Origen ".

    
def search_filmaffinity_movie_href(title):
    
    try:
        
        def search_filmaffinity_scraping(soup): ## this function search in fa search bar, and iterates the results to get matches
            products = soup.find_all("div", attrs = {"class":"mc-title"})
            for i in products:
                href = i.find("a").get("href")
                title_scraping = i.find("a").get("title").lower().strip()
                if title_main == title_scraping: ## if title == movie match, give me the movie page link.
                    return title_scraping, href
                elif title_main in title_scraping:## elif exists for exceptions, maybe.
                    return title_scraping, href

            return "Couldnt find", "Couldn't find"

        title_main = title.lower()
        title_cleaned_search = title_main.replace(" ","+")
        search_url_filmaffinity = "https://www.filmaffinity.com/es/search.php?stext="+title_cleaned_search ## generates link search
        res = requests.get(search_url_filmaffinity)
        html = res.content
        soup = BeautifulSoup(html, "html.parser")
        content = soup.find_all("div", attrs = {"class":"meta content"}) 
        title_scraping, href = search_filmaffinity_scraping(soup) ## aplies function
        if href == "Couldn't find": ## if we don't find match
            content = soup.find_all("dd", attrs = {"itemprop":"description"}) 
            if content: 
            #this if function is important. Sometimes filmaff don't find a match but returns the main page of the movie if the search
            # is exactly like the name. so when this happens, i check if content(this is the way i check im in the page of the movie
            # i want to get info) exsits, then returns the main url, which is the movie info, and the name. GGWP.
                return search_url_filmaffinity  
        else:
            return href 
    
    except:
        return np.nan

## It gets a string of the link of the main page in filmaffinity and returns the stars as a float.

def get_note_filmaffinity(href):
    try:
        res = requests.get(href)
        html = res.content
        soup = BeautifulSoup(html, "html.parser")
        content = soup.find_all("div", attrs = {"itemprop":"ratingValue"})
        pov = content[0].get_text()
        pov = pov.replace(",",".")
        note = float(pov.strip())
        if not note:
            return "No note"
        return note
    except:
        return np.nan

## It gets a string of the main page in filmaffinity and returns the number of voters, as a integer.

def get_votes(href):
    try:
        res = requests.get(href)
        html = res.content
        soup = BeautifulSoup(html, "html.parser")
        content = soup.find_all("div", attrs = {"id":"movie-count-rat"})
        pov = content[0].get_text()
        votes = int(pov.strip().strip('\nvotos').replace(".",""))
        return votes
    
    except:
        return np.nan
    

## Gets the original name of the main page of the ff database as a string

def get_name(href):
    try:
        res = requests.get(href)
        html = res.content
        soup = BeautifulSoup(html, "html.parser")
        content = soup.find_all("div", attrs = {"id":"left-column"})
        content = content[0].find("dd")
        original_name = content.get_text().strip()
        return original_name
    
    except:
        return np.nan
    
    
##With this function, i get the original imdb id for the movie and i search i get the soup. 
#Funny is that my browser gets me to the SPANISH version of the movie, getting the spanish name with the titled. 
#It returns a string.

def get_spanish_name(titled):
    try:
        href = "https://www.imdb.com/title/"+titled
        res = requests.get(href)
        html = res.content
        soup = BeautifulSoup(html, "html.parser")
        content = soup.find("title").get_text()
        content = content.strip("(")
        content = content.split("(")[0].strip()
        return content
    except:
        return np.nan


##CALLING THE FUNCTIONS.
## Rearrange the dataframes and dropping na.

df_number_imdb = df.merge(df_originalnames, left_on='Series_Title', right_on='title')[['Series_Title', 'titleId', 'IMDB_Rating', 'Director', "No_of_Votes"]]

df_number_imdb = df_number_imdb.drop_duplicates(subset=["Series_Title"], keep=False)

#first function
df_number_imdb["Spanish name"] = df_number_imdb["titleId"].apply(get_spanish_name) ## first function

df_number_imdb.columns = ['Series_Title_1', 'titleId', 'IMDB_Rating_1', 'Director_1', "No_of_Votes_1", "Spanish name"] ## renaming

# a huge merge
df_before_filmaff = df.merge(df_number_imdb, left_on='Series_Title', right_on='Series_Title_1')[['Series_Title', "Released_Year", "Runtime", "Genre", "IMDB_Rating", "Director", "Star1", "Star2", "Star3", "Star4","No_of_Votes","Gross", "Spanish name"]]

#second function
df_before_filmaff["Filmaffinity link"] = df_before_filmaff["Spanish name"].apply(search_filmaffinity_movie_href)

## some replacing
df_before_filmaff.loc[df_before_filmaff["No_of_Votes"] ==  1270197, "Filmaffinity link"] = "https://www.filmaffinity.com/es/film768790.html"
df_before_filmaff.loc[df_before_filmaff["Spanish name"] == "¿Teléfono rojo? Volamos hacia Moscú", "Filmaffinity link"] = "https://www.filmaffinity.com/es/film479847.html"
df_before_filmaff.loc[df_before_filmaff["Spanish name"] == "Children of Heaven", "Filmaffinity link"] = "https://www.filmaffinity.com/es/film291595.html"
df_before_filmaff.loc[df_before_filmaff["Spanish name"] == "Pink Floyd: The Wall", "Filmaffinity link"] = "https://www.filmaffinity.com/es/film352368.html"
df_before_filmaff.loc[df_before_filmaff["Spanish name"] == "El gabinete del Dr. Caligari", "Filmaffinity link"] = "https://www.filmaffinity.com/es/film446167.html"
df_before_filmaff.loc[df_before_filmaff["No_of_Votes"] ==  240266, "Filmaffinity link"] = "https://www.filmaffinity.com/es/film239359.html"
df_before_filmaff.loc[df_before_filmaff["Spanish name"] == "¿Quién teme a Virginia Woolf?", "Filmaffinity link"] = "https://www.filmaffinity.com/es/film969127.html"
df_before_filmaff.loc[df_before_filmaff["Spanish name"] == "¿A quién ama Gilbert Grape?", "Filmaffinity link"] = "https://www.filmaffinity.com/es/film984814.html"
df_before_filmaff.loc[df_before_filmaff["No_of_Votes"] ==  43690, "Filmaffinity link"] = "https://www.filmaffinity.com/es/film526741.html"
df_before_filmaff.loc[df_before_filmaff["Spanish name"] == "Regreso al futuro. Parte II", "Filmaffinity link"] = "https://www.filmaffinity.com/es/film775323.html"
df_before_filmaff.loc[df_before_filmaff["Spanish name"] == "Interstate 60: Episodios de carretera", "Filmaffinity link"] = "https://www.filmaffinity.com/es/film239328.html"
df_before_filmaff.loc[df_before_filmaff["No_of_Votes"] ==  82781, "Filmaffinity link"] = "https://www.filmaffinity.com/es/film228749.html"
df_before_filmaff.loc[df_before_filmaff["No_of_Votes"] ==  90442, "Filmaffinity link"] = "https://www.filmaffinity.com/es/film711519.html"

# third function
df_before_filmaff["Filmaffinity score"] = df_before_filmaff["Filmaffinity link"].apply(get_note_filmaffinity)

#Droping subset
df_before_filmaff = df_before_filmaff.dropna(subset=['Filmaffinity score'])

# fourth function
df_before_filmaff["Filmaffinity votes"] = df_before_filmaff["Filmaffinity link"].apply(get_votes)



#### EXPORTING

df_before_filmaff.to_csv("src/clean_data_filmaff_imdb.csv",index=False)