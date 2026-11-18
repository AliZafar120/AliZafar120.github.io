PROBLEM = {
    "slug": "binary-tree-level-order-traversal", "number": 102, "title": "Binary Tree Level Order Traversal", "category": "Tree", "difficulty": "Medium",
    "url": "https://leetcode.com/problems/binary-tree-level-order-traversal/", "premium": False,
    "statement_html": """<p>Given the root of a binary tree, return its node values grouped by depth: the root's value on its own in the first list, then both children of the root left to right, then all grandchildren left to right, and so on. The output is a list of lists, one per level.</p>
<pre>
Input:  root = [1, 2, 3, 4, null, null, 5]
            1
           / \\
          2   3
         /     \\
        4       5
Output: [[1], [2, 3], [4, 5]]

Input:  root = []
Output: []
</pre>
<ul>
  <li>0 &le; number of nodes &le; 2000</li>
  <li>-1000 &le; Node.val &le; 1000</li>
</ul>""",
    "intro_html": """<p><strong>Breadth-first search, one level per round.</strong> A queue holds the nodes of the current level. In each round we note how many nodes the queue holds, pop exactly that many (collecting their values into one list) and push their children, which form the next level. Taking a snapshot of the queue size before popping is what cleanly separates one level from the next.</p>""",
    "blocks": [
        {"code": "from collections import deque\nfrom typing import List, Optional\n\nclass Solution:\n    def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:",
         "explain": "<p>LeetCode calls <code>levelOrder</code> with the root and expects a list of levels. <code>deque</code> gives O(1) pops from the front, which a plain list cannot (<code>list.pop(0)</code> is O(n)).</p>",
         "diagram": None},
        {"code": "        if root is None:\n            return []",
         "explain": "<p>An empty tree has no levels. Handling it here lets the queue start with a real node and keeps the loop free of <code>None</code> checks on the root.</p>",
         "diagram": None},
        {"code": "        result = []\n        queue = deque([root])",
         "explain": "<p><code>result</code> will receive one list per level. The queue is seeded with the root, which is the entire first level by itself.</p>",
         "diagram": "  tree [1, 2, 3, 4, null, null, 5]\n  queue = [1]        result = []"},
        {"code": "        while queue:\n            level = []",
         "explain": "<p>Each pass of the outer loop processes exactly one level. <code>level</code> gathers that level's values. When the queue is empty there are no more nodes anywhere below, so we are done.</p>",
         "diagram": "  round 1: queue = [1]       level = []\n  round 2: queue = [2, 3]    level = []\n  round 3: queue = [4, 5]    level = []"},
        {"code": "            for _ in range(len(queue)):\n                node = queue.popleft()\n                level.append(node.val)",
         "explain": "<p>The key trick: <code>len(queue)</code> is evaluated once, when the loop starts, so the loop runs exactly as many times as there are nodes in the current level, even though we will be appending children to the same queue inside. Each popped node's value goes into the current level.</p>",
         "diagram": "  round 2: len(queue) = 2, so pop twice\n    pop 2 -> level = [2]      queue = [3]       (then push 4)\n    pop 3 -> level = [2, 3]   queue = [4]       (then push 5)\n  queue is now [4, 5] but the loop has already finished"},
        {"code": "                if node.left:\n                    queue.append(node.left)\n                if node.right:\n                    queue.append(node.right)",
         "explain": "<p>Enqueue the children, left before right so that the next level comes out in left-to-right order. Skipping <code>None</code> children keeps the queue to real nodes only, so <code>len(queue)</code> is an accurate count of the next level.</p>",
         "diagram": "  round 1: pop 1, push 2, 3        queue = [2, 3]\n  round 2: pop 2, push 4           queue = [3, 4]\n           pop 3, push 5           queue = [4, 5]\n  round 3: pop 4, no children      queue = [5]\n           pop 5, no children      queue = []"},
        {"code": "            result.append(level)",
         "explain": "<p>The inner loop has consumed the whole level, so its list is complete. Append it, then the outer loop moves on to the children now waiting in the queue.</p>",
         "diagram": "  after round 1: result = [[1]]\n  after round 2: result = [[1], [2, 3]]\n  after round 3: result = [[1], [2, 3], [4, 5]]"},
        {"code": "        return result",
         "explain": "<p>The queue is empty, meaning the deepest level has been processed, and <code>result</code> holds every level from top to bottom.</p>",
         "diagram": None},
    ],
    "complexity": "Time O(n), each node is enqueued and dequeued once. Space O(w) for the queue, where w is the maximum width of the tree (up to n/2), plus O(n) for the output.",
}

TESTS = """
s = Solution()
assert s.levelOrder(build_tree([1, 2, 3, 4, None, None, 5])) == [[1], [2, 3], [4, 5]]
assert s.levelOrder(build_tree([])) == []
assert s.levelOrder(build_tree([7])) == [[7]]
assert s.levelOrder(build_tree([3, 9, 20, None, None, 15, 7])) == [[3], [9, 20], [15, 7]]
assert s.levelOrder(build_tree([1, None, 2, None, 3])) == [[1], [2], [3]]
assert s.levelOrder(build_tree([1, 2, 3, 4, 5, 6, 7])) == [[1], [2, 3], [4, 5, 6, 7]]
"""
