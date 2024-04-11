import pandas as pd

default_params = pd.DataFrame(
    {
        "neon_id": [None],
        "email": [None],
        "first_name": [None],
        "last_name": [None],
        "has_op_id": [False],
        "has_discourse_id": [False],
        "time_from_asmbly": [None],
        "age": [None],
        "gender": [None],
        "referral_source": [None],
        "family_membership": [False],
        "membership_cancelled": [False],
        "annual_membership": [False],
        "waiver_signed": [False],
        "orientation_attended": [False],
        "taken_MSS": [False],
        "taken_WSS": [False],
        "taken_cnc_class": [False],
        "taken_lasers_class": [False],
        "taken_3dp_class": [False],
        "teacher": [False],
        "steward": [False],
        "num_classes_before_joining": [None],
        "num_classes_attended": [None],
        "total_dollars_spent": [None],
        "duration": [None],
    }
)
