
# Problem Statement:
# You're getting different types of exceptions in a system.

# For each exception type, you need to:

# Monitor the frequency of occurrences.

# Trigger an alert if the number of occurrences exceeds a threshold inside a rolling time window (e.g., 30 mins, 60 mins).

# 🔵 Inputs example:
# ExceptionA: > 5 occurrences in last 30 minutes.

# ExceptionB: > 10 occurrences in last 1 hour.




# first solution comes to mind is sliding withdow of storing timestamps and on every exception remove timestampls from dqeue 
# Sliding Window per exception type

# Store a list or deque of timestamps for each exception type.

# Automatically discard timestamps that are older than the time window.

from collections import defaultdict, deque
import time

class ExceptionMonitor:
    def __init__(self, thresholds):
        self.thresholds = thresholds
        self.exception_logs = defaultdict(deque)  # exception_type -> deque of timestamps

    def log_exception(self, exception_type):
        current_time = time.time()
        limit = self.thresholds[exception_type]['limit']
        window = self.thresholds[exception_type]['window']

        q = self.exception_logs[exception_type]
        q.append(current_time)

        # Evict old timestamps outside the rolling window
        while q and q[0] < current_time - window:
            q.popleft()

        # Check if threshold exceeded
        if len(q) > limit:
            self.send_alert(exception_type, len(q))

    def send_alert(self, exception_type, count):
        print(f"[ALERT] {exception_type} occurred {count} times in the rolling window!")

# Example usage:
thresholds = {
    "ExceptionA": {"limit": 5, "window": 30 * 60},   # 5 times in 30 mins
    "ExceptionB": {"limit": 10, "window": 60 * 60},  # 10 times in 1 hour
}

monitor = ExceptionMonitor(thresholds)

# Simulate logging
monitor.log_exception("ExceptionA")
monitor.log_exception("ExceptionA")
# ... repeat




# While deque operations like append() and popleft() are amortized O(1) in Python, some interviewers get picky about it because:

# Technically, a deque still needs to allocate new memory occasionally.

# In extreme scale scenarios, they might prefer a solution where no linear cleanup happens at all (even rare popleft() scans across stale timestamps might worry them).

# ⚠️ What could your interviewer be hinting at?
# They might want a pure constant time approach like:

# ✅ Alternative 1: Time-bucket based (Fixed-size buckets)
# Instead of keeping all timestamps, you can use time bucketing (rolling histogram):

# ⏳ Rolling Counter Approach (O(1) amortized without a deque):
# Idea:
# Divide time into fixed buckets (e.g., 1-minute slots).

# Keep a counter for each bucket for the past N minutes.

# Rotate/reset buckets as time progresses.




# Fixed-size buckets + circular buffer logic to track counts per time slice and roll them forward efficiently in a sliding window.
# You need to track exception frequencies inside a rolling time window and raise an alert if the count exceeds a configured threshold.

# Divide the rolling window (e.g., 30 mins) into fixed-size buckets (e.g., 1-minute buckets → 30 buckets total).

# Use a circular buffer to re-use the buckets over time by mapping:

# bucket_index = (current_time_in_minutes) % total_buckets
# For each incoming exception:

# Map it to the correct bucket based on time.

# If the bucket is "stale" (older than the window), reset it to zero.

# Increment the current bucket count.

# To check for alerts:

# Sum all buckets that are still inside the valid rolling window.

# If the total exceeds the threshold, trigger the alert.

# Key advantage:

# All operations (reset, increment, map, sum) are O(1) or bounded by the fixed number of buckets (e.g., 30).

# This avoids dynamic structures like deque, making the system scalable and constant-time under heavy load.



import time

class RollingWindowAlert:
    def __init__(self, thresholds, granularity=60):
        self.thresholds = thresholds
        self.granularity = granularity  # bucket size in seconds

        self.buckets = {}               # exception_type -> list of counts
        self.timestamps = {}            # exception_type -> list of last updated times
        # It is the full timestamp, not just the seconds part of the clock.
        # You can get an integer version by doing int(time.time()), e.g. 1709372251


        self.rolling_total = {}         # exception_type -> running total of non-stale buckets

        for ex_type, conf in thresholds.items():
            num_buckets = conf['window'] // granularity + 1
            self.buckets[ex_type] = [0] * num_buckets
            self.timestamps[ex_type] = [0] * num_buckets
            self.rolling_total[ex_type] = 0

    def log_exception(self, exception_type):
        now = int(time.time())
        config = self.thresholds[exception_type]
        window = config['window']
        num_buckets = len(self.buckets[exception_type])

        bucket_idx = (now // self.granularity) % num_buckets
        bucket_time = self.timestamps[exception_type][bucket_idx]

        # Reset stale bucket if needed
        if now - bucket_time >= window:
            # Subtract stale value from rolling total
            old_value = self.buckets[exception_type][bucket_idx]
            self.rolling_total[exception_type] -= old_value

            # Reset bucket
            self.buckets[exception_type][bucket_idx] = 0
            self.timestamps[exception_type][bucket_idx] = now

        # Add new event
        self.buckets[exception_type][bucket_idx] += 1
        self.rolling_total[exception_type] += 1

        # Check threshold
        if self.rolling_total[exception_type] > config['limit']:
            self.send_alert(exception_type, self.rolling_total[exception_type])

    def send_alert(self, exception_type, count):
        print(f"[ALERT] {exception_type} occurred {count} times within the window!")

