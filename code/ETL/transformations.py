

# Importacion de pandas y de las funciones auxiliares
# Importamos las librerias
import pandas as pd
from auxiliar_functions_transformations import *


#--------------------------------------------------------------------------------------------------


'''
========
EXTRACT
========

    - Unimos los archivos 'movies_dataset.csv' y 'credits.csv'
'''
df = merge_movies_and_credits(pd.read_csv(r"../../data/data_bruta/movies_dataset.csv"), pd.read_csv(r"../../data/data_bruta/credits.csv"))


#--------------------------------------------------------------------------------------------------


'''
===============
TRANSFORMATION
===============

    TRANSFORMACION 1:   
    - Desanidar los campos en formato Json.
'''

# Para la columna 'genres'
df = convert_column_json(df, 'genres')

# Para la columna 'production_companies'
df = convert_column_json(df, 'production_companies')

# Para la columna 'production_countries'
df = convert_column_json(df, 'production_countries')

# Para la columna 'spoken languages'
df = convert_column_json(df, 'spoken_languages')

# Para la columna 'cast'
df = convert_column_json(df, 'cast')

# Para la columna 'crew'
df = convert_column_crew(df)


#--------------------------------------------------------------------------------------------------


'''
    TRANSFORMACION 2:
    - Los valores nulos de los campos revenue, budget deben ser rellenados por el número 0.
'''
df = fillna_revenue_and_budget(df)


#--------------------------------------------------------------------------------------------------


'''
    TRANSFORMACION 3:
    - Los valores nulos del campo release date deben eliminarse.
'''
df = dropna_release_date(df)


#--------------------------------------------------------------------------------------------------


'''
    TRANSFORMACION 4:
    - De haber fechas, deberán tener el formato AAAA-mm-dd, además deberán crear la columna release_year 
    donde extraerán el año de la fecha de estreno.
'''
df = add_release_year_column(df)


#--------------------------------------------------------------------------------------------------


'''
    TRANSFORMACION 5:
    - Crear la columna con el retorno de inversión, llamada return con los campos revenue y budget,
    dividiendo estas dos últimas revenue / budget, cuando no hay datos disponibles para calcularlo, 
    deberá tomar el valor 0.
'''
df = add_return_column(df)


#--------------------------------------------------------------------------------------------------


'''
    TRANSFORMACION 6:
    - Eliminar las columnas que no serán utilizadas, video, imdb_id, original_title, poster_path y homepage.
'''
df = drop_useless_columns(df)


#--------------------------------------------------------------------------------------------------

'''
=====
LOAD
=====
'''
# Guardamos los cambios en el mismo csv
df.to_csv(r"../../data/data_procesada/data_procesada.csv", encoding='utf-8-sig', index=False, sep=',') 