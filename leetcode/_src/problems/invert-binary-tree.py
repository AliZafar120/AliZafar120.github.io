PROBLEM = {
    "slug": "invert-binary-tree", "number": 226, "title": "Invert Binary Tree", "category": "Tree", "difficulty": "Easy",
    "url": "https://leetcode.com/problems/invert-binary-tree/", "premium": False,
    "statement_html": """<p>Given the root of a binary tree, mirror it: at every node, swap the left and right children. Return the root of the mirrored tree. The result is what you would see if you held the original tree up to a mirror.</p>
<pre>
Input:  root = [6, 2, 9, 1, 4]
          6                 6
         / \\      ->       / \\
        2   9             9   2
       / \\                   / \\
      1   4                 4   1
Output: [6, 9, 2, null, null, 4, 1]

Input:  root = [1, null, 2]
Output: [1, 2]
</pre>
<ul>
  <li>0 &le; number of nodes &le; 100</li>
  <li>-100 &le; Node.val &le; 100</li>
</ul>""",
    "intro_html": """<p><strong>Swap children, then recurse.</strong> Mirroring a tree means swapping the two children of the root and mirroring each child subtree. The recursion does exactly that, in place, in one pass. The empty tree is its own mirror and ends the recursion.</p>""",
    "blocks": [
        {"code": "from typing import Optional\n\nclass Solution:\n    def invertTree(self, root: Optional[TreeNode]) -> Optional[TreeNode]:",
         "explain": "<p>LeetCode calls <code>invertTree</code> with the root and expects the root of the inverted tree back. We modify the nodes in place and return the same root object.</p>",
         "diagram": None},
        {"code": "        if root is None:\n            return None",
         "explain": "<p>Base case: there is nothing to swap in an empty subtree. Every path down the tree ends here, below a leaf, which is what terminates the recursion.</p>",
         "diagram": "  invertTree(None) -> None\n  leaf 1: swap None and None (no change), recurse into both -> done"},
        {"code": "        root.left, root.right = root.right, root.left",
         "explain": "<p>The swap. Python's tuple assignment exchanges the two references without a temporary variable. Note we swap the whole subtrees, not just the child values, so everything below moves with them.</p>",
         "diagram": "  at node 6:   before          after\n               6               6\n              / \\\\             / \\\\\n             2   9           9   2\n            / \\\\                 / \\\\\n           1   4               1   4   (2's children not yet swapped)"},
        {"code": "        self.invertTree(root.left)\n        self.invertTree(root.right)",
         "explain": "<p>Now mirror the two subtrees themselves. After the swap, <code>root.left</code> is the old right subtree and vice versa, but that does not matter: both get inverted either way. The return values are ignored because the children are modified in place.</p>",
         "diagram": "  invertTree(9): no children, nothing changes\n  invertTree(2): swap 1 and 4\n               6\n              / \\\\\n             9   2\n                / \\\\\n               4   1"},
        {"code": "        return root",
         "explain": "<p>The root object is unchanged in identity, only its children have moved, so returning it gives the caller the mirrored tree. This also lets the recursive calls be used as expressions if preferred.</p>",
         "diagram": "  result in level order: [6, 9, 2, None, None, 4, 1]"},
    ],
    "complexity": "Time O(n), each node is visited once. Space O(h) for the recursion stack.",
}

TESTS = """
s = Solution()
assert to_level_order(s.invertTree(build_tree([6, 2, 9, 1, 4]))) == [6, 9, 2, None, None, 4, 1]
assert to_level_order(s.invertTree(build_tree([1, None, 2]))) == [1, 2]
assert s.invertTree(build_tree([])) is None
assert to_level_order(s.invertTree(build_tree([1]))) == [1]
assert to_level_order(s.invertTree(build_tree([4, 2, 7, 1, 3, 6, 9]))) == [4, 7, 2, 9, 6, 3, 1]
assert to_level_order(s.invertTree(build_tree([2, 1, 3]))) == [2, 3, 1]
"""
