PROBLEM = {
    "slug": "graph-valid-tree", "number": 261, "title": "Graph Valid Tree", "category": "Graph", "difficulty": "Medium",
    "url": "https://leetcode.com/problems/graph-valid-tree/", "premium": True,
    "statement_html": """<p>You have <code>n</code> nodes labelled <code>0</code> to <code>n - 1</code> and a list of undirected edges, each given as a pair <code>[a, b]</code>. Decide whether these edges form a <strong>valid tree</strong>: a graph that is connected (every node can reach every other) and has no cycles. Return <code>true</code> if so, otherwise <code>false</code>.</p>
<pre>
Input:  n = 5, edges = [[0, 1], [0, 2], [1, 3], [1, 4]]
Output: true                0
                           / \\
                          1   2
                         / \\
                        3   4

Input:  n = 4, edges = [[0, 1], [1, 2], [2, 0]]
Output: false       0-1-2 form a cycle, and node 3 is unreachable
</pre>
<ul>
  <li>1 &le; n &le; 2000, 0 &le; len(edges) &le; 5000</li>
  <li>No self loops and no duplicate edges</li>
  <li>A single node with no edges is a valid tree</li>
</ul>""",
    "intro_html": """<p><strong>Edge count plus one traversal.</strong> A tree on <code>n</code> nodes has exactly <code>n - 1</code> edges, so any other count is an instant <code>false</code>. Given exactly <code>n - 1</code> edges, the graph is a tree if and only if it is connected (a cycle would \"waste\" an edge and leave some node cut off). So we build an adjacency list, run one depth-first search from node 0, and check that it reaches all <code>n</code> nodes.</p>""",
    "blocks": [
        {"code": "from typing import List\n\nclass Solution:\n    def validTree(self, n: int, edges: List[List[int]]) -> bool:",
         "explain": "<p>LeetCode's premium template names the method <code>validTree</code> and passes the node count and the edge list; it returns a boolean.</p>",
         "diagram": None},
        {"code": "        if len(edges) != n - 1:\n            return False",
         "explain": "<p>The counting shortcut. Fewer than <code>n - 1</code> edges cannot connect <code>n</code> nodes; more than <code>n - 1</code> edges must create a cycle. This single check removes half the work: after it we never have to detect cycles explicitly, only connectivity.</p>",
         "diagram": "  n = 5, 4 edges  -> 4 == 5 - 1, keep going\n  n = 4, 3 edges  -> 3 == 4 - 1, keep going (cycle caught below)\n  n = 3, 3 edges  -> too many edges, False at once"},
        {"code": "        adj = [[] for _ in range(n)]\n        for a, b in edges:\n            adj[a].append(b)\n            adj[b].append(a)",
         "explain": "<p>Adjacency list for an undirected graph: each edge is recorded in both directions so the traversal can move either way along it.</p>",
         "diagram": "  edges = [[0,1], [0,2], [1,3], [1,4]]\n  adj = [[1, 2],    # 0\n         [0, 3, 4], # 1\n         [0],       # 2\n         [1],       # 3\n         [1]]       # 4"},
        {"code": "        seen = {0}\n        stack = [0]",
         "explain": "<p>Iterative DFS state. We start from node 0 (any node would do, since a tree is connected from everywhere). <code>seen</code> records discovered nodes; <code>stack</code> holds the nodes whose neighbours we still need to explore. Using an explicit stack avoids Python's recursion limit on long chains.</p>",
         "diagram": "  seen = {0}      stack = [0]"},
        {"code": "        while stack:\n            cur = stack.pop()\n            for nb in adj[cur]:\n                if nb not in seen:\n                    seen.add(nb)\n                    stack.append(nb)",
         "explain": "<p>Standard traversal: pop a node, push every neighbour we have not met yet. We mark a node as seen when it is <em>pushed</em>, not when it is popped, so no node is pushed twice. With exactly <code>n - 1</code> edges there is no need to check for cycles here; if the graph were cyclic some node would simply never be reached.</p>",
         "diagram": "  pop 0: push 1, 2       seen = {0,1,2}        stack = [1, 2]\n  pop 2: 0 seen          seen = {0,1,2}        stack = [1]\n  pop 1: push 3, 4       seen = {0,1,2,3,4}    stack = [3, 4]\n  pop 4, pop 3: nothing new                    stack = []"},
        {"code": "        return len(seen) == n",
         "explain": "<p>Reaching all <code>n</code> nodes from node 0 means the graph is connected, and combined with the edge count that makes it a tree. In the second example the 3 edges form a triangle on 0, 1, 2, so the DFS stops at 3 nodes and 3 != 4 gives <code>false</code>.</p>",
         "diagram": "  example 1: seen = {0,1,2,3,4}, 5 == 5 -> True\n  example 2: edges [[0,1],[1,2],[2,0]], n = 4\n             seen = {0,1,2}, 3 != 4 -> False"},
    ],
    "complexity": "Time O(n + E), and since E = n - 1 when we get past the first check, effectively O(n). Space O(n) for the adjacency list, the seen set and the stack.",
}

TESTS = """
s = Solution()
assert s.validTree(5, [[0, 1], [0, 2], [1, 3], [1, 4]]) is True
assert s.validTree(4, [[0, 1], [1, 2], [2, 0]]) is False
assert s.validTree(1, []) is True
assert s.validTree(2, []) is False
assert s.validTree(2, [[0, 1]]) is True
assert s.validTree(4, [[0, 1], [2, 3]]) is False
assert s.validTree(5, [[0, 1], [1, 2], [2, 3], [1, 3], [1, 4]]) is False
assert s.validTree(5, [[0, 1], [1, 2], [2, 3], [3, 4]]) is True
"""
