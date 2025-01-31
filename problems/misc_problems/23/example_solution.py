import sys

def find_peaks(arr):
    n = len(arr)
    if n == 1: return arr
    return [arr[i] for i in range(n) if 
            (i == 0 and arr[i] > arr[i+1]) or
            (i == n-1 and arr[i] > arr[i-1]) or
            (0 < i < n-1 and arr[i] > arr[i-1] and arr[i] > arr[i+1])]

for line in sys.stdin:
    line = line.strip()
    if line:
        arr = list(map(int, line.split()))
        peaks = find_peaks(arr)
        # print to stdout
        print(" ".join(map(str, peaks)))