from common.ethereum import HOUSTECA


def is_investor(address: str) -> bool:
    return HOUSTECA.functions.isInvestor(address).call()


def is_admin(address: str) -> bool:
    return HOUSTECA.functions.isAdmin(address).call()


def is_local_node(address: str) -> bool:
    return HOUSTECA.functions.isLocalNode(address).call()
