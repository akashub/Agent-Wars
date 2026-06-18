import pytest
from solution import LRUCache


def test_basic_put_and_get():
    cache = LRUCache(2)
    cache.put(1, 10)
    assert cache.get(1) == 10


def test_get_missing_returns_minus_one():
    cache = LRUCache(2)
    assert cache.get(99) == -1


def test_overwrite_updates_value_without_growing():
    cache = LRUCache(2)
    cache.put(1, 10)
    cache.put(1, 20)
    assert cache.get(1) == 20
    # capacity 2; only one distinct key inserted — no eviction should have happened
    cache.put(2, 30)
    assert cache.get(2) == 30
    assert cache.get(1) == 20


def test_evicts_lru_when_over_capacity():
    cache = LRUCache(2)
    cache.put(1, 1)
    cache.put(2, 2)
    cache.put(3, 3)  # evicts key 1 (LRU)
    assert cache.get(1) == -1
    assert cache.get(2) == 2
    assert cache.get(3) == 3


def test_get_refreshes_recency():
    cache = LRUCache(2)
    cache.put(1, 1)
    cache.put(2, 2)
    cache.get(1)     # 1 is now MRU; 2 is LRU
    cache.put(3, 3)  # should evict 2, not 1
    assert cache.get(2) == -1
    assert cache.get(1) == 1
    assert cache.get(3) == 3


def test_put_existing_key_refreshes_recency():
    cache = LRUCache(2)
    cache.put(1, 1)
    cache.put(2, 2)
    cache.put(1, 10)  # update 1; now 2 is LRU
    cache.put(3, 3)   # should evict 2
    assert cache.get(2) == -1
    assert cache.get(1) == 10
    assert cache.get(3) == 3


def test_capacity_one():
    cache = LRUCache(1)
    cache.put(1, 1)
    assert cache.get(1) == 1
    cache.put(2, 2)   # evicts 1
    assert cache.get(1) == -1
    assert cache.get(2) == 2


def test_classic_sequence():
    # LeetCode #146 canonical example (capacity 2)
    cache = LRUCache(2)
    cache.put(1, 1)
    cache.put(2, 2)
    assert cache.get(1) == 1     # returns 1
    cache.put(3, 3)              # evicts key 2
    assert cache.get(2) == -1   # not found
    cache.put(4, 4)              # evicts key 1
    assert cache.get(1) == -1   # not found
    assert cache.get(3) == 3    # returns 3
    assert cache.get(4) == 4    # returns 4
