#!/usr/bin/env python
# coding: utf-8

# # ETL to DWH - hma

# In[1]:


import pandas as pd
import ast
import numpy
import sqlite3 as sql
import os


# In[2]:


#vars
input_folder = os.path.join('input')
SQLITE_FILE_PATH = os.path.join("output", "dwh.sqlite3")


# In[3]:


movies_df = pd.read_csv(os.path.join(input_folder,'movies_metadata.csv'))


# In[4]:


# buggy rows
buggy_rows = movies_df.loc[~movies_df["id"].str.isdigit()]


# In[5]:


movies_df.drop(buggy_rows.index, inplace=True)


# In[6]:


movies_genres = []
genre_names = [] 


# In[7]:


for index, row in movies_df.iterrows():
    genres = ast.literal_eval(row["genres"])
    for genre in genres:        
        genre_names.append(genre)           
        movie_genre = dict(
            movie_id=row['id'],
            genre_id=genre['id'],
        )   
        movies_genres.append(movie_genre)


# In[8]:


movies_genres_df = pd.DataFrame(movies_genres)


# In[9]:


genre_names_df = pd.DataFrame(genre_names).drop_duplicates()


# In[10]:


movies_final_df = movies_df[['id','adult','budget','homepage','imdb_id','original_language','original_title','overview', 'popularity','poster_path','revenue','title']]


# In[11]:


movies_final_df['budget'] = movies_final_df['budget'].astype(int)
movies_final_df['id'] = movies_final_df['id'].astype(int)
movies_final_df['popularity'] = movies_final_df['popularity'].astype(float)


# In[12]:


con = sql.connect(SQLITE_FILE_PATH)


# In[13]:


genre_names_df.to_sql('genres', con=con, if_exists='replace', index=False)


# In[14]:


movies_genres_df.to_sql('movie_genre', con=con, if_exists='replace', index=False)


# In[15]:


movies_final_df.to_sql('movies', con=con, if_exists='replace', index=False)


# In[16]:


con.close()


# In[ ]:




