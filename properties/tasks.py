from background_task import background

from properties.operations import check_new_properties


@background(schedule=10)
def check_new_investments_task() -> None:
    check_new_properties()
