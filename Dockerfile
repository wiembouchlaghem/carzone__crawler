# ===============================
# Image de base Python 3.12 slim
# ===============================
FROM python:3.12-slim

# ===============================
# Dépendances système pour Chrome et Selenium
# ===============================
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    ca-certificates \
    unzip \
    fonts-liberation \
    libnss3 \
    libatk-bridge2.0-0 \
    libxkbcommon0 \
    libxcomposite1 \
    libxrandr2 \
    libgbm1 \
    libasound2 \
    libxdamage1 \
    libxshmfence1 \
    libgtk-3-0 \
    && rm -rf /var/lib/apt/lists/*

# ===============================
# Installation Google Chrome
# ===============================
RUN mkdir -p /etc/apt/keyrings \
    && wget -q https://dl.google.com/linux/linux_signing_key.pub \
       -O /etc/apt/keyrings/google-chrome.gpg \
    && echo "deb [arch=amd64 signed-by=/etc/apt/keyrings/google-chrome.gpg] \
       http://dl.google.com/linux/chrome/deb/ stable main" \
       > /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# ===============================
# Variables d'environnement
# ===============================
ENV PYTHONUNBUFFERED=1 \
    OUTPUT_DIR="/app/cars_list_200_output"

# ===============================
# Répertoire de travail
# ===============================
WORKDIR /app

# ===============================
# Dépendances Python
# ===============================
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ===============================
# Copie du script crawler.py
# ===============================
COPY crawler.py .

# Créer le dossier de sortie (pour HTML)
RUN mkdir -p /app/cars_list_200_output

# ===============================
# Commande par défaut
# ===============================
CMD ["python", "crawler.py"]