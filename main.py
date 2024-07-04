from fastapi import FastAPI, HTTPException  # type: ignore
import pandas as pd

app= FastAPI()

dataset = pd.read_csv("./Data/movies_dataset_clean.csv")
credits_data = pd.read_csv("./Data/credits_clean.csv")

@app.get('/cantidad_filmaciones_mes')
def cantidad_filmaciones_mes(Mes: str):
    
        # Diccionario 
        mes_dict = {
            'enero': 'January',
            'febrero': 'February',
            'marzo': 'March',
            'abril': 'April',
            'mayo': 'May',
            'junio': 'June',
            'julio': 'July',
            'agosto': 'August',
            'septiembre': 'September',
            'octubre': 'October',
            'noviembre': 'November',
            'diciembre': 'December'
        }
        
        # Convertir el nombre en ingles
        if Mes.lower() in mes_dict:
            english_month = mes_dict[Mes.lower()]
        else:
            return f'Mes {Mes} no es valido.'

         # Convertir release_date a datetime
        dataset['release_date'] = pd.to_datetime(dataset['release_date'], errors='coerce')
        
        # cantidad de peliculas estrenadas en el mes
        cantidad_de_peliculas = dataset[dataset['release_date'].dt.month_name() == english_month].shape[0]
        
        return f"{cantidad_de_peliculas} películas fueron estrenadas en el mes de {Mes}"

@app.get('/cantidad_filmaciones_dia')
def cantidad_filmaciones_dia(Dia: str):

    dias_dict = {
    'lunes': 'Monday',
    'martes': 'Tuesday',
    'miercoles': 'Wednesday',
    'jueves': 'Thursday',
    'viernes': 'Friday',
    'sabado': 'Saturday',
    'domingo': 'Sunday'
    }

    # Convertir el nombre del día a inglés
    if Dia.lower() in dias_dict:
        english_day = dias_dict[Dia.lower()]
    else:
        return {'error': f'Día {Dia} no es válido.'}

    # Convertir release_date a datetime
    dataset['release_date'] = pd.to_datetime(dataset['release_date'], errors='coerce')

    # Filtrar el dataset por el día de la semana
    cantidad_de_filmaciones = dataset[dataset['release_date'].dt.day_name() == english_day].shape[0]

    return f"{cantidad_de_filmaciones} peliculas fueron estrenadas el dia {Dia}"  

@app.get('/score_titulo')
def score_titulo(titulo_pelicula: str):
    # Filtrar el dataset por el título de la filmación
    filmacion = dataset[dataset['title'].str.lower() == titulo_pelicula.lower()]
    
    if filmacion.empty:
        return {"error": f"No se encontró la filmación con el título {titulo_pelicula}."}

    # Obtener los datos de la filmación
    titulo = filmacion.iloc[0]['title']
    estreno = filmacion.iloc[0]['release_year']
    score = filmacion.iloc[0]['popularity']  # o 'score', dependiendo de cómo esté nombrada la columna en tu dataset

    return f"La película {titulo} fue estrenada en el año {estreno} con un score/popularidad de {score}"

@app.get('/votos_titulo')
def votos_titulo(titulo_de_la_filmacion: str):
    # Filtrar el dataset por el título de la filmación
    filmacion = dataset[dataset['title'].str.lower() == titulo_de_la_filmacion.lower()]
    
    if filmacion.empty:
        return {"error": f"No se encontró la filmación con el título {titulo_de_la_filmacion}."}

    # Obtener los datos de la filmación
    titulo = filmacion.iloc[0]['title']
    estreno = filmacion.iloc[0]['release_year']
    votos = filmacion.iloc[0]['vote_count']
    promedio_votos = filmacion.iloc[0]['vote_average']

    if votos < 2000:
        return f"La película {titulo} fue estrenada en el año {estreno}. La misma no cuenta con al menos 2000 valoraciones, por lo que no se devuelve ningún valor."

    return f"La película {titulo} fue estrenada en el año {estreno}. La misma cuenta con un total de {votos} valoraciones, con un promedio de {promedio_votos}."


@app.get('/get_actor')
def get_actor(nombre_actor):
    
    nombre_actor = nombre_actor.lower()
    
    # Filtrar las películas en las que ha participado el actor
    actor_movies = credits_data[credits_data['cast'].apply(lambda x: nombre_actor in x.lower())]
    
    if actor_movies.empty:
        return {"error": f"Actor '{nombre_actor}' no encontrado en ninguna película."}
    
    # Obtener los IDs de las películas en las que ha participado el actor
    movie_ids = actor_movies['id'].tolist()
    
    # Filtrar el otro dataset por las películas en las que ha participado el actor
    actor_movies_return = dataset[dataset['id'].isin(movie_ids)]
    
    # Calcular métricas
    total_movies = len(actor_movies_return)
    total_return = actor_movies_return['return'].sum()
    average_return = total_return / total_movies if total_movies > 0 else 0
    
    return f"El actor {nombre_actor.title()} ha participado en {total_movies} filmaciones, el mismo ha consegido un retorno de {total_return} con un promedio de {average_return} por filmacion "

@app.get('/get_director')
def get_director(nombre_director: str):
    nombre_director = nombre_director.strip().lower()  # Normalizar el nombre del director
    
    # Filtrar las películas en las que ha trabajado el director
    director_movies = credits_data[credits_data['crew'].apply(lambda x: isinstance(x, str) and nombre_director in x.lower())]
    
    if director_movies.empty:
        return {"error": f"Director '{nombre_director.title()}' no encontrado en ninguna película."}
    
    # Unir con el dataset de películas para obtener los datos necesarios
    director_movie_ids = director_movies['id']
    director_movies_data = dataset[dataset['id'].isin(director_movie_ids)]
    
    # Calcular métricas
    total_return = director_movies_data['return'].sum()
    movie_details = director_movies_data[['title', 'release_date', 'return', 'budget', 'revenue']].to_dict(orient='records')
    
    # Formatear los nombres de las películas
    formatted_movie_details = []
    for movie in movie_details:
        movie['title'] = movie['title'].title()  # Asegura que el título esté capitalizado
        formatted_movie_details.append(movie)
    
    return {
        "director": nombre_director.title(),  # Devolver el nombre del director capitalizado
        "total_return": total_return,
        "movies": formatted_movie_details
    }




    

    

