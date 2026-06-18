class LRUCache:
    """Least-recently-used cache with a fixed capacity.

    LRUCache(capacity): create a cache holding at most `capacity` items.
    get(key) -> int: return the value for key, or -1 if absent. Accessing a key
        (get or put) marks it most-recently-used.
    put(key, value) -> None: insert/update. If over capacity, evict the
        least-recently-used item first.
    """

    def __init__(self, capacity):
        raise NotImplementedError

    def get(self, key):
        raise NotImplementedError

    def put(self, key, value):
        raise NotImplementedError
