import sys
from collections import defaultdict, deque

class SoldierManager:
    def __init__(self):
        self.soldiers = {}  # Dictionary to store ID -> rank mapping

    def add_soldier(self, soldier_id, rank):
        if soldier_id in self.soldiers or soldier_id != len(self.soldiers) + 1:
            return False
        self.soldiers[soldier_id] = rank
        return True

    def find_ranks(self, ranks):
        rank_set = set(ranks)
        current_window = defaultdict(int)
        left = 1
        min_length = float('inf')
        result = (-1, -1)

        for right in range(1, len(self.soldiers) + 1):
            rank = self.soldiers[right]
            if rank in rank_set:
                current_window[rank] += 1

            while len(current_window) == len(rank_set):
                if right - left + 1 < min_length:
                    min_length = right - left + 1
                    result = (left, right)

                left_rank = self.soldiers[left]
                if left_rank in current_window:
                    current_window[left_rank] -= 1
                    if current_window[left_rank] == 0:
                        del current_window[left_rank]
                left += 1

        return result

def process_input():
    manager = SoldierManager()

    for line in sys.stdin:
        line = line.strip()
        if line.startswith("AddSoldier: "):
            _, args = line.split(": ", 1)
            soldier_id, rank = args.split(", ")
            soldier_id = int(soldier_id)
            print(manager.add_soldier(soldier_id, rank))

        elif line.startswith("FindRanks: "):
            _, args = line.split(": ", 1)
            ranks = args.split(", ")
            start, end = manager.find_ranks(ranks)
            if start == -1:
                print("False")
            else:
                print(f"{start},{end}")

if __name__ == "__main__":
    process_input()
