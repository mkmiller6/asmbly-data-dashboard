from dash_mantine_components import Select
from .ids import Ids


def render() -> Select:
    """Render the sort direction dropdown"""

    return Select(
        id=Ids.CHURN_DATA_TABLE_SORT_DIR,
        placeholder="Sort direction",
        label="Sort direction",
        value="desc",
        data=[
            {"value": "asc", "label": "Asc"},
            {"value": "desc", "label": "Desc"},
        ],
        style={
            "width": "200px",
        },
    )
