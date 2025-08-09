$ErrorActionPreference = 'Stop'

function Ensure-HostEntry {
  param(
    [Parameter(Mandatory=$true)][string]$Hostname,
    [string]$IP = '127.0.0.1'
  )
  $hosts = "$env:windir\System32\drivers\etc\hosts"
  $entry = "$IP`t$Hostname"
  $content = Get-Content -Path $hosts -ErrorAction Stop
  if ($content -notmatch "\b$Hostname\b") {
    Add-Content -Path $hosts -Value $entry
    Write-Host "Added: $entry"
  } else {
    Write-Host "Exists: $Hostname"
  }
}

Write-Host "Updating hosts file (requires admin)..."
Ensure-HostEntry -Hostname 'api.localhost'
Ensure-HostEntry -Hostname 'traefik.localhost'
Ensure-HostEntry -Hostname 'portainer.localhost'
Ensure-HostEntry -Hostname 'minio.localhost'
Ensure-HostEntry -Hostname 'flower.localhost'
Ensure-HostEntry -Hostname 'prometheus.localhost'
Ensure-HostEntry -Hostname 'grafana.localhost'
Write-Host "Done."

