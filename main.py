from fastapi import FastAPI, HTTPException  # type: ignore
import pandas as pd

app= FastAPI()

dataset = pd.read_csv("./Data/movies_dataset_clean.csv")


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
