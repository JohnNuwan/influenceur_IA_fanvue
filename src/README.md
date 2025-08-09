# 🚀 Backend FastAPI - Influenceur IA

Backend API pour le système d'automatisation multi-influenceuses avec IA.

## 📋 Table des matières

- [Fonctionnalités](#-fonctionnalités)
- [Architecture](#-architecture)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Utilisation](#-utilisation)
- [API Endpoints](#-api-endpoints)
- [Développement](#-développement)
- [Déploiement](#-déploiement)

## ✨ Fonctionnalités

### 🎯 Core Features
- **Multi-tenant** : Gestion de plusieurs influenceuses
- **Authentification JWT** : Sécurisé avec tokens
- **Base de données PostgreSQL** : Stockage persistant
- **Redis** : Cache et sessions
- **Logging structuré** : Avec structlog

### 🤖 IA & Automatisation
- **Ollama Integration** : Chatbot IA local
- **Génération de contenu** : Images, vidéos, textes
- **Réponses automatiques** : Chatbot intelligent
- **Analytics avancés** : Métriques et insights

### 📊 Analytics & Monitoring
- **Métriques en temps réel** : Performance et engagement
- **Analytics détaillés** : Revenus, audience, contenu
- **Monitoring** : Health checks et alertes
- **Logs structurés** : Traçabilité complète

### 🔗 Intégrations
- **Réseaux sociaux** : Twitter, Instagram, TikTok
- **Plateformes de contenu** : Fanvue, OnlyFans
- **Stockage** : MinIO/S3 compatible
- **APIs externes** : Stable Diffusion, Midjourney

## 🏗️ Architecture

```
src/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── endpoints/          # Endpoints API
│   │       │   ├── auth.py         # Authentification
│   │       │   ├── users.py        # Gestion utilisateurs
│   │       │   ├── influenceuses.py # Gestion influenceuses
│   │       │   ├── content.py      # Gestion contenu
│   │       │   ├── chatbot.py      # Chatbot Ollama
│   │       │   ├── social_media.py # Réseaux sociaux
│   │       │   ├── analytics.py    # Analytics
│   │       │   ├── sales.py        # Ventes
│   │       │   └── health.py       # Health checks
│   │       └── api.py              # Router principal
│   ├── core/
│   │   ├── config.py               # Configuration
│   │   ├── database.py             # Base de données
│   │   ├── security.py             # Sécurité
│   │   └── logging.py              # Logging
│   └── models/                     # Modèles SQLAlchemy
│       ├── user.py                 # Utilisateurs
│       ├── influenceuse.py         # Influenceuses
│       ├── content.py              # Contenu
│       └── conversation.py         # Conversations
├── main.py                         # Point d'entrée
└── requirements.txt                # Dépendances
```

## 🛠️ Installation

### Prérequis
- Python 3.9+
- PostgreSQL 13+
- Redis 6+
- Docker (optionnel)

### Installation locale

1. **Cloner le projet**
```bash
git clone <repository>
cd src
```

2. **Créer un environnement virtuel**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows
```

3. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

4. **Configuration de l'environnement**
```bash
cp .env.example .env
# Éditer .env avec vos configurations
```

5. **Base de données**
```bash
# Créer la base de données PostgreSQL
createdb influenceur_ia

# Appliquer les migrations (si Alembic est configuré)
alembic upgrade head
```

### Migrations avec Docker (recommandé)

```bash
# Démarrer uniquement Postgres
docker-compose up -d postgres

# Générer une migration depuis les modèles
docker-compose run --rm backend alembic -c src/alembic.ini revision --autogenerate -m "initial schema"

# Appliquer les migrations
docker-compose run --rm backend alembic -c src/alembic.ini upgrade head
```

6. **Lancer l'application**
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## ⚙️ Configuration

### Variables d'environnement

Créer un fichier `.env` :

```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/influenceur_ia
REDIS_URL=redis://localhost:6379

# Security
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# External APIs
OPENAI_API_KEY=your-openai-key
REPLICATE_API_TOKEN=your-replicate-token

# Social Media APIs
TWITTER_API_KEY=your-twitter-key
TWITTER_API_SECRET=your-twitter-secret
INSTAGRAM_ACCESS_TOKEN=your-instagram-token

# Storage
MINIO_ENDPOINT=localhost:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin
MINIO_BUCKET_NAME=influenceur-ia

# Ollama
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=llama2:7b

# Monitoring
SENTRY_DSN=your-sentry-dsn
PROMETHEUS_ENABLED=true

# Logging
LOG_LEVEL=INFO
LOG_FORMAT=json
```

## 🚀 Utilisation

### Démarrage rapide

1. **Lancer l'application**
```bash
uvicorn main:app --reload
```

2. **Accéder à la documentation**
- Swagger UI : http://localhost:8000/docs
- ReDoc : http://localhost:8000/redoc

3. **Health check**
```bash
curl http://localhost:8000/health
```

### Exemples d'utilisation

#### Authentification
```bash
# Créer un utilisateur
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "username": "testuser",
    "password": "password123",
    "full_name": "Test User"
  }'

# Se connecter
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=test@example.com&password=password123"
```

#### Gestion des influenceuses
```bash
# Créer une influenceuse
curl -X POST "http://localhost:8000/api/v1/influenceuses/" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "stage_name": "TestInfluenceuse",
    "bio": "Test bio",
    "content_categories": ["lingerie", "feet"],
    "subscription_price": 50.0
  }'
```

#### Chatbot avec Ollama
```bash
# Créer une conversation
curl -X POST "http://localhost:8000/api/v1/chatbot/conversations" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "influenceuse_id": 1,
    "platform": "fanvue"
  }'

# Envoyer un message
curl -X POST "http://localhost:8000/api/v1/chatbot/conversations/1/messages" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Hello!",
    "message_type": "text",
    "sender_type": "user"
  }'
```

## 📚 API Endpoints

### 🔐 Authentification
- `POST /api/v1/auth/register` - Créer un compte
- `POST /api/v1/auth/login` - Se connecter
- `GET /api/v1/auth/me` - Informations utilisateur
- `POST /api/v1/auth/logout` - Se déconnecter

### 👥 Utilisateurs
- `GET /api/v1/users/` - Liste des utilisateurs
- `GET /api/v1/users/{id}` - Détails utilisateur
- `POST /api/v1/users/` - Créer utilisateur
- `PUT /api/v1/users/{id}` - Modifier utilisateur
- `DELETE /api/v1/users/{id}` - Supprimer utilisateur

### 🎭 Influenceuses
- `GET /api/v1/influenceuses/` - Liste des influenceuses
- `GET /api/v1/influenceuses/{id}` - Détails influenceuse
- `POST /api/v1/influenceuses/` - Créer influenceuse
- `PUT /api/v1/influenceuses/{id}` - Modifier influenceuse
- `DELETE /api/v1/influenceuses/{id}` - Supprimer influenceuse
- `GET /api/v1/influenceuses/{id}/stats` - Statistiques

### 📄 Contenu
- `GET /api/v1/content/` - Liste du contenu
- `GET /api/v1/content/{id}` - Détails contenu
- `POST /api/v1/content/` - Créer contenu
- `PUT /api/v1/content/{id}` - Modifier contenu
- `DELETE /api/v1/content/{id}` - Supprimer contenu
- `POST /api/v1/content/{id}/publish` - Publier contenu
- `POST /api/v1/content/{id}/archive` - Archiver contenu

### 🤖 Chatbot
- `GET /api/v1/chatbot/conversations` - Liste conversations
- `POST /api/v1/chatbot/conversations` - Créer conversation
- `GET /api/v1/chatbot/conversations/{id}` - Détails conversation
- `POST /api/v1/chatbot/conversations/{id}/messages` - Envoyer message
- `GET /api/v1/chatbot/conversations/{id}/messages` - Messages conversation
- `POST /api/v1/chatbot/ollama/generate` - Générer avec Ollama

### 📱 Réseaux sociaux
- `POST /api/v1/social-media/{id}/post` - Créer post
- `GET /api/v1/social-media/{id}/posts` - Posts
- `GET /api/v1/social-media/{id}/analytics` - Analytics
- `POST /api/v1/social-media/{id}/sync` - Synchroniser

### 📊 Analytics
- `GET /api/v1/analytics/{id}/overview` - Vue d'ensemble
- `GET /api/v1/analytics/{id}/revenue` - Analytics revenus
- `GET /api/v1/analytics/{id}/engagement` - Analytics engagement
- `GET /api/v1/analytics/{id}/content` - Analytics contenu
- `GET /api/v1/analytics/{id}/audience` - Analytics audience

### 💰 Ventes
- `POST /api/v1/sales/` - Créer vente
- `GET /api/v1/sales/{id}` - Ventes influenceuse
- `GET /api/v1/sales/{id}/summary` - Résumé ventes

### 🏥 Health
- `GET /api/v1/health/` - Health check basique
- `GET /api/v1/health/detailed` - Health check détaillé

## 🛠️ Développement

### Structure du projet
```
src/
├── app/
│   ├── api/                    # API endpoints
│   ├── core/                   # Configuration core
│   ├── models/                 # Modèles de données
│   └── services/               # Services métier
├── tests/                      # Tests
├── alembic/                    # Migrations DB
├── docker/                     # Configuration Docker
└── docs/                       # Documentation
```

### Tests
```bash
# Lancer les tests
pytest

# Tests avec couverture
pytest --cov=app

# Tests spécifiques
pytest tests/test_auth.py
```

### Linting et formatage
```bash
# Black (formatage)
black app/

# isort (imports)
isort app/

# flake8 (linting)
flake8 app/

# mypy (type checking)
mypy app/
```

### Migrations de base de données
```bash
# Créer une migration
alembic revision --autogenerate -m "Description"

# Appliquer les migrations
alembic upgrade head

# Revenir en arrière
alembic downgrade -1
```

## 🐳 Déploiement

### Docker

1. **Construire l'image**
```bash
docker build -t influenceur-ia-backend .
```

2. **Lancer avec Docker Compose**
```bash
docker-compose up -d
```

### Production

1. **Variables d'environnement**
```bash
# Configurer les variables de production
export DATABASE_URL="postgresql://user:pass@prod-db:5432/influenceur_ia"
export SECRET_KEY="your-production-secret"
export LOG_LEVEL="WARNING"
```

2. **Lancer avec Gunicorn**
```bash
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

3. **Reverse Proxy (Nginx)**
```nginx
server {
    listen 80;
    server_name api.influenceur-ia.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 📈 Monitoring

### Métriques
- **Prometheus** : Métriques système et application
- **Grafana** : Dashboards de monitoring
- **Sentry** : Gestion d'erreurs
- **ELK Stack** : Logs et analytics

### Health Checks
- `/health` : Vérification basique
- `/health/detailed` : Vérification complète (DB, Redis, APIs)

## 🔒 Sécurité

### Authentification
- JWT tokens avec expiration
- Hachage bcrypt des mots de passe
- Refresh tokens (à implémenter)

### Autorisation
- Rôles utilisateurs (admin, manager, influenceuse, support)
- Permissions granulaires
- Audit logs

### Protection
- Rate limiting
- CORS configuré
- Validation des entrées
- Sanitisation des données

## 🤝 Contribution

1. Fork le projet
2. Créer une branche feature
3. Commiter les changements
4. Pousser vers la branche
5. Ouvrir une Pull Request

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 🆘 Support

- **Documentation** : `/docs` (Swagger UI)
- **Issues** : GitHub Issues
- **Email** : support@influenceur-ia.com

---

**Influenceur IA Backend** - Système d'automatisation multi-influenceuses avec IA
