import time

class RateLimiter:
    def __init__(self, window, limit, max_credits=None):
        self.limit = limit  # requests per window
        self.window = window  # window size in seconds
        self.max_credits = max_credits if max_credits is not None else limit

        self.last_reset_time = time.time()
        self.available_tokens = limit

    def check_rate_limit(self):
        current_time = time.time()
        elapsed = current_time - self.last_reset_time

        if elapsed >= self.window:
            windows_passed = int(elapsed // self.window)  # we calculate howmany windows passes till now and refill those credits , if we use currtime
            refill = windows_passed * self.limit
            self.available_tokens = min(self.available_tokens + refill, self.max_credits)
            self.last_reset_time += windows_passed * self.window

        if self.available_tokens <= 0:
            return False

        self.available_tokens -= 1
        return True
    

rl = RateLimiter(window=2, limit=5, max_credits=10)

for _ in range(7):
    print(rl.check_rate_limit())  # Should allow 5 requests, then deny 2

time.sleep(2)
print("\n--- After 2 sec ---\n")

for _ in range(6):
    print(rl.check_rate_limit())  # Should refill 5, allow 5, then deny 1
