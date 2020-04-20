import pandas as pd


def read_book_details(title, uid):
    df_unique_book = pd.read_csv("unique_books.csv")
    lst_book = df_unique_book[df_unique_book['book_title'] == title]
    # lst_book.to_csv("C:/Users/Nikhita/Desktop/Dataset/Final/one_book.csv")

    df_unique_user = pd.read_csv("user_details.csv")
    lst_user = df_unique_user[df_unique_user['user_id'] == uid]
    # lst_user.to_csv("C:/Users/Nikhita/Desktop/Dataset/Final/one_user.csv")
    return lst_book, lst_user
