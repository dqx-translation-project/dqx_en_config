import json
import sys

def read_json_file(file: str):
    with open(file, 'r', encoding='utf-8') as json_data:
        return json.loads(json_data.read())

def write_file(filename, data):
    '''Writes a string to a file.'''
    with open(f'{filename}', 'w+') as open_file:
        open_file.write(data)

def generate_hex(file: str):
    en_hex_to_write = ''
    blank_list = []
    data = read_json_file(file)
    for item in data:
        key, value = list(data[item].items())[0]
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

        if en_len > ja_len:
            print('\n')
            print('String too long. Please fix and try again.')
            print(f'File: {file}')
            print(f'JA string: {ja_raw} (byte length: {ja_len})')
            print(f'EN string: {en_raw} (byte length: {en_len})')
            sys.exit()

        ja = ja.replace('7c', '0a')
        en = en.replace('7c', '0a')
        if ja_len != en_len:
            while True:
                en += '00'
                new_len = len(en)
                if (ja_len - new_len) == 0:
                    break

        en_hex_to_write += en

    if blank_list:
        print(f'Found untranslated strings in {file}. Here are the keys:')
        for item in blank_list:
            print('>> ' + item)

    filename = file.replace('.json', '')
    write_file(f'{filename}.hex', en_hex_to_write)

if __name__ == "__main__":
    files = [
        'controls_new.json',
        'settings_new.json'
    ]
    
    for file in files:
        generate_hex(file)
