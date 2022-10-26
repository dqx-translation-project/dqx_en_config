import json
from struct import unpack
import requests
from shutil import copy


orig_dqx_config = "configs/DQXConfig.exe"

FILE_LIST = {
    b"\x49\x4E\x44\x58\x10\x00\x00\x00\x60\x13\x00\x00\x00\x00\x00\x00\xB7\x37\x01\x00\x00\x00\x00": "game_settings.json",
    b"\x49\x4E\x44\x58\x10\x00\x00\x00\xD0\x01\x00\x00\x00\x00\x00\x00\x90\x2F\x01\x00\x00\x00\x00": "controls.json",
}


def generate_hex(json_data: str):
    en_hex_to_write = ''
    blank_list = []
    for item in json_data:
        key, value = list(json_data[item].items())[0]
        ja = key.encode('utf-8').hex() + '00'
        ja_raw = key
        ja_len = len(ja)

        if value:
            en = value.encode('utf-8').hex() + '00'
            en_raw = value
            en_len = len(en)
        else:
            en = ja
            en_len = ja_len
            blank_list.append(ja_raw)

        ja = ja.replace('7c', '0a')
        en = en.replace('7c', '0a')
        if ja_len != en_len:
            while True:
                en += '00'
                new_len = len(en)
                if (ja_len - new_len) == 0:
                    break

        en_hex_to_write += en
    
    return en_hex_to_write


def migrate_translations(untranslated_file: str, translated_file: str):
    with open(f"{untranslated_file}", "r", encoding="utf-8") as untranslated, open(translated_file, "r", encoding="utf-8") as translated:
        unt_data = json.loads(untranslated.read())
        tra_data = json.loads(translated.read())

    count = 0
    entry = 1
    for tra_item in tra_data:
        key, value = list(tra_data[tra_item].items())[0]
        for unt_item in list(unt_data.values())[count]:
            if key == unt_item:
                unt_data[str(entry)].update({key: value})
            count += 1
            entry += 1

    with open(f"{translated_file}.new", "w+", encoding="utf-8") as f:
        f.write(json.dumps(unt_data, indent=2, ensure_ascii=False))


def import_etps():
    copy(orig_dqx_config, "./DQXConfig.exe")

    r1 = requests.get("https://raw.githubusercontent.com/dqx-translation-project/dqx_translations/main/json/_lang/en/adhoc_game_settings.json")
    r2 = requests.get("https://raw.githubusercontent.com/dqx-translation-project/dqx_translations/main/json/_lang/en/adhoc_controller_buttons_2.json")

    game_settings = generate_hex(json.loads(r1.text))
    controls = generate_hex(json.loads(r2.text))

    with open("./DQXConfig.exe", "r+b") as f:
        data = f.read()

        matches = []
        pos = 0
        while True:
            match = data.find(b"\x45\x56\x54\x58\x10\x00\x00", pos)  # EVTX
            if match != -1:  # find returns -1 on no match
                matches.append(match)
                pos = match + 1
            else:
                break

        for match in matches:
            indx_start = f.seek(match + 80)  # jump straight to INDX
            filename = FILE_LIST[f.read(23)]
            f.seek(-23, 1)
            f.seek(8, 1)  # jump to size of INDX
            indx_size = unpack("<I", f.read(4))[0]
            # 16 to get passed INDX header, another 16 to get passed FOOT and last 8 to get to size of text
            f.seek(indx_start + 16 + 16 + indx_size + 8)
            text_size = unpack("<I", f.read(4))[0]
            f.seek(4, 1) # jump to start of strings

            if filename == "game_settings.json":
                f.write(bytes.fromhex(game_settings))
            if filename == "controls.json":
                f.write(bytes.fromhex(controls))


if __name__ == "__main__":
    import_etps()
