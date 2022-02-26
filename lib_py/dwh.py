"""
DWH Modul zur Erstellung der Datenbank
"""
import os
import json
import ast
import pandas as pd
import sqlite3

CSV_FILE_PATH = os.path.join("input", "movies_metadata.csv")
SQLITE_FILE_PATH = os.path.join("output", "dwh.sqlite3")


def test_id_is_int(id):
    """Hilfsmethode um Zeilen mit Fehlern zu identiifzieren."""
    try:
        int(id)
        return True
    except:
        return False

def import_movies(csv_file_path):
    """Import movies from CSV and remove broken rows"""
    movies_df = pd.read_csv(csv_file_path)
    movies_df = movies_df.loc[movies_df["id"].apply(test_id_is_int)]
    return movies_df

def generate_genre_dfs(movies_df):
    """Generate genres_df and genres_movies_df from movies_df"""
    genres = []
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
    genres_df = pd.DataFrame(genres).drop_duplicates()
    genres_movies_df = pd.DataFrame(genres_movies)
    return genres_df, genres_movies_df

def main():
    """
    Import CSV, transform data and export to DWH (SQLite3)
    """
    movies_df = import_movies(CSV_FILE_PATH)
    genres_df, genres_movies_df = generate_genre_dfs(movies_df)

    # Select cols
    movie_cols = ["adult", "budget", "homepage", "id", "imdb_id", "original_language", "original_title", "overview", "popularity", "release_date", "revenue", "runtime", "status", "tagline", "video", "vote_average", "vote_count"]
    movies_export_df = movies_df[movie_cols]

    # Fix data types
    movies_export_df["budget"] = movies_export_df["budget"].astype(int)
    movies_export_df["id"] = movies_export_df["id"].astype(int)
    movies_export_df["popularity"] = movies_export_df["popularity"].astype(float)

    # Export to SQL
    con = sqlite3.connect(SQLITE_FILE_PATH)
    genres_df.to_sql("genres", con=con, if_exists="replace", index=False)
    genres_movies_df.to_sql("genres_movies", con=con, if_exists="replace", index=False)
    movies_export_df.to_sql("movies", con=con, if_exists="replace", index=False)
    con.close()


if __name__ == "__main__":
    print("DWH Start")
    main()
    print("DWH Ende")