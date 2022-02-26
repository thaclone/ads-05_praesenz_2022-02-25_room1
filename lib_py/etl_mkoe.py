#!/usr/bin/env python
# coding: utf-8


def main():
    print("dwh start")

    # # ETL to DWH - mkoe


    import os
    import ast
    import json
    import pandas as pd
    import sqlite3


    # ## Load
    # ### Einlesen der CSV


    CSV_FILE_PATH = os.path.join("input", "movies_metadata.csv")
    SQLITE_FILE_PATH = os.path.join("output", "dwh.sqlite3")



    movies_df = pd.read_csv(CSV_FILE_PATH)


    movies_df.head()


    # ## Transform

    # ### Drei falsche Datensätze löschne


    #Löschen aller nicht integer-Spalten
    movies_df = movies_df.drop(movies_df.loc[~movies_df["id"].str.isdigit()].index)


    #Auslesen, ob ein Wert in der Spalte ids nicht ein integer ist
    movies_df.loc[~movies_df["id"].str.isdigit()].index


    # ### Datentypen anschauen

    # #### Spalten in Movies löschen

    movies_final_df = movies_df.drop(columns=["belongs_to_collection","spoken_languages","genres", "production_countries", "production_companies"])

    movies_final_df.head()


    # #### Budget zu zahlen


    movies_final_df['budget'] = movies_final_df['budget'].astype(int)
    movies_final_df['id'] = movies_final_df['id'].astype(int)
    movies_final_df['popularity'] = movies_final_df['popularity'].astype(float)


    movies_final_df.info()


    # 
    # ### Sichere Codeprüfung mit Eval-Funktionen


    x= movies_df["genres"].apply(ast.literal_eval)


    x



    x[0][0]["id"]



    movies_df.shape


    s2 = "[{'id': print('hi'), 'name': 'Animation'}, {'id': 35, 'name': 'Comedy'}, {'id': 10751, 'name': 'Family'}]"



    eval(s2)



    #ast.literal_eval(s2)


    # ## Genres auflösen in extra Tabelle



    # ### Versuch in der Gruppe

    # Extraktion der Genres aus dem movies_df. Problem
    # Hierbei in der Spalte genres sind mit einem Dictionary mehrere ids und Genres verknüpft.

    # DF bilden mit Genres und Ids der Filme
    movie_df = movies_df[["genres", "id"]]


    movie_df


    movies_genres = []
    genre_names = []

    for index, row in movie_df.iterrows():
        #print (row["id"])
        genres = ast.literal_eval(row["genres"])
        for genre in genres:
            #print ("--> ",genre['id'])
            movie_genre = dict(
                movie_id=row["id"],
                genre_id=genre['id'],
            )
            movies_genres.append(movie_genre)
            genre_name = dict(
                genre_id=genre['id'],
                genre_name=genre['name']
            )
            genre_names.append(genre_name)

    genre_names_df = pd.DataFrame(genre_names).drop_duplicates()


    genre_names_df



    movies_genre_df = pd.DataFrame(movies_genres)



    movies_genre_df


    # ### Marcels Code
    # 
    # Extraktion der Genres aus dem movies_df. Problem Hierbei in der Spalte genres sind mit einem Dictionary mehrere ids und Genres verknüpft.

    genres =[]
    genres_movies = []

    for i, m in movies_df.iterrows():
        mg = m["genres"]
        mg = ast.literal_eval(mg)
        for g in mg:
            genres.append(g)
            genres_movies.append(dict(
                movie_id=m["id"],
                genre_id=g["id"],
            ))

    pd.DataFrame(genres).drop_duplicates()


    pd.DataFrame(genres_movies)





    # ## Überführen in SQL


    con = sqlite3.connect(SQLITE_FILE_PATH)


    genre_names_df.to_sql("genres", con=con, if_exists="replace", index=False)



    query = """
    SELECT * FROM genres;
    """
    pd.read_sql_query(query, con=con)




    movies_genre_df.to_sql("movies_genre", con=con, if_exists="replace", index=False)



    query = """
    SELECT * FROM movies_genre;
    """
    pd.read_sql_query(query, con=con)



    movies_final_df.info()




    movies_final_df.to_sql("movies", con=con, if_exists="replace", index=False)


    query = """
    SELECT * FROM movies;
    """
    pd.read_sql_query(query, con=con)


    print("dwh ende")


