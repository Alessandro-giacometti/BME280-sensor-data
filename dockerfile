FROM python:3.9-slim

WORKDIR /app

# Installa dipendenze di sistema
RUN apt-get update && apt-get install -y i2c-tools

# Installa librerie Python necessarie tramite pip
RUN pip install smbus2 bme280

# Elimina file temporanei della cache apt-get update per alleggerire il container
RUN rm -rf /var/lib/apt/lists/*

# Copia il file Python dentro il container
COPY bme280-get-sensor-data.py /app/

CMD ["python", "/app/bme280-get-sensor-data.py"]