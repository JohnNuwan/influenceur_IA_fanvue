# Dockerfile pour le backend FastAPI
FROM python:3.11-slim

# Définir le répertoire de travail
WORKDIR /app

# Installer les dépendances système
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copier un set minimal de dépendances pour build/migrations
COPY src/requirements.base.txt ./requirements.txt

# Installer les dépendances Python minimales
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code source
COPY src/ ./src/

# Définir le répertoire de travail sur le code
WORKDIR /app/src

# S'assurer que les imports 'app.*' fonctionnent (reloader inclus)
ENV PYTHONPATH=/app/src

# Créer un utilisateur non-root pour la sécurité
RUN useradd --create-home --shell /bin/bash app \
    && chown -R app:app /app
USER app

# Exposer le port
EXPOSE 8000

# Entrypoint qui prépare PYTHONPATH et lance uvicorn
COPY entrypoint.sh /entrypoint.sh
CMD ["sh", "/entrypoint.sh"]
