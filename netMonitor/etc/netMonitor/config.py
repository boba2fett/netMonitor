import os
import json

if os.getenv('tg-env')=="dev":
            with open('config.dev.json', 'r') as json_file:
                CONFIG = json.load(json_file)
else:
    with open('config.json', 'r') as json_file:
        CONFIG = json.load(json_file)