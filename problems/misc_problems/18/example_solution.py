class MilitaryHierarchy:
    def __init__(self):
        # Dictionary to store soldier information: {id: (rank, superior_id)}
        self.soldiers = {}
        
    def add_soldier(self, soldier_id, rank, superior_id):
        """
        Add a soldier to the hierarchy.
        Returns True if successful, False otherwise.
        """
        # Validate inputs
        if not isinstance(soldier_id, int) or not isinstance(rank, int) or not isinstance(superior_id, int):
            return False
            
        if soldier_id < 1 or rank < 1 or rank > 10 or superior_id < 0:
            return False
            
        # Check if soldier ID already exists
        if soldier_id in self.soldiers:
            return False
            
        # Add the soldier
        self.soldiers[soldier_id] = (rank, superior_id)
        return True
        
    def get_superior_chain(self, soldier_id):
        """
        Get the chain of superiors for a given soldier.
        Returns a list of (id, rank) tuples or None if invalid.
        """
        if soldier_id not in self.soldiers:
            return None
            
        chain = []
        current_id = soldier_id
        
        # Prevent infinite loops
        visited = set()
        
        while current_id != 0:  # 0 represents no superior
            if current_id in visited:
                return None  # Circular reference detected
            visited.add(current_id)
            
            if current_id not in self.soldiers:
                return None
                
            rank, superior_id = self.soldiers[current_id]
            chain.append((current_id, rank))
            current_id = superior_id
            
        return chain
        
    def find_common_superior(self, first_id, second_id):
        """
        Find the lowest-ranking common superior between two soldiers.
        Returns the ID of the common superior or False if none exists.
        """
        # Check if both soldiers exist
        if first_id not in self.soldiers or second_id not in self.soldiers:
            return False
            
        # Get superior chains for both soldiers
        first_chain = self.get_superior_chain(first_id)
        second_chain = self.get_superior_chain(second_id)
        
        if first_chain is None or second_chain is None:
            return False
            
        # Convert chains to sets of IDs for easier comparison
        first_ids = {id for id, _ in first_chain}
        second_ids = {id for id, _ in second_chain}
        
        # Find common superiors
        common_superiors = first_ids.intersection(second_ids)
        
        if not common_superiors:
            return False
            
        # Find the common superior with the lowest rank
        lowest_rank = float('inf')
        lowest_rank_id = None
        
        for sup_id in common_superiors:
            rank = self.soldiers[sup_id][0]
            if rank < lowest_rank:
                lowest_rank = rank
                lowest_rank_id = sup_id
                
        return lowest_rank_id

def process_input():
    hierarchy = MilitaryHierarchy()
    
    try:
        while True:
            line = input().strip()
            if not line:
                break
                
            if line.startswith("AddSoldier:"):
                # Parse AddSoldier command
                params = line[11:].strip().split(",")
                if len(params) != 3:
                    print(False)
                    continue
                    
                try:
                    soldier_id = int(params[0])
                    rank = int(params[1])
                    superior_id = int(params[2])
                    result = hierarchy.add_soldier(soldier_id, rank, superior_id)
                    print(result)
                except ValueError:
                    print(False)
                    
            elif line.startswith("FindCommonSuperior:"):
                # Parse FindCommonSuperior command
                parms = line.split(": ", 1)
                params =  parms[1].strip().split(",") 
                if len(params) != 2:
                    print(False)
                    continue
                    
                try:
                    first_id = int(params[0])
                    second_id = int(params[1])
                    result = hierarchy.find_common_superior(first_id, second_id)
                    print(result)
                except ValueError:
                    print(False)
            else:
                print(False)
    except EOFError:
        pass

if __name__ == "__main__":
    process_input()