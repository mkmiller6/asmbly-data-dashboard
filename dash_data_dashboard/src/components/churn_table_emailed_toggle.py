from dash_mantine_components import Switch
from .ids import Ids


def render() -> Switch:
    """Render the emailed toggle"""

    return Switch(
        id=Ids.CHURN_DATA_TABLE_FILTER,
        label="Show already emailed",
        color="indigo",
        checked=True,
    )
