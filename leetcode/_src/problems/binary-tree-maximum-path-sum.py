PROBLEM = {
    "slug": "binary-tree-maximum-path-sum", "number": 124, "title": "Binary Tree Maximum Path Sum", "category": "Tree", "difficulty": "Hard",
    "url": "https://leetcode.com/problems/binary-tree-maximum-path-sum/", "premium": False,
    "statement_html": """<p>A path in a binary tree is any sequence of nodes where consecutive nodes are joined by an edge and no node appears twice. The path does not need to pass through the root and may consist of a single node. Given the root, return the largest possible sum of node values along any path. Values can be negative, so sometimes the best path is a single node.</p>
<pre>
Input:  root = [-10, 9, 20, null, null, 15, 7]
         -10
         /  \\
        9    20
            /  \\
           15   7
Output: 42            the path 15 -> 20 -> 7

Input:  root = [-3]
Output: -3            a single node is still a path
</pre>
<ul>
  <li>1 &le; number of nodes &le; 3 &middot; 10<sup>4</sup></li>
  <li>-1000 &le; Node.val &le; 1000</li>
</ul>""",
    "intro_html": """<p><strong>Postorder gain with a global best.</strong> For each node we compute its <em>gain</em>: the best sum of a path that starts at that node and goes straight down one side, clamped at zero so a negative branch is simply not taken. While we have both children's gains in hand, the best path that <em>bends</em> at this node is <code>node.val + left gain + right gain</code>; we compare that against a running maximum. The node then reports only the one-sided gain upwards, because a parent can extend a path down only one side.</p>""",
    "blocks": [
        {"code": "from typing import Optional\n\nclass Solution:\n    def maxPathSum(self, root: Optional[TreeNode]) -> int:",
         "explain": "<p>LeetCode calls <code>maxPathSum</code> with a non-empty tree and expects an integer. The real work happens in a nested helper that returns one thing and records another.</p>",
         "diagram": None},
        {"code": "        best = root.val",
         "explain": "<p>The answer so far. Starting from <code>root.val</code> rather than negative infinity is safe because the root alone is a valid path, and it keeps the all-negative case correct without special handling.</p>",
         "diagram": "  tree: [-10, 9, 20, null, null, 15, 7]\n  best = -10"},
        {"code": "        def gain(node: Optional[TreeNode]) -> int:\n            nonlocal best",
         "explain": "<p><code>gain(node)</code> returns the maximum sum of a downward path that <em>starts</em> at <code>node</code> and continues into at most one child. It needs <code>nonlocal best</code> so that assigning to <code>best</code> inside updates the enclosing variable instead of creating a local one.</p>",
         "diagram": "  gain(node) = node.val + max(0, gain(left), gain(right))\n  \"one straight leg, pointing down\""},
        {"code": "            if node is None:\n                return 0",
         "explain": "<p>An empty subtree offers no gain. Returning 0 means a leaf's gain is simply its own value.</p>",
         "diagram": "  gain(None) = 0\n  gain(9)  = 9  + max(0, 0) = 9\n  gain(15) = 15, gain(7) = 7"},
        {"code": "            left = max(gain(node.left), 0)",
         "explain": "<p>Recurse into the left child and clamp at zero. If the left branch would only subtract from the total, the best choice is not to include it, and a zero contribution expresses \"stop here\".</p>",
         "diagram": "  at node 20: left = max(gain(15), 0) = 15\n  at node -10: left = max(gain(9), 0) = 9\n\n  if a child had gain -4:  max(-4, 0) = 0  -> branch ignored"},
        {"code": "            right = max(gain(node.right), 0)",
         "explain": "<p>The same for the right child. Both children are now fully processed before the node itself, which is the postorder shape: the node's answer depends on its children's answers.</p>",
         "diagram": "  at node 20: right = max(gain(7), 0) = 7\n  at node -10: right = max(gain(20), 0) = 35"},
        {"code": "            best = max(best, node.val + left + right)",
         "explain": "<p>The best path whose <strong>highest point</strong> is this node goes down the left leg, through the node, and down the right leg. Only here, where both legs are known, can this bent path be measured, so this is where the global answer is updated.</p>",
         "diagram": "  at node 20:  -10 vs 20 + 15 + 7 = 42   -> best = 42\n  at node -10: 42 vs -10 + 9 + 35 = 34   -> best stays 42\n\n          -10\n         /   \\\\\n        9     20      path 15 -> 20 -> 7 bends at 20\n             /  \\\\\n           15    7"},
        {"code": "            return node.val + max(left, right)",
         "explain": "<p>What the parent may use: a path from the parent can come down into this node and continue down only <em>one</em> leg, so we report the node plus the better leg. The bent path was already accounted for in <code>best</code> and must not be passed upwards.</p>",
         "diagram": "  gain(20) = 20 + max(15, 7) = 35\n  gain(-10) = -10 + max(9, 35) = 25  (returned; best stays 42)"},
        {"code": "        gain(root)\n        return best",
         "explain": "<p>Run the traversal from the root. Its return value is the best path that starts at the root, which is not what we want; the answer is the running maximum that every node contributed to.</p>",
         "diagram": "  single node [-3]: best = -3, gain(-3) updates best = max(-3, -3) = -3\n  return -3"},
    ],
    "complexity": "Time O(n), one postorder pass. Space O(h) for the recursion stack.",
}

TESTS = """
s = Solution()
assert s.maxPathSum(build_tree([-10, 9, 20, None, None, 15, 7])) == 42
assert s.maxPathSum(build_tree([-3])) == -3
assert s.maxPathSum(build_tree([1, 2, 3])) == 6
assert s.maxPathSum(build_tree([-2, -1, -3])) == -1
assert s.maxPathSum(build_tree([2, -1])) == 2
assert s.maxPathSum(build_tree([5, 4, 8, 11, None, 13, 4, 7, 2, None, None, None, 1])) == 48
assert s.maxPathSum(build_tree([1, -2, 3])) == 4
"""
