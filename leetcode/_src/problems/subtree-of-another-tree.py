PROBLEM = {
    "slug": "subtree-of-another-tree", "number": 572, "title": "Subtree of Another Tree", "category": "Tree", "difficulty": "Easy",
    "url": "https://leetcode.com/problems/subtree-of-another-tree/", "premium": False,
    "statement_html": """<p>Given the roots of two binary trees <code>root</code> and <code>subRoot</code>, decide whether <code>subRoot</code> appears somewhere inside <code>root</code> as a complete subtree: some node of <code>root</code>, together with <em>all</em> of its descendants, must be identical in shape and values to <code>subRoot</code>. A tree counts as a subtree of itself.</p>
<pre>
Input:  root = [8, 3, 10, 1, 6],  subRoot = [3, 1, 6]
            8
           / \\             3
          3   10          / \\
         / \\             1   6
        1   6
Output: true          the subtree rooted at 3 matches exactly

Input:  root = [8, 3, 10, 1, 6, null, null, null, 7],  subRoot = [3, 1, 6]
Output: false         node 1 now has a child 7, so the match is not exact
</pre>
<ul>
  <li>1 &le; nodes in root &le; 2000, 1 &le; nodes in subRoot &le; 1000</li>
  <li>-10<sup>4</sup> &le; Node.val &le; 10<sup>4</sup></li>
</ul>""",
    "intro_html": """<p><strong>Try every node as a candidate root and compare.</strong> Walk <code>root</code>; at each node, check with a <em>same-tree</em> comparison whether the subtree hanging there is identical to <code>subRoot</code>. If it is, we are done; otherwise recurse into the left and right children. This is two nested recursions: an outer one that picks the starting node and an inner one that verifies an exact match.</p>""",
    "blocks": [
        {"code": "from typing import Optional\n\nclass Solution:\n    def isSubtree(self, root: Optional[TreeNode], subRoot: Optional[TreeNode]) -> bool:",
         "explain": "<p>LeetCode calls <code>isSubtree</code> with the two roots. We will give <code>Solution</code> a second method for the exact comparison so each piece stays small.</p>",
         "diagram": None},
        {"code": "        if root is None:\n            return subRoot is None",
         "explain": "<p>Ran out of tree to search. An empty tree contains only the empty subtree, so the answer is whether <code>subRoot</code> is also empty. With LeetCode's guarantee of at least one node in <code>subRoot</code> this simply returns <code>False</code>.</p>",
         "diagram": "  isSubtree(None, [3, 1, 6]) -> False\n  (we walked below a leaf without finding a match)"},
        {"code": "        if self.isSameTree(root, subRoot):\n            return True",
         "explain": "<p>Does the subtree rooted <em>right here</em> match exactly? If so, stop. We check the current node before descending so the search is a preorder walk over candidate roots.</p>",
         "diagram": "  root tree:   8          subRoot:  3\n              / \\\\                 / \\\\\n             3   10               1   6\n            / \\\\\n           1   6\n  at 8: isSameTree(8-tree, 3-tree)? 8 != 3 -> no\n  at 3: isSameTree(3-tree, 3-tree)? yes -> True"},
        {"code": "        return self.isSubtree(root.left, subRoot) or self.isSubtree(root.right, subRoot)",
         "explain": "<p>No match at this node, so the match (if any) must be rooted somewhere in the left or right subtree. <code>or</code> short-circuits, so the right side is only searched if the left side fails.</p>",
         "diagram": "  isSubtree(8): no match at 8\n    isSubtree(3): match -> True\n  -> True (right side under 10 is never visited)"},
        {"code": "    def isSameTree(self, a: Optional[TreeNode], b: Optional[TreeNode]) -> bool:\n        if a is None or b is None:\n            return a is b",
         "explain": "<p>The exact comparison. If either tree is empty, they are the same only if both are: <code>a is b</code> is <code>True</code> exactly when both are <code>None</code>. This one line covers both the matching-leaves base case and the shape-mismatch case.</p>",
         "diagram": "  a = None, b = None  -> None is None -> True\n  a = 7,    b = None  -> 7 is None    -> False\n\n  second example: node 1 in root has a child 7, subRoot's 1 has none\n  isSameTree(7, None) -> False, so the 3-subtree does not match"},
        {"code": "        return a.val == b.val and self.isSameTree(a.left, b.left) and self.isSameTree(a.right, b.right)",
         "explain": "<p>Both nodes exist: their values must agree and both pairs of children must match recursively. The chained <code>and</code> stops at the first failure, so mismatched subtrees are rejected quickly.</p>",
         "diagram": "  isSameTree(3, 3): 3 == 3\n    isSameTree(1, 1): 1 == 1, children None/None -> True\n    isSameTree(6, 6): 6 == 6, children None/None -> True\n  -> True"},
    ],
    "complexity": "Time O(n * m) in the worst case, comparing subRoot (m nodes) against up to n candidate roots. Space O(h) for the recursion stack.",
}

TESTS = """
s = Solution()
assert s.isSubtree(build_tree([8, 3, 10, 1, 6]), build_tree([3, 1, 6])) is True
assert s.isSubtree(build_tree([8, 3, 10, 1, 6, None, None, None, 7]), build_tree([3, 1, 6])) is False
assert s.isSubtree(build_tree([3, 4, 5, 1, 2]), build_tree([4, 1, 2])) is True
assert s.isSubtree(build_tree([3, 4, 5, 1, 2, None, None, None, None, 0]), build_tree([4, 1, 2])) is False
assert s.isSubtree(build_tree([1]), build_tree([1])) is True
assert s.isSubtree(build_tree([1]), build_tree([2])) is False
assert s.isSubtree(build_tree([1, 2, 3]), build_tree([1, 2, 3])) is True
assert s.isSubtree(build_tree([1, 2, 3]), build_tree([3])) is True
"""
