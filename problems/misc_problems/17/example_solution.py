class MilitaryHierarchy:
    def __init__(self):
        self.soldiers = {}

    def add_soldier(self, ID, Rank, SuperiorID):
        if ID in self.soldiers or ID <= 0 or Rank <= 0 or Rank > 10:
            return False

        if SuperiorID != 0 and SuperiorID not in self.soldiers:
            return False

        self.soldiers[ID] = {
            'Rank': Rank,
            'SuperiorID': SuperiorID,
        }
        return True

    def find_common_superior(self, FirstID, SecondID):
        if FirstID not in self.soldiers or SecondID not in self.soldiers:
            return False

        # Trace the hierarchy upwards for both soldiers
        first_ancestors = self._get_ancestors(FirstID)
        second_ancestors = self._get_ancestors(SecondID)

        # Find the lowest-ranking common superior
        common_superiors = set(first_ancestors.keys()) & set(second_ancestors.keys())
        if not common_superiors:
            return False

        # Choose the one with the lowest rank, breaking ties with the smallest ID
        best_common = min(
            common_superiors,
            key=lambda id_: (self.soldiers[id_]['Rank'], id_)
        )

        return best_common

    def _get_ancestors(self, soldier_id):
        """Returns a dictionary of ancestors {ID: Rank} for the given soldier."""
        ancestors = {}
        current_id = soldier_id
        while current_id != 0:
            ancestors[current_id] = self.soldiers[current_id]['Rank']
            current_id = self.soldiers[current_id]['SuperiorID']
        return ancestors


def process_input():
    hierarchy = MilitaryHierarchy()

    import sys
    input = sys.stdin.read
    lines = input().strip().split('\n')
    output = []

    for line in lines:
        if line.startswith("AddSoldier"):
            _, args = line.split(":")
            ID, Rank, SuperiorID = map(int, args.split(","))
            result = hierarchy.add_soldier(ID, Rank, SuperiorID)
            output.append("True" if result else "False")

        elif line.startswith("FindCommonSuperior"):
            _, args = line.split(":")
            FirstID, SecondID = map(int, args.split(","))
            result = hierarchy.find_common_superior(FirstID, SecondID)
            output.append(str(result) if result else "False")

    print("\n".join(output))

if __name__ == "__main__":
    process_input()