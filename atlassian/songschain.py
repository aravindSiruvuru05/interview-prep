# Our local radio station is running a show where the songs are ordered in a very specific way. 
# The last word of the title of one song must match the first word of the title of the next song - 
# for example, "Silent Running" could be followed by "Running to Stand Still". No song may be played more than once.
#  Given a list of songs and a starting song, find the longest chain of songs that begins with that song, 
# and the last word of each song title matches the first word of the next one. 
# Write a function that returns the longest such chain.
from collections import deque

def get_first_word(title):
    return title.split()[0]

def get_last_word(title):
    return title.split()[-1]

def build_graph(songs):
    graph = {song: [] for song in songs}
    for a in songs:
        for b in songs:
            if a != b and get_last_word(a) == get_first_word(b):
                graph[a].append(b)
    return graph

def longest_song_chain_bfs(songs, start_song):
    graph = build_graph(songs)
    
    queue = deque()
    queue.append( ([start_song], set([start_song])) )  # (path, visited set)

    longest_path = []

    while queue:
        path, visited = queue.popleft()
        current_song = path[-1]

        if len(path) > len(longest_path):
            longest_path = path

        for neighbor in graph[current_song]:
            if neighbor not in visited:
                new_path = path + [neighbor]
                new_visited = visited | {neighbor}
                queue.append((new_path, new_visited))

    return longest_path
songs = [
    "Silent Running",
    "Running to Stand Still",
    "Still of the Night",
    "Night Moves",
    "Moves Like Jagger",
    "Jagger Bomb"
]

start = "Silent Running"
chain = longest_song_chain_bfs(songs, start)
print("Longest song chain:", chain)



def get_first_word(title):
    return title.split()[0]

def get_last_word(title):
    return title.split()[-1]

def build_graph(songs):
    graph = {song: [] for song in songs}
    for a in songs:
        a_last = get_last_word(a)
        for b in songs:
            if a != b and get_first_word(b) == a_last:
                graph[a].append(b)
    return graph

def longest_chain_util(graph, current, visited):
    visited.add(current)
    max_chain = [current]  # Initialize with just the current song

    for neighbor in graph[current]:
        if neighbor not in visited:
            # Use a copy of visited to preserve unique path per call
            chain = longest_chain_util(graph, neighbor, visited.copy())
            if len(chain) + 1 > len(max_chain):
                max_chain = [current] + chain

    return max_chain

def longest_song_chain(songs, start_song):
    graph = build_graph(songs)
    return longest_chain_util(graph, start_song, set())
longest_chain = longest_song_chain(songs, songs[0])

print("Longest song chain:")
print(" → ".join(longest_chain))