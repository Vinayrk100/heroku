import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import re
import sklearn.metrics.pairwise as pw
from scipy import sparse
from sklearn.metrics.pairwise import pairwise_distances
from scipy.sparse.linalg import svds


def recommend_books_userbased(userID):
    books_details_df = pd.read_csv('final_book_details.csv')
    df_ratings = pd.read_csv('ratings.csv')
    df_books_ratings = df_ratings.pivot(
        index='user_id',
        columns='book_id',
        values='rating'
    ).fillna(0)

    R = df_books_ratings.values
    user_ratings_mean = np.mean(R, axis=1)
    R_demeaned = R - user_ratings_mean.reshape(-1, 1)

    U, sigma, Vt = svds(R_demeaned, k=50)

    sigma = np.diag(sigma)

    all_user_predicted_ratings = np.dot(np.dot(U, sigma), Vt) + user_ratings_mean.reshape(-1, 1)

    preds_df = pd.DataFrame(all_user_predicted_ratings, columns=df_books_ratings.columns)

    # Get and sort the user's predictions
    user_row_number = userID  # UserID starts at 1, not 0
    sorted_user_predictions = preds_df.iloc[user_row_number].sort_values(ascending=False)  # UserID starts at 1

    # Get the user's data and merge in the book information.
    user_data = df_ratings[df_ratings.user_id == userID]

    user_full = (user_data.merge(books_details_df, how='left', on='book_id').sort_values(['rating_x'], ascending=False))

    #  Recommendation starts based on Author , Genre , Similar user , book pages

    genre = user_full.genres.unique()
    book_pages = user_full.book_pages.unique()
    authors = user_full.book_authors.unique()

    # Recommend the highest predicted rating books that the user hasn't seen yet.
    recommendations_genre = (books_details_df[~books_details_df['book_id'].isin(user_full['book_id']) &
                                              books_details_df['genres'].isin(genre)]).merge(
        pd.DataFrame(sorted_user_predictions).reset_index(), how='left', left_on='book_id',
        right_on='book_id')

    recommendations_bookpages = (books_details_df[~books_details_df['book_id'].isin(user_full['book_id']) &
                                                  books_details_df['book_pages'].isin(book_pages)]).merge(
        pd.DataFrame(sorted_user_predictions).reset_index(), how='left', left_on='book_id',
        right_on='book_id')

    recommendations_author = (books_details_df[~books_details_df['book_id'].isin(user_full['book_id']) &
                                               books_details_df['book_authors'].isin(authors)]).merge(
        pd.DataFrame(sorted_user_predictions).reset_index(), how='left', left_on='book_id',
        right_on='book_id')

    recommendations_genre = recommendations_genre.drop_duplicates()
    recommendations_genre = recommendations_genre[1:6].sort_values(['rating'], ascending=False)

    recommendations_author = recommendations_author.drop_duplicates()
    recommendations_author = recommendations_author[1:6].sort_values(['rating'], ascending=False)

    recommendations_bookpages = recommendations_bookpages.drop_duplicates()
    recommendations_bookpages = recommendations_bookpages[1:6].sort_values(['rating'], ascending=False)

    user_full = user_full[1:6]

    return user_full, recommendations_genre, recommendations_author, recommendations_bookpages

