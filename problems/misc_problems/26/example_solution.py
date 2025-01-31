import sys

def find_second_largest(arr):
    # Remove duplicates and sort in descending order
    unique_sorted = sorted(set(arr), reverse=True)
    # Return second element (index 1) if we have at least 2 unique numbers
    if len(unique_sorted) >= 2:
        return unique_sorted[1]
    return None

# Read input from stdin
for line in sys.stdin:
    line = line.strip()
    if line:
        # Convert input string to integer array
        arr = list(map(int, line.split()))
        # Find and print second largest
        result = find_second_largest(arr)
        if result is not None:
            print(result)