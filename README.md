## Sync this project with Slider
- Clone this project to `git clone <repo URL> <root>/Localizations/简体中文`
- Clone Slider and open in Unity. In build, select `<root>` as reference translation, and "generate outside project" to somewhere that is not exactly `<root>`
  > Slider will wipe the destination folder, which will nuke the cloned repo, so don't use `<root>` directly!!!
- Copy the generated CSV's to this repo after deleting the original ones
- Check Git diffs to make sure the changes make sense

## Update this project
- Clone this project to `git clone <repo URL> <root>/Localizations/简体中文`
- Run `python -m venv .venv` and activate the virtual environment
  - Linux: `source .venv/bin/activate`
  - Windows Git Bash: `source .venv/Scripts/activate`
- Run `python -m pip install --upgrade pip` and then `pip install -r requirements.txt`
- Run `python sanity.py combine` after syncing (see prev section) to create the Excel sheet
- Update the Excel sheet, then export changes back to Slider (see next section)

## Sync Slider with this project
- Clone this project to `git clone <repo URL> <root>/Localizations/简体中文`
- Run `python -m venv .venv` and activate the virtual environment
  - Linux: `source .venv/bin/activate`
  - Windows Git Bash: `source .venv/Scripts/activate`
- Run `python -m pip install --upgrade pip` and then `pip install -r requirements.txt`
- Run `python sanity.py split` to update pending changes in the Excel sheet to each CSV file (skip if no pending changes)
- Clone Slider and open in Unity. In build, select `<root>` as reference translation, and "generate inside project"