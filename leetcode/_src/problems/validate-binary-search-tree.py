PROBLEM = {
    "slug": "validate-binary-search-tree", "number": 98, "title": "Validate Binary Search Tree", "category": "Tree", "difficulty": "Medium",
    "url": "https://leetcode.com/problems/validate-binary-search-tree/", "premium": False,
    "statement_html": """<p>Given the root of a binary tree, decide whether it is a valid binary search tree. In a valid BST every node's value is strictly greater than <em>every</em> value in its left subtree and strictly less than <em>every</em> value in its right subtree, not merely greater than its left child and less than its right child. Duplicates are not allowed.</p>
<pre>
Input:  root = [8, 3, 12, 1, 6]
            8
           / \\
          3   12
         / \\
        1   6
Output: true

Input:  root = [8, 3, 12, 1, 9]
            8
           / \\
          3   12
         / \\
        1   9
Output: false         9 is a left descendant of 8 but 9 > 8
</pre>
<ul>
  <li>1 &le; number of nodes &le; 10<sup>4</sup></li>
  <li>-2<sup>31</sup> &le; Node.val &le; 2<sup>31</sup> - 1</li>
</ul>""",
    "intro_html": """<p><strong>Pass down an allowed range.</strong> Every node must lie strictly inside an open interval <code>(low, high)</code> inherited from its ancestors: the root may be anything, a left child must stay below its parent, a right child must stay above it. Recursing with tightened bounds checks each node against <em>all</em> of its ancestors at once, which the naive parent-child comparison misses. Infinite bounds at the root make the code uniform.</p>""",
    "blocks": [
        {"code": "from typing import Optional\n\nclass Solution:\n    def isValidBST(self, root: Optional[TreeNode]) -> bool:",
         "explain": "<p>LeetCode calls <code>isValidBST</code> with the root and expects a boolean. The method delegates to a helper that carries the two bounds, which the public signature does not have room for.</p>",
         "diagram": None},
        {"code": "        def valid(node: Optional[TreeNode], low: float, high: float) -> bool:",
         "explain": "<p><code>valid</code> answers: is the subtree at <code>node</code> a BST whose values all lie strictly between <code>low</code> and <code>high</code>? The bounds are typed as float so that infinities can be used at the root.</p>",
         "diagram": "  valid(node, low, high)\n  requires: low < every value in the subtree < high"},
        {"code": "            if node is None:\n                return True",
         "explain": "<p>An empty subtree has no values that could violate anything, so it is trivially valid. This ends the recursion below every leaf.</p>",
         "diagram": None},
        {"code": "            if not (low < node.val < high):\n                return False",
         "explain": "<p>Check the node against its inherited window. Python's chained comparison reads naturally and tests both bounds. This is where <code>[8, 3, 12, 1, 9]</code> fails: node 9 arrives with the window <code>(3, 8)</code> from its ancestors and 9 is outside it, even though 9 is bigger than its own parent 3.</p>",
         "diagram": "  tree [8, 3, 12, 1, 9]\n  node 8: window (-inf, inf)  ok\n  node 3: window (-inf, 8)    ok\n  node 9: window (3, 8)       9 < 8 is False -> return False"},
        {"code": "            return valid(node.left, low, node.val) and valid(node.right, node.val, high)",
         "explain": "<p>Tighten the window for each child. Everything on the left must be below this node, so its upper bound becomes <code>node.val</code>; everything on the right must be above it, so its lower bound does. The lower bound of the left child and the upper bound of the right child are inherited unchanged.</p>",
         "diagram": "  tree [8, 3, 12, 1, 6]\n  valid(8, -inf, inf)\n    valid(3, -inf, 8)\n      valid(1, -inf, 3)  -> leaves ok -> True\n      valid(6, 3, 8)     -> leaves ok -> True\n    valid(12, 8, inf)    -> leaves ok -> True\n  -> True"},
        {"code": "        return valid(root, float(\"-inf\"), float(\"inf\"))",
         "explain": "<p>The root has no ancestors, so its window is unbounded. Using infinities instead of <code>None</code> sentinels keeps the comparison in the helper to a single expression.</p>",
         "diagram": "  single node [5]: valid(5, -inf, inf) -> True"},
    ],
    "complexity": "Time O(n), every node is checked once. Space O(h) for the recursion stack.",
}

TESTS = """
s = Solution()
assert s.isValidBST(build_tree([8, 3, 12, 1, 6])) is True
assert s.isValidBST(build_tree([8, 3, 12, 1, 9])) is False
assert s.isValidBST(build_tree([5])) is True
assert s.isValidBST(build_tree([2, 1, 3])) is True
assert s.isValidBST(build_tree([5, 1, 4, None, None, 3, 6])) is False
assert s.isValidBST(build_tree([2, 2, 2])) is False
assert s.isValidBST(build_tree([5, 4, 6, None, None, 3, 7])) is False
assert s.isValidBST(build_tree([-2147483648, None, 2147483647])) is True
"""
