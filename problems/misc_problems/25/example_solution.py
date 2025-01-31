import sys

for line in sys.stdin:
    line = line.strip()
    if line:
        arr = list(map(int, line.split()))
        max_num = max(arr)
        # print to stdout
        print(max_num)