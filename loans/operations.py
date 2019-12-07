import logging

from common.ethereum import HOUSTECA, get_loan_contract_at, ACCOUNT, w3


logger = logging.getLogger(__name__)


def update_loans() -> None:
    loans = HOUSTECA.functions.loans().call()
    for contract_address in loans:
        contract = get_loan_contract_at(contract_address)
        should_update = contract.functions.shouldUpdate().call()
        if should_update is True:
            trx_data = contract.functions.update().buildTransaction({
                'from': ACCOUNT.address,
            })
            signed_trx_data = w3.eth.account.sign_transaction(trx_data, private_key=ACCOUNT.private_key)
            transaction = w3.eth.sendRawTransaction(signed_trx_data.rawTransaction)
            trx_hash = transaction.hex()
            logger.info('Loan at %s updated. Transaction hash: %s', contract_address, trx_hash)
