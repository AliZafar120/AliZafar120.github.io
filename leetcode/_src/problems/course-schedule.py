PROBLEM = {
    "slug": "course-schedule", "number": 207, "title": "Course Schedule", "category": "Graph", "difficulty": "Medium",
    "url": "https://leetcode.com/problems/course-schedule/", "premium": False,
    "statement_html": """<p>There are <code>numCourses</code> courses numbered from <code>0</code> to <code>numCourses - 1</code>. You are given a list of prerequisite pairs where <code>[a, b]</code> means you must pass course <code>b</code> before you may take course <code>a</code>. Decide whether it is possible to finish every course, which is only impossible when the prerequisites chase each other in a circle.</p>
<pre>
Input:  numCourses = 4, prerequisites = [[1, 0], [2, 0], [3, 1], [3, 2]]
Output: true          one valid plan: 0, 1, 2, 3

Input:  numCourses = 2, prerequisites = [[0, 1], [1, 0]]
Output: false         0 needs 1 and 1 needs 0
</pre>
<ul>
  <li>1 &le; numCourses &le; 2000, 0 &le; len(prerequisites) &le; 5000</li>
  <li>Each pair holds two distinct course numbers and no pair is repeated</li>
</ul>""",
    "intro_html": """<p><strong>Kahn's algorithm (BFS topological sort).</strong> Treat each prerequisite as a directed edge <code>b -&gt; a</code> and count how many prerequisites each course still has (its in-degree). Courses with in-degree zero can be taken right now; taking one releases its dependants, whose in-degree drops. If this peeling process reaches every course the graph is acyclic and the answer is true; any course left with a positive in-degree is stuck in a cycle.</p>""",
    "blocks": [
        {"code": "from collections import deque\nfrom typing import List\n\nclass Solution:\n    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:",
         "explain": "<p>LeetCode calls <code>canFinish</code> with the course count and the prerequisite pairs and expects a boolean. <code>deque</code> provides an O(1) queue for the BFS part of the algorithm.</p>",
         "diagram": None},
        {"code": "        adj = [[] for _ in range(numCourses)]\n        indegree = [0] * numCourses",
         "explain": "<p>Two arrays indexed by course. <code>adj[b]</code> will list the courses that become available once <code>b</code> is done. <code>indegree[a]</code> counts how many prerequisites <code>a</code> still needs. Lists are used instead of dicts because the courses are already dense integers.</p>",
         "diagram": "  numCourses = 4\n  adj      = [[], [], [], []]\n  indegree = [0, 0, 0, 0]"},
        {"code": "        for course, pre in prerequisites:\n            adj[pre].append(course)\n            indegree[course] += 1",
         "explain": "<p>Build the graph. The pair <code>[course, pre]</code> becomes an edge from <code>pre</code> to <code>course</code>, pointing in the direction you move through the degree. Every incoming edge bumps the in-degree of its target.</p>",
         "diagram": "  prerequisites = [[1,0], [2,0], [3,1], [3,2]]\n\n       0 -> 1 -> 3        adj      = [[1,2], [3], [3], []]\n       |         ^        indegree = [0, 1, 1, 2]\n       +--> 2 ---+"},
        {"code": "        queue = deque(i for i in range(numCourses) if indegree[i] == 0)",
         "explain": "<p>Seed the queue with every course that has no prerequisites at all. These are the ones we can take on day one. If this queue is empty and there are courses, every course depends on another one and we already know the answer will be false (the loop below will simply never run).</p>",
         "diagram": "  indegree = [0, 1, 1, 2]  ->  queue = [0]"},
        {"code": "        taken = 0\n        while queue:\n            cur = queue.popleft()\n            taken += 1",
         "explain": "<p>Pop a course that is ready and \"take\" it. We only need the <em>count</em> of courses taken, not their order, because the question is yes or no. (Returning the order instead would turn this into Course Schedule II.)</p>",
         "diagram": "  queue = [0]  ->  cur = 0, taken = 1"},
        {"code": "            for nxt in adj[cur]:\n                indegree[nxt] -= 1\n                if indegree[nxt] == 0:\n                    queue.append(nxt)",
         "explain": "<p>Finishing <code>cur</code> satisfies one prerequisite of each course it points to, so their in-degrees drop. A course whose in-degree hits zero has everything it needs and joins the queue. Each edge is relaxed exactly once, so this is linear in the number of edges.</p>",
         "diagram": "  cur=0: indegree -> [0,0,0,2]  queue=[1,2]   taken=1\n  cur=1: indegree -> [0,0,0,1]  queue=[2]     taken=2\n  cur=2: indegree -> [0,0,0,0]  queue=[3]     taken=3\n  cur=3: no outgoing edges      queue=[]      taken=4"},
        {"code": "        return taken == numCourses",
         "explain": "<p>If every course was taken, the dependency graph has no cycle. If some were never reached, they sit in a cycle (or behind one) and their in-degree never fell to zero. In the two-course example <code>0 &lt;-&gt; 1</code> both start with in-degree 1, the queue is empty from the start, and <code>taken</code> stays 0.</p>",
         "diagram": "  [[0,1],[1,0]]: indegree=[1, 1]  queue=[]  taken=0 != 2 -> False"},
    ],
    "complexity": "Time O(V + E) where V is the number of courses and E the number of prerequisite pairs. Space O(V + E) for the adjacency lists, in-degree array and queue.",
}

TESTS = """
s = Solution()
assert s.canFinish(4, [[1, 0], [2, 0], [3, 1], [3, 2]]) is True
assert s.canFinish(2, [[0, 1], [1, 0]]) is False
assert s.canFinish(1, []) is True
assert s.canFinish(3, []) is True
assert s.canFinish(3, [[0, 1], [1, 2], [2, 0]]) is False
assert s.canFinish(5, [[1, 0], [2, 1], [3, 2], [4, 3]]) is True
assert s.canFinish(4, [[1, 0], [2, 1], [3, 2], [1, 3]]) is False
"""
