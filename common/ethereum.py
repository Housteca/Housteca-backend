import json

from django.conf import settings
from web3.auto import Web3
from web3.contract import Contract

ETHEREUM_ADDRESS_REGEX = r'^0x[a-fA-F0-9]{40}$'

w3 = Web3()


def _load_contract(path: str) -> Contract:
    with open(path) as file:
        contract_dict = json.load(file)
        return w3.eth.contract(
            abi=contract_dict['abi'],
            address=contract_dict['networks'][settings.NETWORK_ID]['address']
        )


HOUSTECA = _load_contract(settings.HOUSTECA_ABI_FILE_PATH)
