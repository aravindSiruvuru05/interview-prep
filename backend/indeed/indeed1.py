# 1 - 2 | 2 - 1 | 3 - 4 | 4 - 2 | 5 - 2 | 6 - 1 | 7 - 1 | 8 -2 |
# 9 - 2 | 10 - 1 | 11 - 1 | 12 -1

# heap ==    (2, 4) (4, 3)
# [3, 4, 5]
# [1, 3, 4, 5, 7, 8]
# [1, 2, 3, 5, 9, 10]
# [3, 6, 8, 9, 11, 12k]
import heapq

def solve(k):


#   3
#  3
# 1, 1
    #  itterate -> counter 
    # 1 2 -> 12k
    pointers = [0] * 4
    counter = {
        1 : 2,
        2: 1,
        3: 4,
        4: 2,
        5: 2,
        6: 1,
        7: 1,
        8: 2,
        9: 2,
        10: 1,
        11: 1,
        12: 1
    }
    hq = []
    keys = [key for key in counter]

    for _ in range(k):
        curr = keys.pop()
        heapq.heappush(hq, (counter[curr], -curr))

    while keys:
        curr = keys.pop()
        freq, ele = hq[0]
        if freq <= counter[curr]:
            heapq.heappushpop(hq, (counter[curr], -curr))
    
    res = []

    for el in hq:
        freq, key = el
        res.append(-1*key)
    res.reverse()
    print(res)


solve(2)







# n = 3       m = 6     [4,3,2,2,2,6]