PROBLEM = {
    "slug": "same-tree", "number": 100, "title": "Same Tree", "category": "Tree", "difficulty": "Easy",
    "url": "https://leetcode.com/problems/same-tree/", "premium": False,
    "statement_html": """<p>Given the roots of two binary trees <code>p</code> and <code>q</code>, decide whether the trees are identical: they must have exactly the same shape and every corresponding pair of nodes must hold the same value.</p>
<pre>
Input:  p = [4, 2, 7],  q = [4, 2, 7]
          4          4
         / \\        / \\
        2   7      2   7
Output: true

Input:  p = [4, 2],  q = [4, null, 2]
          4          4
         /            \\
        2              2
Output: false         same values, different shape
</pre>
<ul>
  <li>0 &le; number of nodes in each tree &le; 100</li>
  <li>-10<sup>4</sup> &le; Node.val &le; 10<sup>4</sup></li>
</ul>""",
    "intro_html": """<p><strong>Recurse on both trees in lockstep.</strong> Two trees are the same when their roots agree and their left subtrees are the same and their right subtrees are the same. The recursion walks both trees together; the moment one side has a node where the other has <code>None</code>, or two values differ, the answer is false and the comparison stops early.</p>""",
    "blocks": [
        {"code": "from typing import Optional\n\nclass Solution:\n    def isSameTree(self, p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:",
         "explain": "<p>LeetCode passes the two roots, either of which may be <code>None</code>. The method is recursive on itself, so the same function compares whole trees and tiny subtrees alike.</p>",
         "diagram": None},
        {"code": "        if p is None and q is None:\n            return True",
         "explain": "<p>Two empty trees are identical. This is the base case the recursion bottoms out on below every matching pair of leaves, and it also handles the input where both trees are empty.</p>",
         "diagram": "  p = None, q = None  -> True\n  (reached below every leaf of two matching trees)"},
        {"code": "        if p is None or q is None:\n            return False",
         "explain": "<p>Exactly one side is empty (we already handled both being empty), so the shapes differ at this spot. This is the check that catches <code>[4, 2]</code> versus <code>[4, null, 2]</code>.</p>",
         "diagram": "  p:   4        q:   4\n      /              \\\\\n     2                2\n  compare left children: p.left = 2, q.left = None -> False"},
        {"code": "        if p.val != q.val:\n            return False",
         "explain": "<p>Both nodes exist, so compare their values. A mismatch anywhere makes the trees different, and returning immediately avoids descending into subtrees that cannot change the answer.</p>",
         "diagram": "  p:   4        q:   4\n      / \\\\           / \\\\\n     2   7          2   9\n  at the right children: 7 != 9 -> False"},
        {"code": "        return self.isSameTree(p.left, q.left) and self.isSameTree(p.right, q.right)",
         "explain": "<p>Roots agree, so the trees are the same exactly when both pairs of subtrees are. Python's <code>and</code> short-circuits: if the left subtrees already differ, the right ones are never visited.</p>",
         "diagram": "  isSameTree(4, 4): 4 == 4\n    isSameTree(2, 2): 2 == 2\n      isSameTree(None, None) -> True\n      isSameTree(None, None) -> True   -> True\n    isSameTree(7, 7): 7 == 7\n      isSameTree(None, None) -> True\n      isSameTree(None, None) -> True   -> True\n  -> True and True = True"},
    ],
    "complexity": "Time O(min(n, m)), each pair of nodes is compared once and the walk stops at the first difference. Space O(h) for the recursion stack.",
}

TESTS = """
s = Solution()
assert s.isSameTree(build_tree([4, 2, 7]), build_tree([4, 2, 7])) is True
assert s.isSameTree(build_tree([4, 2]), build_tree([4, None, 2])) is False
assert s.isSameTree(build_tree([4, 2, 7]), build_tree([4, 2, 9])) is False
assert s.isSameTree(build_tree([]), build_tree([])) is True
assert s.isSameTree(build_tree([1]), build_tree([])) is False
assert s.isSameTree(build_tree([1]), build_tree([1])) is True
assert s.isSameTree(build_tree([1, 2, 3, 4]), build_tree([1, 2, 3, None, 4])) is False
"""
