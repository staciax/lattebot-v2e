# Standard
import json

# data_store
def data_read(filename):
    with open("data_valorant/" + filename + ".json", "r", encoding='utf-8') as json_file:
        data = json.load(json_file)
    return data

def data_save(filename, data):
    with open("data_valorant/" + filename + ".json", 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=2, ensure_ascii=False)

def config_read():
    with open("data_valorant/config.json", "r", encoding='utf-8') as json_file:
        data = json.load(json_file)
    return data

def config_save(data):
    with open("data_valorant/config.json", 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=2, ensure_ascii=False)