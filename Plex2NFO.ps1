# --- Plex to Jellyfin NFO Orchestrator ---

# Prompt for the variables dynamically at runtime
$plex_ip = Read-Host "Enter your Plex Server URL (e.g., http://192.168.1.50:32400)"
$token = Read-Host "Enter your Plex Token - 'Get Info' on any media item > View XML. The token is at the end of the URL"

# Safely establish the working directory (handles both saved .ps1 files and copy/paste)
$working_dir = $PSScriptRoot
if ([string]::IsNullOrEmpty($working_dir)) {
    $working_dir = (Get-Location).Path
}
Set-Location $working_dir

Write-Host "`nFetching Plex libraries..." -ForegroundColor Cyan
$libraries_url = "$plex_ip/library/sections?X-Plex-Token=$token"

try {
    # Fetch and parse the libraries XML
    [xml]$libs = Invoke-RestMethod -Uri$libraries_url
    Write-Host "`nAvailable Libraries:" -ForegroundColor Yellow
    foreach ($dir in $libs.MediaContainer.Directory) {
        Write-Host "  Key: $($dir.key) - $($dir.title) ($($dir.type))"
    }
}
catch {
    Write-Host "Failed to connect to Plex. Double-check your IP and Token." -ForegroundColor Red
    Write-Host "Error details: $_" -ForegroundColor Red
    Pause
    exit
}

# Interactive prompt for the key
$key = Read-Host "`nEnter the Library Key for the library you want to export"

Write-Host "`nDownloading metadata.xml (this may take a moment for large libraries)..." -ForegroundColor Cyan
$metadata_url = "$plex_ip/library/sections/$key/all?includeGuids=1&X-Plex-Token=$token"
Invoke-WebRequest -Uri $metadata_url -OutFile "metadata.xml"

Write-Host "`nRunning Audit Script (PlexXMLPull.py)..." -ForegroundColor Cyan
python PlexXMLPull.py

Write-Host "`nAudit complete. Please check audit_log.txt in your folder to confirm the data looks correct." -ForegroundColor Yellow
$continue = Read-Host "Does the audit log look good? (Y/N)"

if ($continue -match "^[yY]") {
    Write-Host "`nRunning NFO Creator (JellyfinNFOCreator.py)..." -ForegroundColor Cyan
    python JellyfinNFOCreator.py
    Write-Host "`nAll done! You can now run a 'Scan All Libraries' with 'Replace all metadata' in Jellyfin." -ForegroundColor Green
}
else {
    Write-Host "`nHalting script so you can investigate the audit log." -ForegroundColor Red
}

Pause