#!/bin/bash

# Script de rangement léger (sûr) pour Influenceur IA
# Déplace documentation secondaire et modules, garde Docker & scripts à la racine

set -euo pipefail

echo "🔄 Rangement de la documentation..."

mkdir -p DOCUMENTATION

for f in ROADMAP.md DOCKER.md architecture_automatisation.md previsionnel_multi_influenceuses.md pack_influenceuse_fanvue_nsfl.md; do
  if [ -f "$f" ]; then
    echo "📚 Déplacement de $f → DOCUMENTATION/"
    mv "$f" DOCUMENTATION/
  fi
done

# Déplacer modules vers DOCUMENTATION/modules
if [ -d modules ]; then
  mkdir -p DOCUMENTATION/modules
  echo "📁 Déplacement du dossier modules → DOCUMENTATION/modules"
  mv modules/* DOCUMENTATION/modules/ 2>/dev/null || true
  rmdir modules 2>/dev/null || true
fi

# Déplacer project.config vers CONFIGURATION/
if [ -f project.config ]; then
  mkdir -p CONFIGURATION
  echo "🔧 Déplacement de project.config → CONFIGURATION/project.config"
  mv project.config CONFIGURATION/project.config
fi

echo "✅ Fini. README.md reste à la racine. Rien d’autre n’a été déplacé."
echo "ℹ️ Voir PROJECT_STRUCTURE.md pour les détails."
