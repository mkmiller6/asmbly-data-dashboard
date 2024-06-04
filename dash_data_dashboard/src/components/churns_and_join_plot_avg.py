from dash_mantine_components import Select
from .ids import Ids


def render() -> Select:
    """Render the sort by dropdown"""

    return Select(
        id=Ids.CHURNS_AND_JOINS_PLOT_AVG,
        label="Averaging",
        value="14 Days",
        data=[
            {"value": "None", "label": "None"},
            {"value": "7 Days", "label": "7 Days"},
            {"value": "14 Days", "label": "14 Days"},
            {"value": "30 Days", "label": "30 Days"},
            {"value": "90 Days", "label": "90 Days"},
        ],
        style={
            "width": "200px",
        },
    )
