

## Web Scrapping of Filmaffinity Database:
### By: Gaspar Masdeu
### Date: July 25th 2022

![Filmaffinity logo](data:image/png;base64,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)

#
## Hypothesis:
#

1. Filmaffinity users gives lower scores overall, and tends to dislike Romance more than IMDB users.
2. IMDB users likes shorter movies.
#

## ORGANIZATION:

### Scraping

The scrapping part is the hard part of this project. In the FUNCTIONS.py files you have the functions and i used to iterate to the webpaga and find the results i wanted.
My original database was a IMDB database which had the titles of the movies in ENGLISH. Filmaffinity is a spanish database, so i had to find a way to find the name of the movie in spanish. Webscrapping the IMDB page gave me the name of the movie in spanish.
Then, I created a function which, with only the name of the movie in spanish, gave us the link to the main page of the movie, the score of the movie and the total users who voted the movie.
The webscrapping part ended, and i got the moviepage link in filmaffinity and in IMDB. I got the IMDB rating, the filmaffinity rating, and both users votecount.


### Cleanup:
After a brief exploration of the size and quality of the data, I proceed to a first basic roughing out. In the following phases I went through the file by columns, evaluating the best way to extract the most data according to the content, the type of data and the usefulness it could provide us for future visualizations. This process is documented in: cleaning.ipynb commented file with the cleaning process.


### Analysis:
Once the clean file has been obtained, several graphs have been made, relying on different libraries, in order to visually support the conclusions. This process is documented in: VIZ_1.ipynb file that includes both the graphs and the conclusions obtained from the study.
