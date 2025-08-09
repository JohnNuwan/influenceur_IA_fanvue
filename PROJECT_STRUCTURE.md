# 📁 Structure du Projet Influenceur IA

## 🏗️ Organisation simplifiée (sûre par défaut)

Nous gardons les fichiers critiques à la racine pour ne rien casser (Docker, scripts, Traefik, monitoring), et nous rangeons la documentation secondaire dans `DOCUMENTATION/`.

```
.
├── README.md
├── ROADMAP.md               (→ conseillé: déplacé dans DOCUMENTATION/)
├── DOCKER.md                (→ conseillé: déplacé dans DOCUMENTATION/)
├── architecture_automatisation.md (→ conseillé: déplacé dans DOCUMENTATION/)
├── previsionnel_multi_influenceuses.md (→ conseillé: déplacé dans DOCUMENTATION/)
├── pack_influenceuse_fanvue_nsfl.md (→ conseillé: déplacé dans DOCUMENTATION/)
├── .gitignore               # Reste à la racine
├── Dockerfile               # Reste à la racine
├── docker-compose.yml       # Reste à la racine
├── env.example              # Reste à la racine
├── start.sh / stop.sh       # Reste à la racine
├── traefik/                 # Reste à la racine
├── init-scripts/            # Reste à la racine
├── monitoring/              # Reste à la racine
├── src/                     # Code backend
└── modules/                 # Modules et docs techniques
```

## 🎯 Pourquoi ce choix ?
- Évite de casser les chemins relatifs de `docker-compose.yml` et des scripts.
- Compatible Windows (pas de symlinks requis).
- Rangement immédiat de la racine en déplaçant seulement la documentation volumineuse.

## 🚚 Ce que fait le rangement par défaut
- Crée un dossier `DOCUMENTATION/`.
- Déplace: `ROADMAP.md`, `DOCKER.md`, `architecture_automatisation.md`, `previsionnel_multi_influenceuses.md`, `pack_influenceuse_fanvue_nsfl.md`.
- Laisse `README.md` à la racine (point d’entrée du repo).

## 🧪 Option avancée (plus tard)
Quand tout sera stabilisé, on pourra regrouper Docker dans `DOCKER/` et créer des liens symboliques. Attention: sous Windows les symlinks nécessitent des permissions spécifiques. Nous le ferons plus tard pour éviter les surprises.
