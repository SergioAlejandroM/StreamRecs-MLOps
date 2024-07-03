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
    
