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


def hop_1(adapter, user_id=30):
    """
    Traverse exactly 1 hop from a starting user.

    Returns the users directly connected to the starting user.
    """
    return adapter.hop_1(user_id)


def hop_2(adapter, user_id=30):
    """
    Traverse exactly 2 hops from a starting user.

    Returns users reachable within 2 hops.
    """
    return adapter.hop_2(user_id)


def hop_3(adapter, user_id=30):
    """
    Traverse exactly 3 hops from a starting user.

    Returns users reachable within 3 hops.
    """
    return adapter.hop_3(user_id)

def indexed_lookup(adapter, user_type=0): 
    """ 
    Look up users using an indexed user_type property. 
    Returns all users matching the specified user_type. 
    """ 
    return adapter.indexed_lookup(user_type)