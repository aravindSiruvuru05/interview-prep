
import heapq
from collections import defaultdict

def weighted_vote_winner(votes):
    vote_count = defaultdict(int)
    last_seen = {}  # track the last vote index for each candidate

    for i, candidate in enumerate(votes):
        vote_count[candidate] += 1
        last_seen[candidate] = i

    heap = []
    for candidate, count in vote_count.items():
        # Max heap: sort by votes DESC, then latest index DESC
        heapq.heappush(heap, (-count, -last_seen[candidate], candidate))

    # Top of heap is winner
    _, _, winner = heapq.heappop(heap)
    return winner

# Example usage
votes = ["c1", "c2", "c1", "c2", "c1", "c2", "c3", "c4", "c4"]
print(weighted_vote_winner(votes))  # Output depends on vote order