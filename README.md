# Plex XML To Jellyfin .NFO Files

**Original Author:** [2dee11](https://github.com/2dee11)  
*Forked and updated to include exact ID matching (IMDb/TMDb/TVDb), streamlined PowerShell orchestration, and improved Collections parsing.*

> "I, probably like you reading this, wanted to convert my Plex library to Jellyfin without losing all of my years or hard work setting up Titles, Sort Titles, Original Titles, Added At Dates, Last Viewed At Dates, View Counts, and Collections.
> 
> This collection of scripts will help you do just that as easily as possible. Please note that I am by no means a developer, just an idiot on the internet with access to ChatGPT and a little know how. I tried to segment this as much as possible to try and prevent issues but use at your own risk." 
> — **2dee11**

It now pulls the exact provider IDs (TMDb, IMDb, TVDb) straight from Plex so that Jellyfin matches your media 1:1, bypassing Jellyfin's fuzzy scrapers entirely.

## Prerequisites
* **Python 3** installed on your PC.
* **PowerShell** (Windows native).
* Your **Plex IP Address** (e.g., `http://192.168.1.50:32400`).
* Your **Plex Token** (Find this by clicking *Get Info* on any media item in Plex, then *View XML*. The token is at the very end of the URL).

---

## Steps

### 1. Setup Your Working Directory
Create a folder to house the tools (e.g., `C:\PlexToJellyfin`). 
Place the following three files into this directory:
1. `Run-PlexSync.ps1` (The main orchestrator script)
2. `PlexXMLPull.py` (The audit log generator)
3. `JellyfinNFOCreator.py` (The NFO writer)

### 2. Run the Orchestrator Script
Right-click `Run-PlexSync.ps1` and select **Run with PowerShell**. 
*(Note: If your system execution policy blocks the script, open PowerShell and run `powershell.exe -ExecutionPolicy Bypass -File .\Run-PlexSync.ps1`)*

The script will:
* Prompt you for your Plex IP and Token.
* Automatically connect to Plex and list your available libraries with their ID keys.
* Ask you which Library Key you want to export.
* Download the library data (`metadata.xml`), ensuring all hidden external GUIDs are included.
* Run the first Python script to generate an audit log.

### 3. Review the Audit Log
The PowerShell script will pause and ask you to review `audit_log.txt`. Open this text file and verify that:
* Your movies are listed correctly.
* The file paths match where your media is actually stored.
* The TMDb/IMDb/TVDb IDs have populated successfully. 

### 4. Generate the .NFO Files
If the audit log looks good, type `Y` in the PowerShell window to continue. 

The script will run `JellyfinNFOCreator.py`. This will read your `audit_log.txt` and generate a perfectly formatted `MOVIENAME.nfo` file directly next to every media file in your directories
