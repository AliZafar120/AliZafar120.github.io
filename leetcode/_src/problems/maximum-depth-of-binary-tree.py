PROBLEM = {
    "slug": "maximum-depth-of-binary-tree", "number": 104, "title": "Maximum Depth of Binary Tree", "category": "Tree", "difficulty": "Easy",
    "url": "https://leetcode.com/problems/maximum-depth-of-binary-tree/", "premium": False,
    "statement_html": """<p>Given the root of a binary tree, return its maximum depth: the number of nodes on the longest path from the root down to a leaf. A tree with a single node has depth 1 and an empty tree has depth 0.</p>
<pre>
Input:  root = [5, 3, 8, null, null, 7, null, 6]
            5
           / \\
          3   8
             /
            7
           /
          6
Output: 4             the path 5 -> 8 -> 7 -> 6 has four nodes

Input:  root = []
Output: 0
</pre>
<ul>
  <li>0 &le; number of nodes &le; 10<sup>4</sup></li>
  <li>-100 &le; Node.val &le; 100</li>
</ul>""",
    "intro_html": """<p><strong>Postorder recursion.</strong> The depth of a tree is one more than the depth of its deeper child. That sentence is the whole algorithm: recurse into both subtrees, take the larger answer, add one for the current node. The empty tree is the base case with depth 0.</p>""",
    "blocks": [
        {"code": "from typing import Optional\n\nclass Solution:\n    def maxDepth(self, root: Optional[TreeNode]) -> int:",
         "explain": "<p>LeetCode calls <code>maxDepth</code> with the root <code>TreeNode</code> (or <code>None</code> for an empty tree). <code>TreeNode</code> has <code>val</code>, <code>left</code> and <code>right</code> attributes and is supplied by the grader.</p>",
         "diagram": None},
        {"code": "        if root is None:\n            return 0",
         "explain": "<p>The base case. An empty subtree contributes no nodes to any path, so its depth is 0. Every recursive descent eventually hits <code>None</code> below a leaf, which is what stops the recursion.</p>",
         "diagram": "  maxDepth(None) = 0\n\n  leaf 6:   maxDepth(6) = 1 + max(maxDepth(None), maxDepth(None))\n                        = 1 + max(0, 0) = 1"},
        {"code": "        left = self.maxDepth(root.left)",
         "explain": "<p>Ask the left subtree how deep it is. We trust the recursion to return the correct depth for any smaller tree; that is the inductive leap that makes the three-line solution work.</p>",
         "diagram": "            5\n           / \\\\\n          3   8\n             /\n            7\n           /\n          6\n  at node 5: left = maxDepth(3) = 1"},
        {"code": "        right = self.maxDepth(root.right)",
         "explain": "<p>Same question for the right subtree. The two calls are independent, so the order does not matter; both are needed because the longest path could be on either side.</p>",
         "diagram": "  at node 5: right = maxDepth(8)\n    at node 8: left = maxDepth(7)\n      at node 7: left = maxDepth(6) = 1, right = 0 -> 2\n    at node 8: right = maxDepth(None) = 0 -> 1 + max(2, 0) = 3\n  right = 3"},
        {"code": "        return 1 + max(left, right)",
         "explain": "<p>The current node sits on top of whichever child path is longer, so it adds exactly one to that depth. Returning this value to the caller lets the parent make the same decision one level up.</p>",
         "diagram": "  node 5: 1 + max(left=1, right=3) = 4\n\n  call stack unwinds:\n  maxDepth(6)=1 -> maxDepth(7)=2 -> maxDepth(8)=3 -> maxDepth(5)=4"},
    ],
    "complexity": "Time O(n), every node is visited once. Space O(h) for the recursion stack, where h is the tree height (O(n) for a degenerate chain).",
}

TESTS = """
s = Solution()
assert s.maxDepth(build_tree([5, 3, 8, None, None, 7, None, 6])) == 4
assert s.maxDepth(build_tree([])) == 0
assert s.maxDepth(build_tree([1])) == 1
assert s.maxDepth(build_tree([3, 9, 20, None, None, 15, 7])) == 3
assert s.maxDepth(build_tree([1, None, 2])) == 2
assert s.maxDepth(build_tree([1, 2, None, 3, None, 4])) == 4
"""
