PROBLEM = {
    "slug": "number-of-connected-components-in-an-undirected-graph", "number": 323, "title": "Number of Connected Components in an Undirected Graph", "category": "Graph", "difficulty": "Medium",
    "url": "https://leetcode.com/problems/number-of-connected-components-in-an-undirected-graph/", "premium": True,
    "statement_html": """<p>You are given <code>n</code> nodes labelled <code>0</code> to <code>n - 1</code> and a list of undirected edges <code>[a, b]</code>. A connected component is a group of nodes that can all reach each other by following edges; an isolated node is a component of its own. Return how many connected components the graph has.</p>
<pre>
Input:  n = 6, edges = [[0, 1], [1, 2], [3, 4]]
Output: 3            {0, 1, 2}   {3, 4}   {5}

Input:  n = 3, edges = []
Output: 3
</pre>
<ul>
  <li>1 &le; n &le; 2000, 0 &le; len(edges) &le; 5000</li>
  <li>No self loops and no duplicate edges</li>
</ul>""",
    "intro_html": """<p><strong>Union-Find (disjoint set union).</strong> Start by treating every node as its own component, so there are <code>n</code> of them. Then process each edge: find the representative (root) of each endpoint; if the roots differ, the edge joins two previously separate components, so merge them and decrement the count. If the roots are already the same the edge is redundant. Path compression keeps the <code>find</code> operation almost constant time.</p>""",
    "blocks": [
        {"code": "from typing import List\n\nclass Solution:\n    def countComponents(self, n: int, edges: List[List[int]]) -> int:",
         "explain": "<p>LeetCode's premium template names the method <code>countComponents</code>; it receives the node count and the edges and returns an integer.</p>",
         "diagram": None},
        {"code": "        parent = list(range(n))",
         "explain": "<p>The entire union-find structure is this one array. <code>parent[x]</code> points to some other node in the same component, and a node that points to <em>itself</em> is the root, the representative of its component. Initially every node is its own root, which encodes <code>n</code> singleton components.</p>",
         "diagram": "  n = 6\n  node   : 0 1 2 3 4 5\n  parent : 0 1 2 3 4 5     every node is its own root"},
        {"code": "        def find(x: int) -> int:\n            while parent[x] != x:\n                parent[x] = parent[parent[x]]\n                x = parent[x]\n            return x",
         "explain": "<p>Follow parent pointers up until we hit a root. The line <code>parent[x] = parent[parent[x]]</code> is <strong>path compression</strong> (the \"path halving\" variant): while climbing, we make each node skip over its parent and point at its grandparent. The tree gets flatter every time anyone walks through it, so later <code>find</code> calls are nearly O(1). Without compression a chain of unions could build a tall tree and make <code>find</code> O(n).</p>",
         "diagram": "  before find(3):   0 <- 1 <- 2 <- 3     (3 -> 2 -> 1 -> 0)\n  step at x=3: parent[3] = parent[2] = 1,  x = 1\n  step at x=1: parent[1] = parent[1] = 0,  x = 0 (root)\n  after:            0 <- 1          0 <- 3\n                    0 <- 2          chain is flattened"},
        {"code": "        components = n",
         "explain": "<p>Count the components by subtraction. We begin with <code>n</code> singletons and will lower this number by one for every edge that actually merges two groups.</p>",
         "diagram": "  components = 6"},
        {"code": "        for a, b in edges:\n            root_a, root_b = find(a), find(b)",
         "explain": "<p>For each edge, locate the representative of both endpoints. Two nodes are in the same component exactly when their roots are the same object, so comparing roots answers \"already connected?\" directly.</p>",
         "diagram": "  edge [0, 1]: find(0) = 0, find(1) = 1   -> different\n  edge [1, 2]: find(1) = 1, find(2) = 2   -> different\n  edge [3, 4]: find(3) = 3, find(4) = 4   -> different"},
        {"code": "            if root_a != root_b:\n                parent[root_a] = root_b\n                components -= 1",
         "explain": "<p>The <strong>union</strong> step: hang one root under the other, which merges the two trees into one component, and record that the count went down. If the roots were already equal the edge lies inside an existing component and changes nothing. (Union by rank would choose which root goes under which more carefully; with path compression alone the structure is already fast enough for interview purposes.)</p>",
         "diagram": "  edge [0,1]: parent[0] = 1   components 6 -> 5\n  edge [1,2]: parent[1] = 2   components 5 -> 4\n  edge [3,4]: parent[3] = 4   components 4 -> 3\n\n  parent : [1, 2, 2, 4, 4, 5]\n  trees  :   2        4      5\n            /        /\n           1        3\n          /\n         0"},
        {"code": "        return components",
         "explain": "<p>Every merging edge has been subtracted. What remains is the number of distinct roots, which is the number of connected components. With no edges at all the loop never runs and the answer is simply <code>n</code>.</p>",
         "diagram": "  components = 3  ->  {0,1,2}  {3,4}  {5}"},
    ],
    "complexity": "Time O(n + E * alpha(n)) where alpha is the inverse Ackermann function, effectively constant, so O(n + E) in practice. Space O(n) for the parent array.",
}

TESTS = """
s = Solution()
assert s.countComponents(6, [[0, 1], [1, 2], [3, 4]]) == 3
assert s.countComponents(3, []) == 3
assert s.countComponents(1, []) == 1
assert s.countComponents(5, [[0, 1], [1, 2], [2, 3], [3, 4]]) == 1
assert s.countComponents(4, [[0, 1], [1, 2], [2, 0]]) == 2
assert s.countComponents(5, [[0, 1], [1, 2], [3, 4], [0, 2]]) == 2
assert s.countComponents(7, [[0, 1], [2, 3], [4, 5], [1, 3], [5, 6]]) == 2
"""
