from dash_mantine_components import TextInput
from .ids import Ids


def render() -> TextInput:
    """Render the search bar"""

    return TextInput(
        id=Ids.CHURN_DATA_TABLE_SEARCH,
        placeholder="Name, Email, or Neon ID",
        label="Search",
        style={
            "width": "200px",
        },
    )
