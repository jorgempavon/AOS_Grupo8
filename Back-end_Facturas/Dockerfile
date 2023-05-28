# Imagen base de Python
FROM python:3.8


WORKDIR /app

# Copia de las dependencias del back y script de inicializacion de la BD
COPY requirements.txt .
COPY init.sql .

# Creacion y activacion del entorno virtual
RUN python -m venv venv
RUN /bin/bash -c "source venv/bin/activate"

# Instalacion de las dependencias del back
RUN pip install --no-cache-dir -r requirements.txt
# Instalacion de dependencia para que no se comience a  ejecutar el back-end de la aplicación antes que la base de datos
RUN apt-get update && apt-get install -y netcat
WORKDIR /app/Software
COPY Software/ .

RUN ls -la
 
EXPOSE 5000
CMD ["python","app.py"]


