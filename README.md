# dqx_en_config

Python scripts that generate hex to paste into a hex editor for a translated English DQX settings client.

**I do not own or work for DQX and am purely doing this to be able to understand the client in my native language (English)**

**Images in `imgs` directory are owned by Square Enix and edited by Lightpost on the Dragon's Den forums.**

https://www.woodus.com/forums/topic/36234-dragon-quest-x-online-config-translated-executable/

# How to use

- Open `DQXConfig.exe` with a hex editor like wxMEdit (something that supports utf-8)
- Search for `45 56 54 58 10`. This indicates the start of text
- Copy from the first byte that has string data all the way to the last string right before "FOOT"
- Paste the bytes into `app/<file>_orig.hex` (one for controls and one for settings)
- Run `main.py` to generate easily-read json files for both of these hex dumps
- Port over (with `hyde_json_merge`) or translate the json files
  - If using `hyde_json_merge`:
    - You need to put the `orig` file in the `src` dir and remove `_orig`
    - You need to put the `new` file in the `dst` dir and remove `_new`
    - Rename both files to add `_new` in the `out` dir and put them in `app`
- Run `parse.py` to generate `app/<file>_new.hex` (one for controls and one for settings)
- Copy the hex in each file and paste directly over the bytes in your hex editor
- Save the executable
- If desired, open your edited `DQXConfig.exe` with `ResourceHacker` and replace with assets in `imgs`

# How to install

- Back up `C:\Program Files (x86)\SquareEnix\DRAGON QUEST X\Game\DQXConfig.exe` (rename it to `DQXConfig.orig.exe` or something)
- Paste the patched config exe (see releases on the right) into this directory
- Have fun
