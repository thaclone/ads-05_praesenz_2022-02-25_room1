#!/usr/bin/env python
# coding: utf-8

print("dwh start")

# # ETL to DWH - mkoe

# In[1]:


import os
import ast
import json
import pandas as pd
import sqlite3


# ## Load
# ### Einlesen der CSV

# In[2]:


CSV_FILE_PATH = os.path.join("input", "movies_metadata.csv")
SQLITE_FILE_PATH = os.path.join("output", "dwh.sqlite3")


# In[3]:


movies_df = pd.read_csv(CSV_FILE_PATH)


# In[4]:


movies_df.head()


# ## Transform

# ### Drei falsche Datensätze löschne

# In[5]:


#Löschen aller nicht integer-Spalten
movies_df = movies_df.drop(movies_df.loc[~movies_df["id"].str.isdigit()].index)


# In[6]:


#Auslesen, ob ein Wert in der Spalte ids nicht ein integer ist
movies_df.loc[~movies_df["id"].str.isdigit()].index


# ### Datentypen anschauen

# #### Spalten in Movies löschen

# In[7]:


movies_final_df = movies_df.drop(columns=["belongs_to_collection","spoken_languages","genres", "production_countries", "production_companies"])


# In[8]:


movies_final_df.head()


# #### Budget zu zahlen

# In[9]:


movies_final_df['budget'] = movies_final_df['budget'].astype(int)
movies_final_df['id'] = movies_final_df['id'].astype(int)
movies_final_df['popularity'] = movies_final_df['popularity'].astype(float)


# In[10]:


movies_final_df.info()


# 
# ### Sichere Codeprüfung mit Eval-Funktionen

# In[11]:


x= movies_df["genres"].apply(ast.literal_eval)


# In[12]:


x


# In[13]:


x[0][0]["id"]


# In[ ]:





# In[14]:


movies_df.shape


# In[15]:


s2 = "[{'id': print('hi'), 'name': 'Animation'}, {'id': 35, 'name': 'Comedy'}, {'id': 10751, 'name': 'Family'}]"


# In[16]:


eval(s2)


# In[17]:


#ast.literal_eval(s2)


# In[ ]:





# ## Genres auflösen in extra Tabelle

# In[ ]:





# ### Versuch in der Gruppe

# Extraktion der Genres aus dem movies_df. Problem
# Hierbei in der Spalte genres sind mit einem Dictionary mehrere ids und Genres verknüpft.

# In[18]:


# DF bilden mit Genres und Ids der Filme
movie_df = movies_df[["genres", "id"]]


# In[19]:


movie_df


# In[20]:


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


# In[21]:


genre_names_df = pd.DataFrame(genre_names).drop_duplicates()


# In[22]:


genre_names_df


# In[23]:


movies_genre_df = pd.DataFrame(movies_genres)


# In[24]:


movies_genre_df


# ### Marcels Code
# 
# Extraktion der Genres aus dem movies_df. Problem Hierbei in der Spalte genres sind mit einem Dictionary mehrere ids und Genres verknüpft.

# In[25]:


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


# In[26]:


pd.DataFrame(genres).drop_duplicates()


# In[27]:


pd.DataFrame(genres_movies)


# In[ ]:





# In[ ]:





# ## Überführen in SQL

# In[28]:


con = sqlite3.connect(SQLITE_FILE_PATH)


# In[29]:


genre_names_df.to_sql("genres", con=con, if_exists="replace", index=False)


# In[30]:


query = """
SELECT * FROM genres;
"""
pd.read_sql_query(query, con=con)


# In[ ]:





# In[31]:


movies_genre_df.to_sql("movies_genre", con=con, if_exists="replace", index=False)


# In[32]:


query = """
SELECT * FROM movies_genre;
"""
pd.read_sql_query(query, con=con)


# In[33]:


movies_final_df.info()


# In[34]:


movies_final_df.to_sql("movies", con=con, if_exists="replace", index=False)


# In[35]:


query = """
SELECT * FROM movies;
"""
pd.read_sql_query(query, con=con)


# In[ ]:

print("dwh ende")


