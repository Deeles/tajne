import json
from typing import Dict

import utils
from classes.token import Token


def run():
    loaded_function_dict = utils.get_loaded_function_dict(r'token_history/functions.json')

    # iterable = range(14100, 14101)
    iterable = [14092, 14093, 14100]

    tokens = []
    for i in iterable:
        try:
            dictionary = load_json(i)
            token = Token(dictionary)
            tokens.append(token)
            print(token.listed_with_liquidity(loaded_function_dict))
            hour_moooooooney = token.get_hour_mooooooooney(loaded_function_dict)
            utils.plot(hour_moooooooney, 'Wrapped BNB', token.date_added)
        except Exception as e:
            print(e)


def load_json(number: int) -> Dict:
    file = f'token_history/{number}.json'
    with open(file) as reader:
        return json.load(reader)


if __name__ == '__main__':
    run()
