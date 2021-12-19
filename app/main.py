import json

def read_file(file: str):
    with open(file, 'r') as hex_data:
        return hex_data.read()

def format_to_json(json_data, data, number):
    json_data[number]={}
    json_data[number][data]=''
    
    return json_data

def write_file(filename, data):
    with open(f'{filename}', 'w+', encoding='utf-8') as open_file:
        open_file.write(data)

def convert_hex_to_json(file: str):
    hex_data = read_file(file)
    hex_data = hex_data.replace('0A', '7C')
    hex_data = hex_data.replace('00', '0A')
    hex_data = hex_data.replace(' ', '')
    hex_data = bytearray.fromhex(hex_data)
    game_data = hex_data.decode('utf-8')

    jsondata_ja = {}
    jsondata_en = {}
    number = 1

    for line in game_data.split('\n'):
        json_data_en = format_to_json(jsondata_en, line, number)
        number += 1

    json_data = json.dumps(
        jsondata_en,
        indent=2,
        sort_keys=False,
        ensure_ascii=False
    )

    return json_data

if __name__ == "__main__":
    files = [
        'controls_orig.hex',
        'settings_orig.hex'
    ]
    
    for file in files:
        data = convert_hex_to_json(file)
        filename = file.replace('.hex', '')
        write_file(f'{filename}.json', data)
