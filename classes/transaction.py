from datetime import datetime
from typing import Dict


class Transaction:

    def __init__(self, dictionary: Dict, is_to: bool):
        self.date_time = datetime.fromtimestamp(int(dictionary['timeStamp']))
        self.value = int(dictionary['value']) / (10 ** int(dictionary['tokenDecimal']))
        self.token_name = dictionary['tokenName']
        self.is_to = is_to
        self.data = dictionary['data'] if 'data' in dictionary else 'NO_DATA'
        self.hash = dictionary['hash']

    def is_before(self, date_time: datetime) -> bool:
        return self.date_time <= date_time

    def is_after(self, date_time: datetime) -> bool:
        return self.date_time > date_time
