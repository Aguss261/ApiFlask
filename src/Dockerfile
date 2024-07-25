# Usa una imagen base de Python
FROM python:3.9

# Define el directorio de trabajo en el contenedor
WORKDIR /app

# Copia el archivo de requisitos y luego instala las dependencias
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del código fuente
COPY . .

# Define el comando por defecto
CMD ["flask", "run", "--host=0.0.0.0"]
