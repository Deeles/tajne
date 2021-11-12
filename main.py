import os
import json
from typing import Dict

import utils
from classes.token import Token


def run():
    loaded_function_dict = utils.get_loaded_function_dict(r'functions.json')
    directory = r'token_history/'

    tokens = []
    for filename in os.listdir(directory):
        file_name = os.path.join(directory, filename)
        dictionary = load_json(file_name)
        token = Token(dictionary)
        tokens.append(token)
        print(token.listed_with_liquidity(loaded_function_dict))
        hour_moooooooney, price, liqui = token.get_hour_mooooooooney(loaded_function_dict)
        utils.plot(token.name, hour_moooooooney, price, liqui, 'Wrapped BNB', token.date_added)


def load_json(file_name: str) -> Dict:
    with open(file_name) as reader:
        return json.load(reader)


if __name__ == '__main__':
    run()
