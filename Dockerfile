# Usa un'immagine base Python leggera
FROM python:3.12-slim

# Imposta la directory di lavoro dentro il container
WORKDIR /app

# Copia i file della repo nel container
COPY . /app

# Aggiorna pip e installa le dipendenze
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Crea le cartelle per immagini e soluzioni se non esistono
RUN mkdir -p images solutions

# Esponi la porta su cui Flask gira
EXPOSE 5000

# Imposta l'entrypoint per avviare il server
ENTRYPOINT ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "server:app"]
