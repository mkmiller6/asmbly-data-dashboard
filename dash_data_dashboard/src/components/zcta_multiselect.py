from dash_mantine_components import MultiSelect
from .ids import Ids


def render() -> MultiSelect:
    """Render the multi-select for the zcta map."""

    return MultiSelect(
        id=Ids.ZCTA_MULTISELECT,
        label="Member Status",
        value=["active"],
        searchable=True,
        data=[
            {"value": "active", "label": "Active"},
            {"value": "inactive", "label": "Inactive"},
            # {"value": "never_joined", "label": "Never Joined"},
        ],
        style={
            "width": "400px",
        },
    )
