import queue
from threading import Thread
from .cache_utils import cache, get_cached_response, print_cache_stats, clear_cache
from .rate_limiter import TokenBucket

def input_with_timeout(prompt, timeout):
    q = queue.Queue()
    def get_input():
        try:
            q.put(input(prompt))
        except Exception:
            q.put(None)
    t = Thread(target=get_input)
    t.daemon = True
    t.start()
    try:
        return q.get(timeout=timeout)
    except queue.Empty:
        return None

def run_chatbot(chain, bucket):
    print("🤖 Gemini Chatbot with Memory, Rate Limiting, and Caching (type 'exit' or 'quit' to quit)")
    while True:
        cache_size = len(cache)
        print(f"[Cache: {cache_size}/50] You: ", end="", flush=True)
        user_input = input_with_timeout("", 300)
        if user_input is None:
            print("\n[Timeout] No input for 5 minutes. Exiting chat.")
            break
        user_input = user_input.strip()
        cmd = user_input.lower()
        if cmd in ('exit', 'quit'):
            print("🤖 Goodbye!")
            break
        if cmd == 'cache':
            print_cache_stats()
            continue
        if cmd == 'clear':
            clear_cache()
            continue
        if cmd == 'demo':
            demo_prompt = "What is Python?"
            print(f"[Cache: {len(cache)}/50] You: {demo_prompt}")
            response, cached, elapsed = get_cached_response(demo_prompt, chain)
            if cached:
                print(f"\u26A1 [CACHED in {elapsed:.1f}ms] ")
            else:
                print(f"\U0001F501 [FRESH in {elapsed:.1f}ms] ")
            print(f"\U0001F916 AI: {response}")
            print(f"[Cache: {len(cache)}/50] You: {demo_prompt}")
            response, cached, elapsed = get_cached_response(demo_prompt, chain)
            if cached:
                print(f"\u26A1 [CACHED in {elapsed:.1f}ms] ")
            else:
                print(f"\U0001F501 [FRESH in {elapsed:.1f}ms] ")
            print(f"\U0001F916 AI: {response}")
            print_cache_stats()
            continue
        if not bucket.consume():
            print("[429] Rate limit exceeded. Please wait.")
            continue
        response, cached, elapsed = get_cached_response(user_input, chain)
        if cached:
            print(f"\u26A1 [CACHED in {elapsed:.1f}ms] ")
        else:
            print(f"\U0001F501 [FRESH in {elapsed:.1f}ms] ")
        print(f"\U0001F916 AI: {response}")
