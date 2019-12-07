from background_task import background

from loans.operations import update_loans


@background(schedule=20)
def start_loan_update_task() -> None:
    update_loans()
