FROM python:3.10-slim

# Tools install karna
RUN apt-get update && apt-get install -y wget unzip curl

# Direct Chrome file download aur install
RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN apt-get install -y ./google-chrome-stable_current_amd64.deb
RUN rm google-chrome-stable_current_amd64.deb

WORKDIR /app

# Requirements aur code copy karna
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Server ko live karna (Render default port 10000 use karta hai par hum dynamically handle karenge)
CMD ["sh", "-c", "uvicorn app:app --host 0.0.0.0 --port ${PORT:-10000}"]
