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


def aggregation(adapter):
    """
    Count users grouped by user_type.

    Returns one row per user_type value.
    """
    return adapter.aggregation()


def mixed_read_write(adapter):
    """Create or update, read, and remove a temporary user."""
    return adapter.mixed_read_write()


def concurrency(adapter, user_id=30, concurrent_requests=5):
    """Run simultaneous point lookups against one adapter connection."""
    from concurrent.futures import ThreadPoolExecutor

    with ThreadPoolExecutor(max_workers=concurrent_requests) as executor:
        futures = [
            executor.submit(adapter.point_lookup, user_id)
            for _ in range(concurrent_requests)
        ]
        return [future.result() for future in futures]