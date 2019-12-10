from common.ethereum import HOUSTECA
from properties.models import Property


def check_new_properties() -> None:
    properties = Property.objects.filter(contract_address__isnull=True)
    if len(properties) > 0:
        entries = HOUSTECA.events.InvestmentCreated.getLogs(fromBlock=0)
        for prop in properties:
            candidates = list(filter(lambda e: e.args.borrower == prop.user.address, entries))
            if candidates:
                candidate = candidates[-1]
                prop.contract_address = candidate.args.contract_address
                prop.save()
