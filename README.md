# dqx_en_config

Scripts to convert `DQXConfig.exe` into English.

# Background

The string tables are ETP files, which are the same type of files seen for DQX's game text. Although you can dump the ETP files directly from `DQXConfig.exe`, they are also packed with the game's dat files. This repo uses the files in the game's dats, instead of the executable, as we mass upload these into our translation platform, Weblate. This script will pull the translated ETPs from Weblate and import them into `DQXConfig.exe`, giving you a ready-to-use executable.

# How to use

- Place an updated `DQXConfig.exe` into the `app/configs` directory
- Run `pip install -r requirements.txt` to install necessary modules (in a venv if you prefer)
- `cd` into the `app` directory
- Run `python main.py` to read in the ETPs from the dqx_translations repository and write them into the executable
- Run `.\port_assets.bat` to move the images into the executable
- Finished executable is in the app folder and ready to be used

# How to install

- Back up `C:\Program Files (x86)\SquareEnix\DRAGON QUEST X\Game\DQXConfig.exe` (rename it to `DQXConfig.orig.exe` or something)
- Paste the patched config exe (see releases on the right) into this directory
- Have fun

**I do not own or work for DQX and am purely doing this to be able to understand the client in my native language (English)**

**Images in `imgs` directory are owned by Square Enix and edited by Lightpost on the Dragon's Den forums.**

https://www.woodus.com/forums/topic/36234-dragon-quest-x-online-config-translated-executable/
