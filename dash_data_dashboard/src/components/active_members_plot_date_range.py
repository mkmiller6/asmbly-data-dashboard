import datetime
from dash_mantine_components import DateRangePicker
from .ids import Ids


def render() -> DateRangePicker:
    """Render the sort by dropdown"""

    return DateRangePicker(
        id=Ids.ACTIVE_MEMBERS_PLOT_DATE_RANGE,
        label="Date Range",
        value=[
            datetime.date(2022, 7, 11),
            datetime.date.today() - datetime.timedelta(days=1),
        ],
        minDate=datetime.date(2022, 7, 11),
        maxDate=datetime.date.today() - datetime.timedelta(days=1),
        amountOfMonths=2,
        clearable=False,
        style={
            "width": "200px",
        },
    )
