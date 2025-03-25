def pascal_triangle(n):
    triangle = []
    for row_num in range(n):
        row = [1]  # First element is always 1
        if triangle:
            last_row = triangle[-1]
            row += [last_row[i] + last_row[i + 1] for i in range(len(last_row) - 1)]
            row.append(1)  # Last element is always 1
        triangle.append(row)
    return triangle

# Print Pascal's Triangle
n = 5  # You can change this value
triangle = pascal_triangle(n)
for row in triangle:
    print(row)
