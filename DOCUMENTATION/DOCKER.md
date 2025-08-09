# 🐳 Guide Docker - Influenceur IA

Ce guide explique comment utiliser l'environnement Docker pour le projet Influenceur IA.

## 🚀 Démarrage rapide

### Prérequis
- Docker installé et en cours d'exécution
- Docker Compose installé
- Au moins 8GB de RAM disponible
- Au moins 20GB d'espace disque

### Démarrage automatique
```bash
# Rendre les scripts exécutables
chmod +x start.sh stop.sh

# Démarrer l'environnement
./start.sh
```

### Démarrage manuel
```bash
# Créer le réseau Traefik
docker network create traefik-public

# Créer le fichier acme.json pour Traefik
mkdir -p traefik
touch traefik/acme.json
chmod 600 traefik/acme.json

# Copier le fichier d'environnement
cp env.example .env

# Démarrer les services
docker-compose up -d
```

## 🛑 Arrêt

```bash
# Arrêt simple
./stop.sh

# Ou manuellement
docker-compose down

# Pour supprimer aussi les volumes (⚠️ ATTENTION : supprime toutes les données)
docker-compose down -v
```

## 🌐 Services accessibles

Une fois démarré, vous pouvez accéder aux services suivants :

| Service | URL | Description |
|---------|-----|-------------|
| **API Backend** | http://api.localhost | API FastAPI principale |
| **Traefik Dashboard** | http://traefik.localhost:8080 | Interface de routage Traefik |
| **Portainer** | http://portainer.localhost | Gestion Docker |
| **MinIO Console** | http://minio.localhost | Gestion des fichiers S3 |
| **Flower** | http://flower.localhost | Monitoring Celery |
| **Prometheus** | http://prometheus.localhost | Métriques système |
| **Grafana** | http://grafana.localhost | Tableaux de bord (admin/admin) |

## 🔧 Configuration

### Variables d'environnement
1. Copier `env.example` vers `.env`
2. Modifier les valeurs selon votre environnement
3. Redémarrer les services : `docker-compose restart`

### Fichiers de configuration
- `docker-compose.yml` : Configuration des services
- `Dockerfile` : Image du backend FastAPI
- `monitoring/prometheus.yml` : Configuration Prometheus
- `init-scripts/01-init-db.sql` : Initialisation base de données

## 📊 Monitoring

### Logs des services
```bash
# Tous les services
docker-compose logs -f

# Service spécifique
docker-compose logs -f backend
docker-compose logs -f postgres
docker-compose logs -f ollama
```

### Métriques
- **Prometheus** : Collecte des métriques
- **Grafana** : Visualisation des métriques
- **Flower** : Monitoring des tâches Celery

### Health checks
Tous les services ont des health checks configurés :
```bash
# Vérifier l'état des services
docker-compose ps

# Voir les health checks en temps réel
watch docker-compose ps
```

## 🗄️ Base de données

### Accès direct
```bash
# Se connecter à PostgreSQL
docker-compose exec postgres psql -U postgres -d influenceur_ia

# Voir les logs PostgreSQL
docker-compose logs -f postgres
```

### Données de démonstration
L'utilisateur admin par défaut est créé automatiquement :
- **Email** : admin@influenceur-ia.com
- **Mot de passe** : admin123

### Sauvegarde
```bash
# Créer une sauvegarde
docker-compose exec postgres pg_dump -U postgres influenceur_ia > backup.sql

# Restaurer une sauvegarde
docker-compose exec -T postgres psql -U postgres -d influenceur_ia < backup.sql
```

## 🤖 Ollama (LLMs locaux)

### Modèles disponibles
Par défaut, aucun modèle n'est téléchargé. Pour télécharger des modèles :

```bash
# Accéder au conteneur Ollama
docker-compose exec ollama ollama

# Télécharger des modèles
ollama pull llama2
ollama pull mistral
ollama pull codellama
```

### Configuration GPU
Pour utiliser le GPU (NVIDIA) :
1. Installer NVIDIA Docker
2. Vérifier que `nvidia-smi` fonctionne
3. Le conteneur Ollama utilisera automatiquement le GPU

### Modèles personnalisés
Placez vos modèles personnalisés dans `./ollama-models/`

## 📁 Stockage MinIO

### Accès S3
- **Endpoint** : http://localhost:9000
- **Access Key** : minioadmin
- **Secret Key** : minioadmin
- **Region** : us-east-1

### Créer un bucket
```bash
# Via l'interface web
http://minio.localhost

# Ou via AWS CLI
aws --endpoint-url http://localhost:9000 s3 mb s3://influenceur-ia
```

## 🔄 Celery (Tâches asynchrones)

### Workers
```bash
# Voir les workers actifs
docker-compose logs -f celery

# Redémarrer les workers
docker-compose restart celery
```

### Monitoring
- **Flower** : http://flower.localhost
- **Redis** : http://localhost:6379

## 🚨 Dépannage

### Problèmes courants

#### Ports déjà utilisés
```bash
# Voir quels ports sont utilisés
netstat -tulpn | grep :80
netstat -tulpn | grep :5432

# Arrêter les services qui utilisent ces ports
sudo systemctl stop apache2  # exemple
```

#### Problèmes de permissions
```bash
# Corriger les permissions des volumes
sudo chown -R $USER:$USER ./logs
sudo chown -R $USER:$USER ./traefik
```

#### Problèmes de réseau
```bash
# Recréer le réseau Traefik
docker network rm traefik-public
docker network create traefik-public
```

#### Problèmes de base de données
```bash
# Redémarrer PostgreSQL
docker-compose restart postgres

# Vérifier les logs
docker-compose logs postgres
```

### Logs détaillés
```bash
# Logs avec timestamps
docker-compose logs -f --timestamps

# Logs des 100 dernières lignes
docker-compose logs --tail=100
```

## 🔒 Sécurité

### Variables sensibles
- Ne jamais commiter le fichier `.env`
- Changer les mots de passe par défaut en production
- Utiliser des secrets Docker en production

### Accès réseau
- Seuls les ports nécessaires sont exposés
- Traefik gère le routage et la sécurité
- Les services internes ne sont pas exposés

## 📈 Performance

### Ressources recommandées
- **CPU** : 4+ cœurs
- **RAM** : 8GB+ (16GB recommandé)
- **Disque** : SSD recommandé
- **GPU** : Optionnel pour Ollama

### Optimisations
- Les volumes sont persistants
- Les images sont optimisées
- Health checks pour la stabilité
- Monitoring intégré

## 🚀 Production

### Variables d'environnement
```bash
# Créer un fichier .env.prod
cp env.example .env.prod

# Modifier les valeurs pour la production
# Désactiver DEBUG
# Changer les mots de passe
# Configurer les domaines
```

### Déploiement
```bash
# Utiliser le fichier de production
docker-compose --env-file .env.prod up -d

# Ou créer un docker-compose.prod.yml
docker-compose -f docker-compose.prod.yml up -d
```

## 📚 Ressources

- [Documentation Docker](https://docs.docker.com/)
- [Documentation Traefik](https://doc.traefik.io/traefik/)
- [Documentation Portainer](https://docs.portainer.io/)
- [Documentation Ollama](https://ollama.ai/docs)
- [Documentation MinIO](https://min.io/docs/)

## 🤝 Support

En cas de problème :
1. Vérifier les logs : `docker-compose logs -f [service]`
2. Vérifier l'état : `docker-compose ps`
3. Consulter ce guide
4. Vérifier la roadmap du projet
