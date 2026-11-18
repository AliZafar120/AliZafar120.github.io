PROBLEM = {
    "slug": "lowest-common-ancestor-of-a-binary-search-tree", "number": 235, "title": "Lowest Common Ancestor of a Binary Search Tree", "category": "Tree", "difficulty": "Medium",
    "url": "https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-search-tree/", "premium": False,
    "statement_html": """<p>Given the root of a binary search tree and two nodes <code>p</code> and <code>q</code> that both exist in it, return their lowest common ancestor: the deepest node that has both <code>p</code> and <code>q</code> in its subtree. A node counts as its own ancestor, so if <code>p</code> is above <code>q</code> the answer is <code>p</code> itself.</p>
<pre>
Input:  root = [8, 3, 12, 1, 6, 10, 14],  p = 1,  q = 6
            8
           / \\
          3   12
         / \\  / \\
        1  6 10 14
Output: 3             1 and 6 are on different sides of 3

Input:  root = [8, 3, 12, 1, 6, 10, 14],  p = 3,  q = 1
Output: 3             3 is an ancestor of 1, so it is its own LCA
</pre>
<ul>
  <li>2 &le; number of nodes &le; 10<sup>5</sup>, all values distinct</li>
  <li><code>p != q</code> and both exist in the tree</li>
</ul>""",
    "intro_html": """<p><strong>Walk down from the root using the BST order.</strong> At any node, if both targets are smaller the LCA must be in the left subtree; if both are larger it is in the right subtree. The first node where the targets split, one on each side or one equal to the node itself, is the LCA. No recursion or parent pointers are needed, just a single downward walk.</p>""",
    "blocks": [
        {"code": "class Solution:\n    def lowestCommonAncestor(self, root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':",
         "explain": "<p>LeetCode's template passes the actual node objects for <code>p</code> and <code>q</code>, not their values, and expects a node back. The quoted type hints match the template; the grader supplies <code>TreeNode</code>.</p>",
         "diagram": None},
        {"code": "        node = root",
         "explain": "<p>A cursor that starts at the root. We will move it down one level per step; we never need to go back up because the decision at each level is final.</p>",
         "diagram": "            8          p = 1, q = 6\n           / \\\\\n          3   12       node = 8\n         / \\\\  / \\\\\n        1  6 10 14"},
        {"code": "        while node:",
         "explain": "<p>Keep descending while there is a node. Since <code>p</code> and <code>q</code> are guaranteed to exist, the loop always returns from inside before falling off the tree; the condition is a safety net.</p>",
         "diagram": None},
        {"code": "            if p.val < node.val and q.val < node.val:\n                node = node.left",
         "explain": "<p>Both targets are smaller than the current value, so by the BST property both live in the left subtree, and so does every common ancestor below this node. Move left.</p>",
         "diagram": "  node = 8: p.val=1 < 8 and q.val=6 < 8  -> go left\n  node = 3"},
        {"code": "            elif p.val > node.val and q.val > node.val:\n                node = node.right",
         "explain": "<p>The mirror case: both targets are larger, so both are in the right subtree. Move right.</p>",
         "diagram": "  if instead p = 10, q = 14:\n  node = 8: 10 > 8 and 14 > 8 -> go right\n  node = 12: 10 < 12 but 14 > 12 -> split, answer 12"},
        {"code": "            else:\n                return node",
         "explain": "<p>The targets are no longer on the same side: one is left and one is right, or one of them <em>is</em> this node. Either way no deeper node can contain both, so this is the lowest common ancestor.</p>",
         "diagram": "  p = 1, q = 6:\n  node = 3: 1 < 3 but 6 > 3  -> split -> return 3\n\n  p = 3, q = 1:\n  node = 8: both < 8 -> go left\n  node = 3: p.val == node.val, neither branch fires -> return 3"},
    ],
    "complexity": "Time O(h), one walk down the tree. Space O(1).",
}

TESTS = """
def find(node, val):
    while node and node.val != val:
        node = node.left if val < node.val else node.right
    return node

s = Solution()
t = build_tree([8, 3, 12, 1, 6, 10, 14])
assert s.lowestCommonAncestor(t, find(t, 1), find(t, 6)) is find(t, 3)
assert s.lowestCommonAncestor(t, find(t, 3), find(t, 1)) is find(t, 3)
assert s.lowestCommonAncestor(t, find(t, 10), find(t, 14)) is find(t, 12)
assert s.lowestCommonAncestor(t, find(t, 1), find(t, 14)) is find(t, 8)
assert s.lowestCommonAncestor(t, find(t, 6), find(t, 3)).val == 3
t2 = build_tree([2, 1])
assert s.lowestCommonAncestor(t2, find(t2, 2), find(t2, 1)) is find(t2, 2)
t3 = build_tree([6, 2, 8, 0, 4, 7, 9, None, None, 3, 5])
assert s.lowestCommonAncestor(t3, find(t3, 2), find(t3, 8)).val == 6
assert s.lowestCommonAncestor(t3, find(t3, 3), find(t3, 5)).val == 4
"""
