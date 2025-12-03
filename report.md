
# Social Network Analysis Assignment
**Student Name:** Alaeddine Sahih
**Date:** December 3, 2025
**Course:** Data Structures and Algorithms

---

## 1. Capture (Problem Definition)
The objective of this assignment was to develop a Python-based application to analyze a social network stored in a text file (`network.txt`). The system parses a dataset of users and their direct mutual friendships to construct a graph representation of the network. The core functional requirements were to generate friend suggestions for a specific user—ranked by the number of mutual friends—and to calculate the shortest connection path (degrees of separation) between any two users in the network.

## 2. Contemplate (Design Choices)
To solve this problem efficiently and address the performance analysis requirements, I made the following design decisions:

* **Data Representation: Adjacency List**
    I chose to represent the social network using an **Adjacency List**, implemented as a Python Dictionary of Sets (`{ 'User': {'Friend1', 'Friend2'} }`).
    * *Justification:* Social networks are inherently "sparse" graphs, meaning most users are only connected to a small fraction of the total population. An Adjacency Matrix would require $O(V^2)$ space, mostly filled with zeros (wasted memory). The Adjacency List is space-efficient, using $O(V + E)$ space. Furthermore, I used Python `sets` for the value storage because they allow for $O(1)$ average time complexity when checking if a specific friendship exists.

* **Search Algorithm: Breadth-First Search (BFS)**
    I implemented **Breadth-First Search (BFS)** to find the connection path between users.
    * *Justification:* Since the social network is an unweighted graph (where every friendship represents an equal "distance" of 1), BFS is the optimal algorithm. It explores the graph layer-by-layer, guaranteeing that the first time the target user is reached, it is via the shortest possible path.

## 3. Contract (Interface Design)
The application is organized into a `SocialNetwork` class with the following interface:

* `load_network(filename) -> bool`: Reads the input file, parses the `User: Friend` format, and populates the graph structure. It ensures all relationships are bidirectional (mutual).
* `get_suggestions(user) -> list`: Returns a list of potential friends for a target user. It filters out existing friends and the user themselves, ranking the results by the count of mutual connections.
* `get_shortest_path(start, end) -> list`: Returns the sequence of users representing the shortest path between a `start` and `end` node using BFS.

## 4. Compose (Algorithm Logic)
* **Parsing:** The file reader uses the `collections.defaultdict` structure to simplify graph creation. It splits each line by the colon delimiter and iterates through the friend list. Crucially, it enforces reciprocity: if "Alice: Bob" is encountered, the system updates both Alice's list to include Bob and Bob's list to include Alice.
* **Friend Suggestions:** To find suggestions for User A, the algorithm iterates through User A's direct friends. It then inspects the friends of those friends (neighbors of neighbors). If a person is found who is not User A and not already a direct friend, they are added to a candidate map. This map tracks the "mutual count," and the final list is sorted in descending order of this count.
* **Pathfinding (BFS):** The algorithm utilizes a `collections.deque` for efficient queue operations ($O(1)$ pops). It starts at the source user, exploring all immediate neighbors before moving to neighbors-of-neighbors, tracking the path taken until the target is found.


## 5. Chart (Visualization & Logic Flow)
To visualize the system's architecture without external images, I have mapped out the data structure in memory and the control flow for the two primary algorithms.

---

### A. Data Structure Visualization
```text
The network is stored as an **Adjacency List** using a Dictionary of Sets. This maps every user (key) to their set of immediate connections (value).


[ Graph Storage in Memory ]
---------------------------
"Alice"   --> { "Bob", "David" }
"Bob"     --> { "Alice", "Charlie", "Emma" }
"Charlie" --> { "Bob", "Frank" }
"David"   --> { "Alice" }
```

### B. Algorithm Flow: Friend Suggestions
```text
This algorithm identifies friends of friends who are not already directly connected to the target user. It counts mutual friends and ranks suggestions accordingly.

[Start: Get Suggestions for User U]
           |
           v
[Loop: For each Friend F of User U]
           |
           v
    [Loop: For each Neighbor N of F]
               |
               v
       [Is N == U?] ---- Yes --> [Skip]
               |
              No
               |
               v
  [Is N already a direct friend of U?] ---- Yes --> [Skip]
               |
              No
               |
               v
      [Add N to Candidate List]
      [Increment Mutual Count for N]
               |
               v
        [End Inner Loop]
           |
           v
       [End Outer Loop]
           |
           v
[Sort Candidates by Mutual Count (High → Low)]
           |
           v
[Return Sorted List]
```
### C. Algorithm Flow: Shortest Path (BFS)
```text
This algorithm uses Breadth-First Search to compute the shortest connection path between two users. BFS ensures the path found is the shortest in an unweighted graph.

[Start: Find Path from A to B]
           |
           v
[Initialize Queue with (A, path = [A])]
[Mark A as Visited]
           |
           v
[Is Queue Empty?] ---- Yes --> [Return: No Path Found]
           |
          No
           |
           v
[Dequeue Current Node C]
           |
           v
[Is C == B?] ---- Yes --> [Return: Path Found!]
           |
          No
           |
           v
[Loop: For each Neighbor N of C]
               |
               v
      [Is N already Visited?] ---- Yes --> [Skip]
               |
              No
               |
               v
       [Mark N as Visited]
       [Enqueue (N, path + [N])]
               |
               v
       [Repeat Loop]
```

## 6. Code (Implementation)

*check social_network.py(submitted separately)*

## 7. Check (Performance Analysis & Testing)
**Performance Analysis:**
* **Time Complexity:**
    * *Graph Loading:* $O(V + E)$, where $V$ is users and $E$ is friendships.
    * *Shortest Path:* $O(V + E)$ in the worst-case scenario (visiting all nodes and edges).
    * *Suggestions:* $O(N \cdot M)$ where $N$ is the user's friend count and $M$ is the average friends-of-friends count.
* **Space Complexity:** $O(V + E)$ to store the graph in memory.

**Test Results:**
The algorithm was tested on the provided `network.txt` dataset with the following results:
* **Network Statistics:** The system correctly parsed the file, identifying **55 Total Users** and **172 Total Friendships**.
* **Functional Testing:**
    * *Suggestions:* For input "Alice", the system correctly identified "Grace" as a top suggestion with 2 mutual friends (Bob, Frank).
    * *Pathfinding:* For input "Charlie" to "Emma", the system found a shortest path of length 2.
    * *Disconnected Graph:* When testing two disconnected users ("Paul" to "Victor"), the system correctly reported "No connection path found" rather than crashing, handling the error case appropriately.
* **Usability:** The final implementation includes an interactive menu loop, allowing the user to perform multiple queries efficiently without restarting the application.
