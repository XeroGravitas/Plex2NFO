# Plex XML To Jellyfin .NFO Files

### Disclaimer 

These scripts were developed strictly for personal use to solve a specific migration headache on my own home server. While they work perfectly for my setup, your environment, folder structures, or Plex agent history might behave differently.

Please use with care. Always run a test on a single file or small library first (as outlined in the steps below), and always ensure you have backups of your Jellyfin database and media directories before running automated scripts. Use at your own risk!

---

**Original Author:** [2dee11](https://github.com/2dee11)  
*Forked and updated to include exact ID matching (IMDb/TMDb/TVDb), streamlined PowerShell orchestration, and improved Collections parsing.*

> "I, probably like you reading this, wanted to convert my Plex library to Jellyfin without losing all of my years or hard work setting up Titles, Sort Titles, Original Titles, Added At Dates, Last Viewed At Dates, View Counts, and Collections.
> 
> This collection of scripts will help you do just that as easily as possible. Please note that I am by no means a developer, just an idiot on the internet with access to ChatGPT and a little know how. I tried to segment this as much as possible to try and prevent issues but use at your own risk." 
> — **2dee11**

It now pulls the exact provider IDs (TMDb, IMDb, TVDb) straight from Plex so that Jellyfin matches your media 1:1, bypassing Jellyfin's fuzzy scrapers entirely.

## Prerequisites
* **OS:** Windows (Native). *Note: This tool is designed and tested for Windows host environments; path translation for Linux/Docker container mounts is not handled automatically.*
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

The script will run `JellyfinNFOCreator.py`. This will read your `audit_log.txt` and generate a perfectly formatted `MOVIENAME.nfo` file directly next to every media file in your directories. 

> "Note: you may get a few 'Directory does not exist' errors for folder names with special characters like Alien3 or Joker: Folie à Deux. Check the output... I just fixed these manually myself within Jellyfin." — **2dee11**

### 5. Ingest into Jellyfin
Go to your Jellyfin WebUI:
1. Go to your Dashboard -> Libraries.
2. Click the three-dot menu on the updated library and select **Scan Library**.
3. Choose **Replace all metadata** and let it run. 

Jellyfin will read the `.nfo` files and your movies should be just as they were in Plex, locked to the exact database matches. 

> "After this initial bulk 'upload' I would suggest going into settings and selecting Manage Library for each Library and under Metadata Savers section check Nfo. Now scan library and replace all metadata... Now from this point on any changes you make Jellyfin will keep those new movie.nfo files updated." — **2dee11**

---

## Notes & Limitations

* **No TV Show Support:** Currently, this script only parses Movie libraries. It does not work for TV Shows.
* **Collections Cleanup:** The scripts correctly format the XML tags for Box Sets/Collections, but depending on your Jellyfin setup, you may still need the **TMDb Box Sets Plugin** installed to pull down the artwork and metadata for those collections.
* **Optional Scripts Removed:** Previous versions of this repo included standalone scripts just for exporting Collections. These have been archived/removed to streamline the main working branch.

## Potential Solutions for Docker Setups

The core script logic does not care about Docker. It simply reads XML from a Plex web endpoint, generates standard .nfo XML files, and writes them directly into your movie folders. Theoretically, as long as the file paths match from the POV of both server's target folders, it should work. Again, *theoretically.*

#### Option A: 
Find & Replace in `audit_log.txt`: The user opens `audit_log.txt` during the pause step and uses Notepad to Find & Replace `/data/movies` with `Z:\Media\Movies` before hitting Y in PowerShell.

#### Option B: 
(Run inside a container): Run the Python script directly inside the Docker container shell (where the paths native to Plex/Jellyfin actually exist).

Please feel free to fork a Docker-friendly version!

## Troubleshooting
> "I had some issues with accessing a network drive to store the files in. Running [net use] in CMD helped figure out which drives were accessible or not and troubleshooting accordingly... YMMV" — **2dee11**

(I also found running standard PowerShell without Administrator privileges mapped network drives best for the orchestrator script).

## Final Note
> "I do not plan on maintaining this and updating this with every change to Plex or Jellyfin, if someone else proposes changes I will try and add them." — **2dee11**

## Good luck!
