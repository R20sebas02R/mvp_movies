

# Importamos las librerias a usar
import pandas as pd
import json
import re
import os

#-----------------------------------------------------------------------------------------------


def merge_movies_and_credits(movies_df: pd.DataFrame, credits_df: pd.DataFrame):
    '''
    La función devuelve el DataFrame resultado de unir movies y credits. Para ello elimina los id's que no están en
    el formato adecuado (número entero), elimina los id's duplicados y finalmente los convierte a enteros de 64 bits.
    '''
    
    # Convierte los id's de cada DataFrame a entero y si no se puede lo etiqueta con NaN
    movies_df['id'] = pd.to_numeric(movies_df['id'], errors='coerce')
    credits_df['id'] = pd.to_numeric(credits_df['id'], errors='coerce')
    
    # Dropea los registros que son NaN
    movies_df = movies_df.dropna(subset=['id'])
    credits_df = credits_df.dropna(subset=['id'])
    
    # Dropea los registros duplicados
    movies_df.drop_duplicates(subset='id', inplace=True)
    credits_df.drop_duplicates(subset='id', inplace=True) 

    # Juntar los DataFrames utilizando el campo "id"
    merged_data = pd.merge(movies_df, credits_df, on='id')
    
    # Eliminar los registros que no tienen título 
    merged_data = merged_data.dropna(subset=['title'])
    
    # Restablecer el índice
    merged_data = merged_data.reset_index(drop=True)
    
    return merged_data

    
#-----------------------------------------------------------------------------------------------


def convert_column_json(df: pd.DataFrame, column: str, name='name', num_segmentos=507):
    '''
    Esta funcion transforma la columna especificada en un formato mas simple
    Requiere el dataframe y el nombre de la columna 
    Retorna el dataframe con la columna modificada
    '''
    # Calcula el tamaño de cada segmento
    tam_segmento = len(df) // num_segmentos

    for i in range(num_segmentos):
        # Calcula los índices inicial y final para el segmento actual
        start_idx = i * tam_segmento
        end_idx = (i + 1) * tam_segmento

        # Si es el último segmento, ajusta el índice final al tamaño del DataFrame
        if i == num_segmentos - 1:
            end_idx = len(df)

        # Obtiene el segmento actual del DataFrame
        segmento_df = df.iloc[start_idx:end_idx]

        # Aplica la transformación a la columna especificada usando el método apply
        segmento_df[column] = segmento_df[column].apply(lambda x: extract_values_of_dictionaries(x, name))

        # Hace que los cambios se vean reflejados en el dataframe original
        df.iloc[start_idx:end_idx] = segmento_df

    return df

def extract_values_of_dictionaries(value, name):
    # Transforma la fila en la columna especificada en una cadena de texto
    fila = str(value)
    # Utiliza expresión regular para encontrar los substrings entre {} (los diccionarios en la fila)
    diccionarios_en_la_fila = re.findall(r'{.*?}', fila)

    # Una lista de los valores de los diccioarios asociados al film actual en el loop
    valores_row = []

    # Iterar sobre los diccionarios_en_la_fila
    for diccionario in diccionarios_en_la_fila:
        # Buscar la expresión regular 'name' dentro del diccionario
        match = re.search(rf"{name}': '([^']*)", diccionario)
        if match:
            # Le asigna el valor encontrado a la variable valor
            valor = match.group(1)
            valores_row.append(valor)

    # Devuelve la lista de géneros como string
    return json.dumps(valores_row)


#-----------------------------------------------------------------------------------------------


def convert_column_crew(df: pd.DataFrame, num_segmentos=507):
    '''
    Esta función transforma la columna 'crew' en un formato más simple
    Requiere el dataframe
    Retorna el dataframe con la columna modificada
    '''
    # Calcula el tamaño de cada segmento
    tam_segmento = len(df) // num_segmentos

    for i in range(num_segmentos):
        # Calcula los índices inicial y final para el segmento actual
        start_idx = i * tam_segmento
        end_idx = (i + 1) * tam_segmento

        # Si es el último segmento, ajusta el índice final al tamaño del DataFrame
        if i == num_segmentos - 1:
            end_idx = len(df)

        # Obtiene el segmento actual del DataFrame
        segmento_df = df.iloc[start_idx:end_idx]

        # Aplica la transformación a la columna 'crew' usando el método apply
        segmento_df['crew'] = segmento_df['crew'].apply(extract_director)

        # Hace que los cambios se vean reflejados en el dataframe original
        df.iloc[start_idx:end_idx] = segmento_df

    return df

def extract_director(value):
    # Transforma la fila en la columna 'crew' en una cadena de texto
    fila = str(value)
    # Utiliza expresión regular para encontrar los substrings entre {} (los diccionarios en la fila)
    diccionarios_en_la_fila = re.findall(r'{.*?}', fila)

    # Una lista de los directores asociados al film actual en el loop
    director_row = []

    for diccionario in diccionarios_en_la_fila:
        match = re.search(r"name': '([^']*)", diccionario)

        if match:
            director_h = match.group(1)

            match = re.search(r"job': '([^']*)", diccionario)

            if match:
                job = match.group(1)

                if job == 'Director' and director_h:
                    director_row.append(director_h)

    # Devuelve la lista de directores como string
    return json.dumps(director_row)


#-----------------------------------------------------------------------------------------------


def fillna_revenue_and_budget(df: pd.DataFrame):
    
    # Rellena los valores faltantes en la columna 'revenue' con 0
    df['revenue'].fillna(value=0, inplace=True)
    
    # Rellena los valores faltantes en la columna 'budget' con 0
    df['budget'].fillna(value=0, inplace=True)
    
    # Devuelve el DataFrame modificado
    return df


#-----------------------------------------------------------------------------------------------


def dropna_release_date(df: pd.DataFrame):
    
    # Convierte la columna 'release_date' al formato datetime, permitiendo errores y valores no válidos
    df['release_date'] = pd.to_datetime(df['release_date'], format='%Y-%m-%d', errors='coerce')
    
    # Elimina las filas que tienen valores faltantes en la columna 'release_date'
    df.dropna(subset=['release_date'], inplace=True)
    
    # Devuelve el DataFrame modificado
    return df


#-----------------------------------------------------------------------------------------------


def add_release_year_column(df: pd.DataFrame):
    if 'release_year' in df.columns:
        df = df.drop('release_year', axis=1)  # Eliminar la columna 'release_year' si ya existe
        
    # Convierte la columna 'release_date' al formato datetime, permitiendo errores y valores no válidos
    df['release_date'] = pd.to_datetime(df['release_date'], format='%Y-%m-%d', errors='coerce')
    
    # Obtiene el índice de la columna 'release_date'
    release_date_idx = df.columns.get_loc('release_date')
    
    # Inserta una nueva columna 'release_year' después de la columna 'release_date'
    df.insert(release_date_idx + 1, 'release_year', df['release_date'].dt.strftime('%Y'))
    
    # Devuelve el DataFrame modificado
    return df


#-----------------------------------------------------------------------------------------------


def add_return_column(df: pd.DataFrame):
    
    if 'return' in df.columns:
        df = df.drop('return', axis=1)  # Eliminar la columna 'inversion' si ya existe
        
    # Convertir las columnas revenue y budget en numéricas
    df['revenue'] = pd.to_numeric(df['revenue'], errors='coerce')
    df['budget'] = pd.to_numeric(df['budget'], errors='coerce')
    
    # Calcular el retorno de inversión
    df['return'] = df.apply(lambda row: row['revenue'] / row['budget'] if (pd.notnull(row['revenue']) and pd.notnull(row['budget']) and row['budget']!=0) else 0, axis=1)
    
    return df 


#-----------------------------------------------------------------------------------------------


def drop_useless_columns(df: pd.DataFrame):
    
    # En realidad voy a eliminar todas las columnas solicitadas a excepcion de 'adult' ya que la considero util en el ml
    columns_to_drop = ['video', 'imdb_id', 'original_title', 'poster_path', 'homepage']

    # Filtra las columnas existentes en el DataFrame
    columns_to_drop = [column for column in columns_to_drop if column in df.columns]
    
    # Verifica si hay columnas para eliminar
    if columns_to_drop:
        
        # Elimina las columnas especificadas del DataFrame
        df.drop(columns_to_drop, axis=1, inplace=True)
        
    # Devuelve el DataFrame modificado
    return df