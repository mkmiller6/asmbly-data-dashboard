"""HTML element IDs for Dash components"""

from enum import StrEnum


class Ids(StrEnum):
    """HTML element IDs for Dash components"""

    CHURN_DATA_TABLE = "churn-data-table"
    CHURN_DATA_TABLE_CONTAINER = "churn-data-table-container"
    CHURN_DATA_TABLE_SEARCH = "churn-data-table-search"
    CHURN_DATA_TABLE_SORT_BY = "churn-data-table-sort-by"
    CHURN_DATA_TABLE_SORT_DIR = "churn-data-table-sort-dir"
    CHURN_DATA_TABLE_FILTER = "churn-data-table-filter"
    CHURN_DATA_TABLE_SUBMIT = "churn-data-table-submit"

    ACTIVE_MEMBERS_CARD = "active-members-card"

    ACTIVE_MEMBERS_PLOT = "active-members-plot"
    ACTIVE_MEMBERS_PLOT_DATE_RANGE = "active-members-plot-date-range"
