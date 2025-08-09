# PowerShell tidy script (ASCII only) for Influenceur IA
# Moves secondary documentation into DOCUMENTATION/ only
# Keeps README, Docker files, scripts, Traefik, monitoring at repo root

$ErrorActionPreference = "Stop"

Write-Host "Reorganisation de la documentation..."

if (!(Test-Path -Path "DOCUMENTATION")) {
  New-Item -ItemType Directory -Path "DOCUMENTATION" | Out-Null
}

$files = @(
  "ROADMAP.md",
  "DOCKER.md",
  "architecture_automatisation.md",
  "previsionnel_multi_influenceuses.md",
  "pack_influenceuse_fanvue_nsfl.md"
)

foreach ($f in $files) {
  if (Test-Path -Path $f) {
    Write-Host ("Deplacement de {0} -> DOCUMENTATION" -f $f)
    Move-Item -Path $f -Destination "DOCUMENTATION" -Force
  }
}

# Move modules docs into DOCUMENTATION/modules
if (Test-Path -Path "modules") {
  if (!(Test-Path -Path "DOCUMENTATION/modules")) {
    New-Item -ItemType Directory -Path "DOCUMENTATION/modules" | Out-Null
  }
  Write-Host "Deplacement du dossier 'modules' -> DOCUMENTATION/modules"
  Move-Item -Path "modules/*" -Destination "DOCUMENTATION/modules" -Force
  Remove-Item -Recurse -Force "modules" -ErrorAction SilentlyContinue
}

# Move project.config into CONFIGURATION/
if (Test-Path -Path "project.config") {
  if (!(Test-Path -Path "CONFIGURATION")) {
    New-Item -ItemType Directory -Path "CONFIGURATION" | Out-Null
  }
  Write-Host "Deplacement de project.config -> CONFIGURATION/project.config"
  Move-Item -Path "project.config" -Destination "CONFIGURATION/project.config" -Force
}

Write-Host "Fini. README.md reste a la racine. Rien de critique n'a ete deplace."
Write-Host "Voir PROJECT_STRUCTURE.md pour les details."
