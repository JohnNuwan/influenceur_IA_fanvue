#!/bin/bash

# Script de démarrage pour Influenceur IA
echo "🚀 Démarrage d'Influenceur IA..."

# Vérifier que Docker est installé et en cours d'exécution
if ! command -v docker &> /dev/null; then
    echo "❌ Docker n'est pas installé. Veuillez l'installer d'abord."
    exit 1
fi

if ! docker info &> /dev/null; then
    echo "❌ Docker n'est pas en cours d'exécution. Veuillez le démarrer."
    exit 1
fi

# Vérifier que Docker Compose est installé
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose n'est pas installé. Veuillez l'installer d'abord."
    exit 1
fi

# Créer le réseau Traefik s'il n'existe pas
if ! docker network ls | grep -q "traefik-public"; then
    echo "🌐 Création du réseau Traefik..."
    docker network create traefik-public
fi

# Créer le fichier acme.json pour Traefik
if [ ! -d "traefik" ]; then
    mkdir -p traefik
fi

if [ ! -f "traefik/acme.json" ]; then
    echo "🔐 Création du fichier acme.json pour Traefik..."
    touch traefik/acme.json
    chmod 600 traefik/acme.json
fi

# Créer les dossiers nécessaires
echo "📁 Création des dossiers nécessaires..."
mkdir -p logs
mkdir -p init-scripts
mkdir -p monitoring
mkdir -p ollama-models

# Copier le fichier d'environnement s'il n'existe pas
if [ ! -f ".env" ]; then
    echo "⚙️ Copie du fichier d'environnement..."
    cp env.example .env
    echo "⚠️  N'oubliez pas de configurer le fichier .env avec vos vraies valeurs !"
fi

# Démarrer les services
echo "🐳 Démarrage des services Docker..."
docker-compose up -d

# Attendre que les services soient prêts
echo "⏳ Attente du démarrage des services..."
sleep 30

# Vérifier l'état des services
echo "🔍 Vérification de l'état des services..."
docker-compose ps

echo ""
echo "✅ Influenceur IA est démarré !"
echo ""
echo "🌐 Services accessibles :"
echo "   - API Backend: http://api.localhost"
echo "   - Traefik Dashboard: http://traefik.localhost:8080"
echo "   - Portainer: http://portainer.localhost"
echo "   - MinIO Console: http://minio.localhost"
echo "   - Flower (Celery): http://flower.localhost"
echo "   - Prometheus: http://prometheus.localhost"
echo "   - Grafana: http://grafana.localhost (admin/admin)"
echo ""
echo "📝 Pour voir les logs : docker-compose logs -f [service]"
echo "🛑 Pour arrêter : ./stop.sh"
