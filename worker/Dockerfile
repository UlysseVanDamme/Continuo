FROM python:3.12-slim

# System libs needed for MIDI processing
RUN apt-get update && apt-get install -y libasound2-dev gcc python3-dev && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY worker.py .

CMD ["python", "worker.py"]