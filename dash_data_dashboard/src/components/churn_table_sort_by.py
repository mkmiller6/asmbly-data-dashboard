from dash_mantine_components import Select
from .ids import Ids


def render() -> Select:
    """Render the sort by dropdown"""

    return Select(
        id=Ids.CHURN_DATA_TABLE_SORT_BY,
        placeholder="Sort by",
        label="Sort by",
        value="Churn Risk",
        data=[
            {"value": "Churn Risk", "label": "Churn Risk"},
            {"value": "Name", "label": "Name"},
            {"value": "Email Address", "label": "Email Address"},
            {"value": "Emailed", "label": "Emailed"},
            {"value": "Neon ID", "label": "Neon ID"},
        ],
        style={
            "width": "200px",
        },
    )
