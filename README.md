# Plex XML To Jellyfin .NFO Files

### Disclaimer

These scripts were developed strictly for personal use to solve a specific migration headache on my own home server. While they work perfectly for my setup, your environment, folder structures, or Plex agent history might behave differently.

Please use with care. Always run a test on a single file or small library first (as outlined in the steps below), and always ensure you have backups of your Jellyfin database and media directories before running automated scripts. Use at your own risk!

---

**Original Author:** [2dee11](https://github.com/2dee11)  
_Forked and updated to include exact ID matching (IMDb/TMDb/TVDb), streamlined PowerShell orchestration, and improved Collections parsing._

> "I, probably like you reading this, wanted to convert my Plex library to Jellyfin without losing all of my years or hard work setting up Titles, Sort Titles, Original Titles, Added At Dates, Last Viewed At Dates, View Counts, and Collections.
>
> This collection of scripts will help you do just that as easily as possible. Please note that I am by no means a developer, just an idiot on the internet with access to ChatGPT and a little know how. I tried to segment this as much as possible to try and prevent issues but use at your own risk."
> — **2dee11**

It now pulls the exact provider IDs (TMDb, IMDb, TVDb) straight from Plex so that Jellyfin matches your media 1:1, bypassing Jellyfin's fuzzy scrapers entirely. It also robustly handles both modern and legacy Plex Metadata Agents (useful for those of us with a decade-old library), and parses non-English (UTF-8) character sets correctly.

## Prerequisites

- **OS:** Windows (Native). _Note: This tool is designed and tested for Windows host environments; path translation for Linux/Docker container mounts is not handled automatically._
- **Python 3** installed on your PC.
- **PowerShell** (Windows native).
- Your **Plex IP Address** (e.g., `http://192.168.1.50:32400`).
- Your **Plex Token** (Find this by clicking _Get Info_ on any media item in Plex, then _View XML_. The token is at the very end of the URL). More info: [Plex Support](https://support.plex.tv/articles/204059436-finding-an-authentication-token-x-plex-token/)

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
_(Note: If your system execution policy blocks the script, open PowerShell and run `powershell.exe -ExecutionPolicy Bypass -File .\Run-PlexSync.ps1`)_

The script will:

- Prompt you for your Plex IP and Token.
- Automatically connect to Plex and list your available libraries with their ID keys.
- Ask you which Library Key you want to export.
- Download the library data (`metadata.xml`), ensuring all hidden external GUIDs are included.
- Run the first Python script to generate an audit log.

### 3. Review the Audit Log

The PowerShell script will pause and ask you to review `audit_log.txt`. Open this text file and verify that:

- Your movies are listed correctly.
- The file paths match where your media is actually stored.
- The TMDb/IMDb/TVDb IDs have populated successfully.

It also outputs `audit_log.csv`, with a count of each Movie Title. This allows for easier manual de-duplication in Jellyfin. _Note:_ This counts Titles _only_, as different Metadata Agents can disagree on release year. I'd rather flag _potential_ duplicates than miss actual ones.

### 4. Generate the .NFO Files

If the audit log looks good, type `Y` in the PowerShell window to continue.

The script will run `JellyfinNFOCreator.py`. This will read your `audit_log.txt` and generate a perfectly formatted `MOVIENAME.nfo` file directly next to every media file in your directories, including titles with multiple parts or multiple version.

### 5. Ingest into Jellyfin

Go to your Jellyfin WebUI:

1. Go to your Dashboard -> Libraries.
2. Click the three-dot menu on the updated library and select **Scan Library**.
3. Choose **Replace all metadata** and let it run.

Jellyfin will read the `.nfo` files and your movies should be just as they were in Plex, locked to the exact database matches. This may take a while for large libraries, depending on storage speed etc.

### 6. Optional finishing touch

Once Jellyfin has finished updating the metadata, I recommend installing [Plexyfin](https://github.com/cleverdevil/plexyfin) as a Jellyfin plugin and running it with the `Force Replace All Artwork` flag. This will import all of your custom movie posters from Plex, completing your brand new mirrored library!

---

## Notes & Limitations

- **No TV Show Support:** Currently, this script only parses Movie libraries. It does not work for TV Shows.
- **No Automatic Duplicate Cleanup** Plex items with multiple versions (Theatrical and Director's Cuts etc.) will appear as separate items in Jellyfin and need to be merged manually (Select each version > Three dots menu > Group Versions). `audit_log.csv` is now included to help streamline this workflow.
- **Collections Cleanup:** The scripts correctly format the XML tags for Box Sets/Collections, but depending on your Jellyfin setup, you may still need the **TMDb Box Sets Plugin** installed to pull down the artwork and metadata for those collections.
- **Optional Scripts Removed:** Previous versions of this repo included standalone scripts just for exporting Collections. These have been archived/removed to streamline the main working branch.

## Potential Solutions for Docker Setups

The core script logic does not care about Docker. It simply reads XML from a Plex web endpoint, generates standard .nfo XML files, and writes them directly into your movie folders. Theoretically, as long as the file paths match from the POV of both server's target folders, it should work. Again, _theoretically._

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
