import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import os

# Load the movie titles and genres data
movies_df = pd.read_csv('ml-100k/u.item', sep='|', encoding='latin-1', header=None,
                        names=['movieId', 'title', 'release_date', 'video_release_date',
                               'IMDb_URL', 'unknown', 'Action', 'Adventure', 'Animation',
                               'Childrens', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy',
                               'Film-Noir', 'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi',
                               'Thriller', 'War', 'Western'])

# Get the genre columns
genres = movies_df.columns[6:]

# Create a string of all genres, repeating each genre for every movie it belongs to
genre_string = ""
for index, row in movies_df.iterrows():
    for genre in genres:
        if row[genre] == 1:
            genre_string += genre + " "

# Create the word cloud
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(genre_string)

# Save the word cloud image to a file
wordcloud.to_file("genre_wordcloud.png")

print("Word cloud generated and saved as genre_wordcloud.png")
