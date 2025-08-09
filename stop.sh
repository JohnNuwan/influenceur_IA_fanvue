#!/bin/bash

# Script d'arrêt pour Influenceur IA
echo "🛑 Arrêt d'Influenceur IA..."

# Arrêter les services
echo "🐳 Arrêt des services Docker..."
docker-compose down

echo ""
echo "✅ Influenceur IA est arrêté !"
echo ""
echo "💡 Pour redémarrer : ./start.sh"
echo "🗑️  Pour supprimer les volumes : docker-compose down -v"
