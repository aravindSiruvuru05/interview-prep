def sort(left, right):
    res = []
    i, j = 0, 0
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            res.append(left[i])
            i += 1
        else:
            res.append(right[j])
            j += 1
    res.extend(left[i:])
    res.extend(right[j:])
    
    return res

def mergesort(arr):
    if len(arr) == 1:
        return arr

    mid = len(arr) // 2

    left = mergesort(arr[:mid])
    right = mergesort(arr[mid:])

    return sort(left, right)

a = mergesort([9,2,4,6,7,4,1])
print(a)