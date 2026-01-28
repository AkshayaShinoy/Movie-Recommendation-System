from django.shortcuts import render
import joblib
import os
import pandas as pd
from imdb import IMDb # <--- Add this import

# Construct the path to the pickle files from the project's base directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Paths to the pickle files
movie_titles_path = os.path.join(BASE_DIR, 'movie_titles.pkl')
item_similarity_matrix_path = os.path.join(BASE_DIR, 'item_similarity_matrix.pkl')

# Create an IMDb instance
ia = IMDb()

def get_imdb_poster_url(title):
    """Fetches the poster URL from the IMDb database for a given movie title."""
    try:
        # Search for the movie by its title
        movies = ia.search_movie(title)
        if movies:
            # Get the first movie from the search results
            movie = movies[0]
            # Fetch the poster URL
            ia.update(movie)
            if 'full-size cover url' in movie:
                return movie['full-size cover url']
            elif 'cover url' in movie:
                return movie['cover url']
    except Exception as e:
        print(f"Error fetching poster for {title}: {e}")
    
    return 'https://via.placeholder.com/300x450.png?text=Poster+Not+Found'


def index(request):
    # Load the movie titles from the saved pickle file
    movie_titles_df = joblib.load(movie_titles_path)
    movie_titles = movie_titles_df['title'].tolist()

    context = {
        'movie_titles': movie_titles,
    }

    return render(request, "index.html", context)


def recommendations(request):
    # Get the selected movie title from the form
    selected_movie = request.POST.get('movie_title')

    # Load the similarity matrix and movie titles
    item_similarity_matrix = joblib.load(item_similarity_matrix_path)
    movies_df = joblib.load(movie_titles_path)

    # Get the movie ID for the selected movie
    movie_id = movies_df[movies_df['title'] == selected_movie]['movieId'].iloc[0]

    # Get the top 10 most similar movies from the matrix
    similar_movies_ids = item_similarity_matrix[movie_id].sort_values(ascending=False).index[1:11]
    
    # Get the movie titles for the recommended IDs
    recommended_movies_df = movies_df[movies_df['movieId'].isin(similar_movies_ids)]
    
    # Get the posters for the recommended movies using the IMDbPY library
    recommended_movies_with_posters = []
    for index, row in recommended_movies_df.iterrows():
        title = row['title']
        poster_url = get_imdb_poster_url(title)
        recommended_movies_with_posters.append({'title': title, 'poster_url': poster_url})

    # Get the poster for the selected movie using the IMDbPY library
    selected_movie_poster = get_imdb_poster_url(selected_movie)

    context = {
        'selected_movie': selected_movie,
        'selected_movie_poster': selected_movie_poster,
        'recommended_movies': recommended_movies_with_posters,
    }
    
    return render(request, 'results.html', context)
