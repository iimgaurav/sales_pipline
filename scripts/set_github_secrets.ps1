param(
    [Parameter(Mandatory=$false)]
    [string]$SecretsFile = "secrets.json"
)

if (-not (Get-Command gh -ErrorAction SilentlyContinue)) {
    Write-Error "GitHub CLI 'gh' not found. Install from https://cli.github.com/."
    exit 1
}

if (-not (Test-Path $SecretsFile)) {
    Write-Error "Secrets file not found: $SecretsFile"
    exit 1
}

$json = Get-Content $SecretsFile -Raw | ConvertFrom-Json
foreach ($k in $json.PSObject.Properties.Name) {
    $v = $json.$k
    Write-Host "Setting secret: $k"
    gh secret set $k --body "$v"
}
