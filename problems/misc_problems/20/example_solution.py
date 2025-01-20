from collections import defaultdict, deque
from typing import Dict, Set, List, Union

class SocialNetwork:
    def __init__(self):
        self.users: Dict[str, dict] = {}  # username -> user info
        self.friends: Dict[str, Set[str]] = defaultdict(set)  # username -> set of friends
    
    def add_user(self, username: str, name: str, age: int) -> bool:
        """Add a new user to the network."""
        if username in self.users:
            return False
        
        self.users[username] = {
            'name': name,
            'age': age
        }
        return True
    
    def remove_user(self, username: str) -> bool:
        """Remove a user from the network."""
        if username not in self.users:
            return False
        
        # Remove user's friendships
        for friend in self.friends[username]:
            self.friends[friend].remove(username)
        
        # Remove user
        del self.users[username]
        del self.friends[username]
        return True
    
    def add_friendship(self, username1: str, username2: str) -> bool:
        """Add a friendship between two users."""
        if (username1 not in self.users or 
            username2 not in self.users or 
            username1 == username2):
            return False
        
        if username2 in self.friends[username1]:
            return False
        
        self.friends[username1].add(username2)
        self.friends[username2].add(username1)
        return True
    
    def remove_friendship(self, username1: str, username2: str) -> bool:
        """Remove a friendship between two users."""
        if (username1 not in self.users or 
            username2 not in self.users or 
            username2 not in self.friends[username1]):
            return False
        
        self.friends[username1].remove(username2)
        self.friends[username2].remove(username1)
        return True
    
    def get_friends(self, username: str) -> Union[str, bool]:
        """Get sorted list of friends for a user."""
        if username not in self.users:
            return False
        
        return ','.join(sorted(self.friends[username]))
    
    def degree_of_separation(self, username1: str, username2: str) -> int:
        """Calculate minimum number of connections between two users."""
        if username1 not in self.users or username2 not in self.users:
            return -1
        
        if username1 == username2:
            return 0
        
        # BFS to find shortest path
        visited = {username1}
        queue = deque([(username1, 0)])
        
        while queue:
            current_user, distance = queue.popleft()
            
            for friend in self.friends[current_user]:
                if friend == username2:
                    return distance + 1
                if friend not in visited:
                    visited.add(friend)
                    queue.append((friend, distance + 1))
        
        return -1

def process_command(network: SocialNetwork, command: str) -> Union[bool, str, int]:
    """Process a single command and return the result."""
    parts = command.strip().split(' ', 1)
    operation = parts[0]
    
    if operation == 'AddUser':
        # Extract username and full name (in quotes) and age
        remaining = parts[1].split('"')
        username = remaining[0].strip()
        name = remaining[1].strip()
        age = int(remaining[2].strip())
        return network.add_user(username, name, age)
    
    elif operation == 'RemoveUser':
        username = parts[1].strip()
        return network.remove_user(username)
    
    elif operation == 'AddFriendship':
        username1, username2 = parts[1].strip().split()
        return network.add_friendship(username1, username2)
    
    elif operation == 'RemoveFriendship':
        username1, username2 = parts[1].strip().split()
        return network.remove_friendship(username1, username2)
    
    elif operation == 'GetFriends':
        username = parts[1].strip()
        return network.get_friends(username)
    
    elif operation == 'DegreeOfSeparation':
        username1, username2 = parts[1].strip().split()
        return network.degree_of_separation(username1, username2)
    
    raise ValueError(f"Unknown command: {operation}")

def main():
    network = SocialNetwork()
    
    try:
        while True:
            command = input()
            if not command:
                break
            result = process_command(network, command)
            print(result)
    except EOFError:
        pass

if __name__ == "__main__":
    main()