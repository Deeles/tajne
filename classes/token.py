from datetime import datetime
from datetime import timedelta
from typing import Dict, List, Tuple

import utils
from classes.transaction import Transaction


def add_money(money: Dict[str, float], token_name: str, value: float):
    if token_name in money:
        money[token_name] += value
    else:
        money[token_name] = value


class Token:

    def __init__(self, dictionary: Dict):
        self.name = dictionary['name']
        self.date_added = datetime.strptime(dictionary['dateAdded'], "%Y-%m-%dT%H:%M:%S.%fZ")
        self.pair = dictionary['pair']
        self.liquidity_transaction_data = dictionary['history'][0]['data']

        self.transactions = []

        for small_dictionary in dictionary['history']:
            self.transactions.append(Transaction(small_dictionary,
                                                 is_to=small_dictionary['to'].lower() == self.pair.lower()))

    def listed_with_liquidity(self, loaded_function_dict: Dict[str, str]) -> Dict[str, float]:
        money = {}

        for transaction in self.transactions:
            if utils.is_add_liquidity_function_hex(transaction.data, loaded_function_dict):
                add_money(money, transaction.token_name, transaction.value)

        return money

    def get_hourly_volume(self) -> Dict:
        money = {}

        first_transaction_time = self.transactions[2].date_time
        for transaction in self.transactions[2:]:
            if transaction.is_before(first_transaction_time + timedelta(hours=24)):
                add_money(money, transaction.token_name, transaction.value)

        return money

    def get_hour_mooooooooney(self, loaded_function_dict: Dict[str, str]) -> List[Tuple[datetime, Dict[str, float]]]:
        hour_mooooooooney = []
        start_time = self.transactions[0].date_time
        end_time = self.transactions[-1].date_time
        diff = end_time - start_time
        days, seconds = diff.days, diff.seconds
        hours = days * 24 + seconds // 3600
        for hour in range(hours + 1):
            time_from = start_time + timedelta(hours=hour)
            time_to = start_time + timedelta(hours=hour + 1)
            trans = self.get_transactions_between(time_from, time_to)
            trans = [tran for tran in trans if utils.is_buy_function_hex(tran.data, loaded_function_dict) or\
                     utils.is_sell_function_hex(tran.data, loaded_function_dict)]
            hour_mooooooooney.append((time_from, self.get_money_from_transactions(trans)))

        return hour_mooooooooney

    def get_transactions_between(self, from_date, to_date) -> List[Transaction]:
        transactions_between = []

        for transaction in self.transactions:
            if transaction.is_before(to_date) and transaction.is_after(from_date):
                transactions_between.append(transaction)

        return transactions_between

    def get_money_from_transactions(self, transactions: List[Transaction]):
        money = {}

        for transaction in transactions:
            add_money(money, transaction.token_name, transaction.value)

        return money
