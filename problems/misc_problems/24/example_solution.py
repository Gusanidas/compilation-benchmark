from collections import Counter
import sys

def freq_sort(arr):
    # Count frequencies and sort by (-frequency, value)
    counts = Counter(arr)
    return sorted(arr, key=lambda x: (-counts[x], x))

for line in sys.stdin:
    line = line.strip()
    if line:
        arr = list(map(int, line.split()))
        sorted_arr = freq_sort(arr)
        # print to stdout
        print(" ".join(map(str, sorted_arr)))