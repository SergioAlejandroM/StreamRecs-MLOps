# StreamRecs-MLOps

## Proyecto Individual Nº1: MLOps para Sistema de Recomendación en Streaming

### Descripción

Este proyecto implementa un sistema de recomendación de películas utilizando técnicas de MLOps. El objetivo es desarrollar un pipeline automatizado que integre la recolección de datos, la transformación, el entrenamiento del modelo, y la implementación del sistema de recomendación en un entorno de producción.

### Estructura del Proyecto

- **Data**: Carpeta que contiene los datos utilizados para el proyecto.
- **EDA.ipynb**: Notebook que realiza el análisis exploratorio de datos.
- **Transformaciones.ipynb**: Notebook que realiza las transformaciones de los datos.
- **credits.ipynb**: Notebook que maneja los datos de créditos de películas.
- **main.py**: Script principal que contiene la lógica del sistema de recomendación.
- **requirements.txt**: Archivo que lista las dependencias del proyecto.
- **data_profile.html**: Reporte de perfilamiento de datos.

### Instalación

1. Clona el repositorio:
   ```bash
   git clone https://github.com/SergioAlejandroM/StreamRecs-MLOps.git

2. Navega al directorio del proyecto:
    ```bash
   cd StreamRecs-MLOps

3. Crea y activa un entorno virtual:
    ```bash
    python -m venv venv
    source venv/bin/activate  # En Windows usa `venv\Scripts\activate`

4. Instala dependecias:
    ```bash
    pip install -r requirements.txt


### Uso
1. Realiza el análisis exploratorio de datos ejecutando EDA.ipynb.

2. Aplica las transformaciones necesarias en Transformaciones.ipynb.

3. Ejecuta credits.ipynb para manejar los datos de créditos.

4. Corre la api:
    ```bash
    uvicorn main:app --reload

### Contacto
Para cualquier consulta, por favor contacta a Sergio Alejandro a través de [sergio.manrique303@gmail.com]. 


