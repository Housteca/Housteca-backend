import json
from typing import Optional

from django.conf import settings
from web3.auto import Web3
from web3.contract import Contract

from common.account import Account

ETHEREUM_ADDRESS_REGEX = r'^0x[a-fA-F0-9]{40}$'

w3 = Web3()


def _load_ethereum_account() -> Account:
    with open(settings.PRIVATE_KEY_PATH) as keyfile:
        private_key = w3.eth.account.decrypt(keyfile.read(), settings.PRIVATE_KEY_PASSWORD)
        acc = w3.eth.account.from_key(private_key)
        return Account(address=acc.address, private_key=private_key)


ACCOUNT = _load_ethereum_account()


def _load_contract(path: str, contract_address: Optional[str] = None) -> Contract:
    with open(path) as file:
        contract_dict = json.load(file)
        address = contract_address or contract_dict['networks'][settings.NETWORK_ID]['address']
        return w3.eth.contract(
            abi=contract_dict['abi'],
            address=address,
        )


HOUSTECA = _load_contract(settings.HOUSTECA_ABI_FILE_PATH)


def get_loan_contract_at(address :str) -> Contract:
    return _load_contract(settings.LOAN_ABI_FILE_PATH, address)