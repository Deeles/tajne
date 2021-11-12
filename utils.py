import json
from datetime import datetime
from typing import Dict, Union, List, Tuple

import matplotlib.pyplot as plt


def is_add_liquidity_function_hex(hex_code: str, loaded_function_dict: Dict[str, str]) -> bool:
    add_liquidity_substrings = ["finalize", "addliquidity"]
    function_name = get_function_name(hex_code, loaded_function_dict)
    if function_name is None:
        return False
    return any([True for substring in add_liquidity_substrings if substring in function_name])


def is_remove_liquidity_function_hex(hex_code: str, loaded_function_dict: Dict[str, str]) -> bool:
    remove_liquidity_substrings = ["remove"]
    function_name = get_function_name(hex_code, loaded_function_dict)
    if function_name is None:
        return False
    return any([True for substring in remove_liquidity_substrings if substring in function_name])


def is_buy_function_hex(hex_code: str, loaded_function_dict: Dict[str, str]) -> bool:
    buy_substring = ["swapexacteth", "swapeth"]
    function_name = get_function_name(hex_code, loaded_function_dict)
    if function_name is None:
        return False
    return any([True for substring in buy_substring if substring in function_name])


def is_sell_function_hex(hex_code: str, loaded_function_dict: Dict[str, str]) -> bool:
    sell_substring = ["swapexacttokens"]
    function_name = get_function_name(hex_code, loaded_function_dict)
    if function_name is None:
        return False
    return any([True for substring in sell_substring if substring in function_name])


def get_function_name(hex_code: str, loaded_function_dict: Dict[str, str]) -> Union[str, None]:
    trimmed_hex_code = hex_code[:10]
    if trimmed_hex_code in loaded_function_dict:
        return loaded_function_dict[trimmed_hex_code]
    return None


def get_loaded_function_dict(file: str) -> Dict[str, str]:
    loaded_function_dict = {}

    with open(file) as reader:
        data = json.load(reader)
        for key, value in data.items():
            loaded_function_dict[key] = value.lower()

    return loaded_function_dict


def plot(token_name, hour_mooooooney: List[Tuple[datetime, Dict[str, float]]],
         price, liqui, money_name: str, date_added: datetime):
    plot_price = normalize(price)
    plot_money = []
    index_money = []

    for i, tuple_ in enumerate(hour_mooooooney):
        date_time, hour_money = tuple_
        money = 0
        if money_name in hour_money:
            money = hour_money[money_name]

        index_money.append(date_time)
        plot_money.append(money)

    plt.plot(index_money, plot_money)
    plt.plot(index_money, plot_price, color='green')
    plt.plot(index_money, liqui, color='cyan')
    plt.axvline(date_added, color='red')
    plt.xlabel(token_name)
    plt.tight_layout()
    plt.tick_params(axis='x', labelsize=5)
    plt.show()


def normalize(price: List[float]) -> List[float]:
    multiply_by = 100 / price[-1]

    price_new = [price[0] * multiply_by]
    last_price = price[0] * multiply_by
    for part_price in price[1:]:
        if part_price == 0:
            price_new.append(last_price)
            continue
        last_price = part_price * multiply_by
        price_new.append(last_price)

    return price_new