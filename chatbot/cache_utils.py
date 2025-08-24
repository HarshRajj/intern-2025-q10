from cachetools import TTLCache
from threading import Lock

# --- LRU Cache with TTL and Stats ---
cache = TTLCache(maxsize=50, ttl=300)  # 50 entries, 5 minutes TTL
cache_lock = Lock()
cache_stats = {
    'hits': 0,
    'misses': 0,
    'time_saved': 0.0,  # seconds
    'hit_times': [],    # ms per hit
    'miss_times': []    # ms per miss
}

def get_cached_response(prompt, chain):
    import time
    start = time.perf_counter()
    with cache_lock:
        if prompt in cache:
            cache_stats['hits'] += 1
            elapsed = (time.perf_counter() - start) * 1000
            cache_stats['hit_times'].append(elapsed)
            return cache[prompt], True, elapsed
    # Not in cache, call LLM
    miss_start = time.perf_counter()
    response = chain.invoke(input={"input": prompt})["response"]
    miss_elapsed = (time.perf_counter() - miss_start) * 1000
    with cache_lock:
        cache[prompt] = response
        cache_stats['misses'] += 1
        cache_stats['miss_times'].append(miss_elapsed)
    return response, False, miss_elapsed

def print_cache_stats():
    hits = cache_stats['hits']
    misses = cache_stats['misses']
    total = hits + misses
    hit_rate = (hits / total * 100) if total else 0.0
    size = len(cache)
    maxsize = cache.maxsize
    time_saved = sum(cache_stats['hit_times']) / 1000  # seconds
    avg_time_saved = (sum(cache_stats['hit_times']) / hits) if hits else 0.0
    print("\U0001F4CA Cache Statistics:")
    print(f"  • Cache hits: {hits}")
    print(f"  • Cache misses: {misses}")
    print(f"  • Hit rate: {hit_rate:.1f}%")
    print(f"  • Cache size: {size}/{maxsize}")
    print(f"  • Time saved: {time_saved:.1f}s total")
    print(f"  • Avg time saved per hit: {avg_time_saved:.1f}ms")

def clear_cache():
    with cache_lock:
        cache.clear()
    print("\U0001F5D1️ Cache cleared.")
