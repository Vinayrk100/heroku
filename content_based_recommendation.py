# -*- coding: utf-8 -*-
"""Content_based_rec.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Dkng4FdD-HQFvzfo78heV6lf5owKVfVC

# Content Based Filtering - authers, genre, laguage-code
First taken three things separately and then combined.
Only the new books data is used for content based
"""

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
def content(title):
    books = pd.read_csv('unique_books.csv')
    books.head()


    """# Combining Authers, Genres and language for better results"""

    books['corpus'] = (pd.Series(books[['book_authors', 'genres','language_code']].fillna('').values.tolist()).str.join(' '))

    tf_corpus = TfidfVectorizer(analyzer='word',ngram_range=(1, 2),min_df=0, stop_words='english')
    tfidf_matrix_corpus = tf_corpus.fit_transform(books['corpus'])
    cosine_sim_corpus = linear_kernel(tfidf_matrix_corpus, tfidf_matrix_corpus)

    # Build a 1-dimensional array with book titles
    titles = books['book_title']
    indices1 = pd.Series(books.index, index=books['book_title'])

# Function that get book recommendations based on the cosine similarity score of books tags

    idx = indices1[title]
    sim_scores = list(enumerate(cosine_sim_corpus[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:21]
    book_indices = [i[0] for i in sim_scores]
    c = titles.iloc[book_indices]

    return books[books['book_title'].isin(c)].head()

# corpus = content("the secret life of bees").head()
#
# print(corpus.columns)
# books[books['book_title'].isin(corpus)].head()

