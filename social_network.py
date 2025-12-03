from collections import deque, defaultdict

class SocialNetwork:
    def __init__(self):
        self.network = defaultdict(set)

    def load_network(self, filename):
        try:
            with open(filename, 'r') as file:
                for line in file:
                    parts = line.strip().split(':')
                    if len(parts) < 2:
                        continue
                        
                    user = parts[0].strip()
                    friends = parts[1].strip().split()
                    
                    if user not in self.network:
                        self.network[user] = set()
                        
                    for friend in friends:
                        self.network[user].add(friend)
                        self.network[friend].add(user)
            return True
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
            return False

    def get_suggestions(self, user):
        """Finds friend suggestions based on mutual friends."""
        if user not in self.network:
            return None

        direct_friends = self.network[user]
        mutual_counts = defaultdict(int)
        mutual_friends_map = defaultdict(list) 

        for friend in direct_friends:
            for potential_suggestion in self.network[friend]:
                if potential_suggestion != user and potential_suggestion not in direct_friends:
                    mutual_counts[potential_suggestion] += 1
                    mutual_friends_map[potential_suggestion].append(friend)

        sorted_suggestions = sorted(mutual_counts.items(), key=lambda item: item[1], reverse=True)
        
        result = []
        for sugg_user, count in sorted_suggestions:
            mutuals_names = ", ".join(sorted(mutual_friends_map[sugg_user]))
            result.append(f"{sugg_user} ({count} mutual friends: {mutuals_names})")
            
        return result

    def get_shortest_path(self, start, end):
        """BFS to find the shortest path between two users."""
        if start not in self.network or end not in self.network:
            return None

        queue = deque([(start, [start])])
        visited = set([start])

        while queue:
            current_user, path = queue.popleft()
            
            if current_user == end:
                return path

            for neighbor in self.network[current_user]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
        
        return None # No path found

if __name__ == "__main__":
    sn = SocialNetwork()
    
    if sn.load_network("network.txt"):
        print("\n=== Social Network Analysis ===")
        print(f"Total users: {len(sn.network)}")
        total_connections = sum(len(friends) for friends in sn.network.values()) // 2
        print(f"Total friendships: {total_connections}")
        
        all_users = list(sn.network.keys())
        print(f"Sample users: {', '.join(all_users[:5])} ...")

        while True:
            print("\n------------------------------")
            print("Please select an option:")
            print("1) Get Friend Suggestions")
            print("2) Find Shortest Connection Path")
            print("3) Exit")
            
            choice = input("Enter choice (1-3): ").strip()
            
            if choice == '1':
                target_user = input("Enter User Name: ").strip().title()
                suggestions = sn.get_suggestions(target_user)
                
                if suggestions is None:
                    print(f"User '{target_user}' not found in the network.")
                elif not suggestions:
                    print(f"No suggestions found for {target_user} (no friends of friends).")
                else:
                    print(f"\nFriend suggestions for {target_user}:")
                    for s in suggestions:
                        print(f" - {s}")

            elif choice == '2':
                start_node = input("Enter Start User: ").strip().title()
                end_node = input("Enter End User: ").strip().title()
                
                path = sn.get_shortest_path(start_node, end_node)
                
                if path is None:
                    if start_node not in sn.network or end_node not in sn.network:
                        print("Error: One or both users not found.")
                    else:
                        print(f"No connection exists between {start_node} and {end_node}.")
                else:
                    print(f"\nConnection found!")
                    print(f"Shortest path: {' -> '.join(path)}")
                    print(f"Degrees of separation: {len(path) - 1}")

            elif choice == '3':
                print("Exiting program. Goodbye!")
                break
            
            else:
                print("Invalid selection. Please enter 1, 2, or 3.")