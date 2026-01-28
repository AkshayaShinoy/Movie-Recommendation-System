import pandas as pd
import joblib

print("Loading data...")
# 1. Load Data
ratings_df = pd.read_csv('ml-100k/u.data', sep='\t', header=None, names=['userId', 'movieId', 'rating', 'timestamp'])
ratings_df = ratings_df.drop('timestamp', axis=1)

# Load the movie titles to link movie IDs to names
movies_df = pd.read_csv('ml-100k/u.item', sep='|', encoding='latin-1', header=None, 
                        names=['movieId', 'title', 'release_date', 'video_release_date',
                               'IMDb_URL', 'unknown', 'Action', 'Adventure', 'Animation',
                               'Childrens', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy',
                               'Film-Noir', 'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi',
                               'Thriller', 'War', 'Western'])

# 2. Create the User-Item Matrix (Pivot Table)
print("Creating user-item matrix...")
user_item_matrix = ratings_df.pivot_table(index='userId', columns='movieId', values='rating').fillna(0)

# 3. Calculate Item-to-Item Similarity (Correlation)
print("Calculating item-to-item similarity...")
item_similarity_matrix = user_item_matrix.corr(method='pearson')

# 4. Save the trained model and movie titles
print("Saving model and movie titles...")
joblib.dump(item_similarity_matrix, 'item_similarity_matrix.pkl')
joblib.dump(movies_df[['movieId', 'title']], 'movie_titles.pkl')

print("Model trained and saved as 'item_similarity_matrix.pkl'")
