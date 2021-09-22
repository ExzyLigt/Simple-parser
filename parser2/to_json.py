import datetime

import ujson


def to_json(txt_file: str) -> None:
    
    json_filename = str(datetime.datetime.now()) + '.json'
    
    with open(txt_file, 'r') as txt_f, open(json_filename, 'w') as json_f:
        x = [dict(sku=articul.rstrip(" \n")) for articul in txt_f]
        j = {"Аркуш1": x}
        
        ujson.dump(j, json_f, indent=4, ensure_ascii=False)
        

if __name__ == "__main__":
    to_json("articuls.txt", "data.json")