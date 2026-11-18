PROBLEM = {
    "slug": "clone-graph", "number": 133, "title": "Clone Graph", "category": "Graph", "difficulty": "Medium",
    "url": "https://leetcode.com/problems/clone-graph/", "premium": False,
    "statement_html": """<p>You are handed one node of a connected, undirected graph. Every node carries an integer <code>val</code> (the values are unique and run from 1 upwards) and a list <code>neighbors</code> of adjacent nodes. Build and return a <strong>deep copy</strong> of the whole graph: brand new node objects wired together exactly like the originals, so that changing the copy never touches the input. The tests describe a graph by its adjacency list, where entry <code>i</code> lists the values adjacent to node <code>i + 1</code>.</p>
<pre>
Input:  adjList = [[2, 4], [1, 3], [2, 4], [1, 3]]      1 --- 2
Output: [[2, 4], [1, 3], [2, 4], [1, 3]]                |     |
        (same shape, but every node is a new object)    4 --- 3

Input:  adjList = [[]]        a single node with no edges
Output: [[]]
</pre>
<ul>
  <li>0 &le; number of nodes &le; 100, values are unique and 1-indexed</li>
  <li>No self loops and no repeated edges; the graph is connected</li>
  <li>An empty input (<code>node</code> is <code>None</code>) must return <code>None</code></li>
</ul>""",
    "intro_html": """<p><strong>Breadth-first search with an old-to-new dictionary.</strong> We walk the original graph once with a queue, and whenever we meet a node for the first time we create its clone and record the pairing <code>original -&gt; clone</code> in a dict. The dict does double duty: it tells us which nodes we have already visited, and it lets us wire a clone to its neighbours' clones without ever creating a node twice.</p>""",
    "blocks": [
        {"code": "from collections import deque\n\nclass Solution:\n    def cloneGraph(self, node: 'Node') -> 'Node':",
         "explain": "<p>LeetCode calls <code>cloneGraph</code> with one <code>Node</code> of the graph. The class <code>Node</code> has two attributes, <code>val</code> and <code>neighbors</code>, and is supplied by the grader. The quoted type hint <code>'Node'</code> is a forward reference so the hint works even if the class is defined later in the file. <code>deque</code> gives us an O(1) <code>popleft</code> for the BFS queue.</p>",
         "diagram": None},
        {"code": "        if node is None:\n            return None",
         "explain": "<p>The empty graph is the one case where there is nothing to copy. Handling it first means the rest of the code can assume <code>node</code> is a real object.</p>",
         "diagram": None},
        {"code": "        clones = {node: Node(node.val)}",
         "explain": "<p>The heart of the solution: a dictionary mapping each <strong>original node</strong> to its <strong>clone</strong>. Node objects are hashable by identity, so they can be dict keys directly. We seed it with the start node and its freshly made copy. A node is in this dict exactly when it has been discovered, so <code>clones</code> is also our <em>visited</em> set.</p>",
         "diagram": "  original graph        clones (old -> new)\n  1 --- 2\n  |     |               { 1 -> 1' }\n  4 --- 3\n                        1' has val 1 and neighbors [] so far"},
        {"code": "        queue = deque([node])",
         "explain": "<p>The BFS frontier. It holds <em>original</em> nodes whose neighbour lists we still have to process. Anything placed in the queue already has a clone in the dict, which is the invariant we keep for the whole walk.</p>",
         "diagram": "  queue = [1]"},
        {"code": "        while queue:\n            cur = queue.popleft()",
         "explain": "<p>Take the oldest node off the front of the queue. We will now give its clone the right neighbours. Each original node is enqueued once, so this loop runs once per node.</p>",
         "diagram": "  queue = [1]  ->  cur = 1, queue = []"},
        {"code": "            for nb in cur.neighbors:",
         "explain": "<p>Look at every edge leaving <code>cur</code>. Because the graph is undirected, each edge is seen twice in total (once from each end), which is what we want: each clone must list the edge in its own <code>neighbors</code>.</p>",
         "diagram": "  cur = 1, cur.neighbors = [2, 4]"},
        {"code": "                if nb not in clones:\n                    clones[nb] = Node(nb.val)\n                    queue.append(nb)",
         "explain": "<p>First time we see this neighbour? Make its clone, register the pairing, and queue it so its own neighbours get processed later. Creating the clone <em>here</em>, at discovery time, guarantees that by the time any node is popped, every clone it might need to point at already exists or is created on the spot.</p>",
         "diagram": "  cur = 1\n    nb = 2  not in clones -> clones[2] = 2', queue = [2]\n    nb = 4  not in clones -> clones[4] = 4', queue = [2, 4]\n  clones = { 1 -> 1', 2 -> 2', 4 -> 4' }"},
        {"code": "                clones[cur].neighbors.append(clones[nb])",
         "explain": "<p>Wire the edge in the copy: the clone of <code>cur</code> gets the clone of <code>nb</code> appended. We never append an original node, so the copy is fully independent of the input. Appending in the same order as the original keeps the adjacency lists identical.</p>",
         "diagram": "  pop 1: nb=2 new, nb=4 new        1'.neighbors = [2', 4']\n  pop 2: nb=1 known, nb=3 new      2'.neighbors = [1', 3']\n  pop 4: nb=1 known, nb=3 known    4'.neighbors = [1', 3']\n  pop 3: nb=2 known, nb=4 known    3'.neighbors = [2', 4']\n  queue empty -> every clone wired"},
        {"code": "        return clones[node]",
         "explain": "<p>LeetCode wants the clone of the node we were given, which is the entry point into the copied graph. Everything else is reachable from it, exactly as in the original.</p>",
         "diagram": None},
    ],
    "complexity": "Time O(V + E): every node is cloned once and every edge is walked twice. Space O(V) for the dictionary and the queue.",
}

TESTS = """
s = Solution()

def all_nodes(n):
    seen = {}; stack = [n]
    while stack:
        x = stack.pop()
        if id(x) in seen: continue
        seen[id(x)] = x; stack.extend(x.neighbors)
    return seen

adj = [[2, 4], [1, 3], [2, 4], [1, 3]]
g = build_graph(adj)
c = s.cloneGraph(g)
assert graph_to_adj(c) == adj
assert c is not g and c.val == 1
orig, copy = all_nodes(g), all_nodes(c)
assert len(copy) == 4 and not (set(orig) & set(copy))

assert s.cloneGraph(None) is None

single = build_graph([[]])
cs = s.cloneGraph(single)
assert cs is not single and cs.val == 1 and cs.neighbors == []

two = build_graph([[2], [1]])
ct = s.cloneGraph(two)
assert graph_to_adj(ct) == [[2], [1]]
assert ct.neighbors[0] is not two.neighbors[0] and ct.neighbors[0].neighbors[0] is ct

tri = [[2, 3], [1, 3], [1, 2]]
assert graph_to_adj(s.cloneGraph(build_graph(tri))) == tri
"""
