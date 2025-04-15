# ⏱️ Time Complexity Comparison of Common Python Containers

| Operation                     | `set`        | `dict`       | `SortedSet`         | `SortedDict`         | `SortedList`        | `list`         |
|------------------------------|--------------|--------------|---------------------|----------------------|---------------------|----------------|
| `add()` / `insert()`         | O(1)*        | O(1)*        | O(log n)            | O(log n)             | O(log n)            | O(n)           |
| `remove()` / `discard()`     | O(1)*        | O(1)*        | O(log n)            | O(log n)             | O(log n)            | O(n)           |
| `in` / `__contains__()`      | O(1)*        | O(1)*        | O(log n)            | O(log n)             | O(log n)            | O(n)           |
| `get()` / `__getitem__()`    | ❌           | O(1)*        | O(log n) (by index) | O(log n)             | O(log n)            | O(1)           |
| `set()` / `__setitem__()`    | ❌           | O(1)*        | ❌                  | O(log n)             | ❌                  | O(1) (index)   |
| Sorted iteration             | ❌           | ❌           | O(n)                | O(n)                 | O(n)                | ❌ (unsorted)  |
| Index access (`[i]`)         | ❌           | ❌           | O(log n)            | ❌                   | O(log n)            | O(1)           |
| `len()`                      | O(1)         | O(1)         | O(1)                | O(1)                 | O(1)                | O(1)           |
| Insert at arbitrary index    | ❌           | ❌           | ❌                  | ❌                   | O(n)                | O(n)           |
| Maintain order               | ❌ (random)  | ✅ (3.7+)    | ✅ (sorted)         | ✅ (sorted by key)   | ✅ (sorted)         | ✅ (insertion) |

> **Note**: `O(1)*` indicates **average-case**; worst case can be O(n) due to hash collisions or resizing.
> 
> `SortedSet`, `SortedDict`, and `SortedList` are from the [`sortedcontainers`](https://github.com/grantjenks/python-sortedcontainers) library.

