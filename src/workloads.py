"""
Standardized benchmark workloads.

Each workload receives a database adapter and executes
the same logical operation against the database.
"""


def point_lookup(adapter, user_id=30):
    """
    Look up a single user by user_id.

    Returns the database result.
    """
    return adapter.point_lookup(user_id)