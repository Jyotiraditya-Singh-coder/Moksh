# List of DSA topics with subtopics and difficulty levels
DSA_TOPICS = {
    "arrays": {
        "name": "Arrays",
        "subtopics": ["traversal", "insertion", "deletion", "searching", "sorting", "two-pointer", "sliding-window", "prefix-sum"],
        "difficulty_levels": ["easy", "medium", "hard"]
    },
    "linked-lists": {
        "name": "Linked Lists",
        "subtopics": ["singly-linked-list", "doubly-linked-list", "circular-linked-list", "reversal", "detect-cycle", "merge-sorted", "intersection"],
        "difficulty_levels": ["easy", "medium", "hard"]
    },
    "stacks-queues": {
        "name": "Stacks and Queues",
        "subtopics": ["stack-using-arrays", "stack-using-linked-list", "queue-using-arrays", "queue-using-linked-list", "circular-queue", "deque", "monotonic-stack"],
        "difficulty_levels": ["easy", "medium", "hard"]
    },
    "trees": {
        "name": "Trees",
        "subtopics": ["binary-tree", "binary-search-tree", "tree-traversals", "height-depth", "balanced-tree", "lca", "serialization"],
        "difficulty_levels": ["easy", "medium", "hard"]
    },
    "graphs": {
        "name": "Graphs",
        "subtopics": ["representation", "bfs", "dfs", "shortest-path", "minimum-spanning-tree", "topological-sort", "strongly-connected-components"],
        "difficulty_levels": ["easy", "medium", "hard"]
    },
    "dynamic-programming": {
        "name": "Dynamic Programming",
        "subtopics": ["memoization", "tabulation", "knapsack", "lcs", "lis", "edit-distance", "matrix-chain"],
        "difficulty_levels": ["easy", "medium", "hard"]
    },
    "greedy-algorithms": {
        "name": "Greedy Algorithms",
        "subtopics": ["activity-selection", "fractional-knapsack", "huffman-coding", "job-sequencing", "minimum-coins"],
        "difficulty_levels": ["easy", "medium", "hard"]
    },
    "backtracking": {
        "name": "Backtracking",
        "subtopics": ["n-queens", "sudoku", "rat-in-maze", "knight-tour", "permutations", "combinations"],
        "difficulty_levels": ["easy", "medium", "hard"]
    },
    "searching-sorting": {
        "name": "Searching and Sorting",
        "subtopics": ["binary-search", "merge-sort", "quick-sort", "heap-sort", "counting-sort", "radix-sort"],
        "difficulty_levels": ["easy", "medium", "hard"]
    },
    "hashing": {
        "name": "Hashing",
        "subtopics": ["hash-table", "hash-set", "hash-map", "collision-resolution", "frequency-count", "subarray-sum"],
        "difficulty_levels": ["easy", "medium", "hard"]
    }
}

def get_all_topics():
    return list(DSA_TOPICS.keys())

def get_topic_info(topic_id):
    return DSA_TOPICS.get(topic_id, {})