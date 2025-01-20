class SocialNetwork:
    def __init__(self):
        self.users = {}
        self.friendships = {}

    def add_user(self, username, name, age):
        if username in self.users:
            return False
        self.users[username] = {"name": name, "age": age}
        self.friendships[username] = set()
        return True

    def remove_user(self, username):
        if username not in self.users:
            return False
        del self.users[username]
        for friend in self.friendships[username]:
            self.friendships[friend].remove(username)
        del self.friendships[username]
        return True

    def add_friendship(self, username1, username2):
        if username1 not in self.users or username2 not in self.users:
            return False
        if username1 == username2 or username2 in self.friendships[username1]:
            return False
        self.friendships[username1].add(username2)
        self.friendships[username2].add(username1)
        return True

    def remove_friendship(self, username1, username2):
        if username1 not in self.users or username2 not in self.users:
            return False
        if username2 not in self.friendships[username1]:
            return False
        self.friendships[username1].remove(username2)
        self.friendships[username2].remove(username1)
        return True

    def get_friends(self, username):
        if username not in self.users:
            return "false"
        friends = sorted(self.friendships[username])
        return ",".join(friends) if friends else ""


def main():
    network = SocialNetwork()

    while True:
        try:
            command = input()
            if not command:
                break

            parts = command.split()
            action = parts[0]

            if action == "AddUser":
                username, name, age = parts[1], " ".join(parts[2:-1]).strip('"'), int(parts[-1])
                print(network.add_user(username, name, age))

            elif action == "RemoveUser":
                username = parts[1]
                print(network.remove_user(username))

            elif action == "AddFriendship":
                username1, username2 = parts[1], parts[2]
                print(network.add_friendship(username1, username2))

            elif action == "RemoveFriendship":
                username1, username2 = parts[1], parts[2]
                print(network.remove_friendship(username1, username2))

            elif action == "GetFriends":
                username = parts[1]
                print(network.get_friends(username))

        except EOFError:
            break

if __name__ == "__main__":
    main()