PROBLEM = {
    "slug": "construct-binary-tree-from-preorder-and-inorder-traversal", "number": 105, "title": "Construct Binary Tree from Preorder and Inorder Traversal", "category": "Tree", "difficulty": "Medium",
    "url": "https://leetcode.com/problems/construct-binary-tree-from-preorder-and-inorder-traversal/", "premium": False,
    "statement_html": """<p>You are given two lists describing the same binary tree: <code>preorder</code> lists the node values as visited root, left subtree, right subtree, and <code>inorder</code> lists them as left subtree, root, right subtree. All values are distinct. Rebuild the tree and return its root.</p>
<pre>
Input:  preorder = [6, 2, 1, 4, 8],  inorder = [1, 2, 4, 6, 8]
Output: [6, 2, 8, 1, 4]
            6
           / \\
          2   8
         / \\
        1   4

Input:  preorder = [1, 2],  inorder = [2, 1]
Output: [1, 2]        2 is before 1 in inorder, so 2 is a left child
</pre>
<ul>
  <li>1 &le; len(preorder) = len(inorder) &le; 3000</li>
  <li>All values are distinct, and both lists describe a valid tree</li>
</ul>""",
    "intro_html": """<p><strong>Preorder picks the root, inorder splits the children.</strong> The first unused preorder value is always the root of the subtree being built. Looking that value up in <code>inorder</code> tells us how many values lie to its left, and those are exactly the left subtree; everything after it is the right subtree. A hash map from value to inorder index makes the lookup O(1), and a single advancing pointer into <code>preorder</code> hands out roots in the right order, so the whole tree is built in linear time without slicing lists.</p>""",
    "blocks": [
        {"code": "from typing import List, Optional\n\nclass Solution:\n    def buildTree(self, preorder: List[int], inorder: List[int]) -> Optional[TreeNode]:",
         "explain": "<p>LeetCode calls <code>buildTree</code> with the two traversals and expects the root of the reconstructed tree.</p>",
         "diagram": None},
        {"code": "        index = {val: i for i, val in enumerate(inorder)}",
         "explain": "<p>Map each value to its position in <code>inorder</code>. Values are distinct, so the map is unambiguous. Without it we would scan <code>inorder</code> for every node, making the solution O(n&sup2;).</p>",
         "diagram": "  inorder = [1, 2, 4, 6, 8]\n  index   = {1:0, 2:1, 4:2, 6:3, 8:4}"},
        {"code": "        pre = 0",
         "explain": "<p>A cursor into <code>preorder</code>. Preorder visits a node before everything below it, so if we build nodes in the same order, the next root we need is always <code>preorder[pre]</code>. The cursor only ever moves forward.</p>",
         "diagram": "  preorder = [6, 2, 1, 4, 8]\n              ^ pre = 0"},
        {"code": "        def build(lo: int, hi: int) -> Optional[TreeNode]:\n            nonlocal pre\n            if lo > hi:\n                return None",
         "explain": "<p><code>build(lo, hi)</code> constructs the subtree whose values occupy <code>inorder[lo..hi]</code> inclusive. An empty range means no node there. <code>nonlocal pre</code> lets the helper advance the shared cursor.</p>",
         "diagram": "  build(0, 4)  -> whole tree, inorder[0..4] = [1, 2, 4, 6, 8]\n  build(3, 2)  -> lo > hi, empty -> None"},
        {"code": "            val = preorder[pre]\n            pre += 1\n            node = TreeNode(val)",
         "explain": "<p>The root of this range is the next preorder value. Consume it by moving the cursor, then create the node. Which range we are in does not affect which value we take; the recursion order guarantees it is the right one.</p>",
         "diagram": "  build(0, 4): val = preorder[0] = 6, pre -> 1, node 6\n    build(0, 2): val = preorder[1] = 2, pre -> 2, node 2\n      build(0, 0): val = preorder[2] = 1, pre -> 3, node 1\n      build(2, 2): val = preorder[3] = 4, pre -> 4, node 4\n    build(4, 4): val = preorder[4] = 8, pre -> 5, node 8"},
        {"code": "            mid = index[val]",
         "explain": "<p>Where does this root sit in <code>inorder</code>? Everything in <code>inorder[lo..mid-1]</code> was visited before it, so it belongs to the left subtree; <code>inorder[mid+1..hi]</code> belongs to the right.</p>",
         "diagram": "  root 6: mid = index[6] = 3\n  inorder = [1, 2, 4, 6, 8]\n             ^^^^^^^  ^  ^\n             left     6  right\n             [0..2]      [4..4]"},
        {"code": "            node.left = build(lo, mid - 1)\n            node.right = build(mid + 1, hi)",
         "explain": "<p>Build the left subtree <em>first</em>, then the right. This order matters: preorder lists the entire left subtree before the right one, so the cursor must hand out all left-subtree roots before any right-subtree root.</p>",
         "diagram": "  node 6: left = build(0, 2), right = build(4, 4)\n  node 2 (mid = 1): left = build(0, 0) -> 1,  right = build(2, 2) -> 4\n  node 8 (mid = 4): left = build(4, 3), right = build(5, 4), both None\n\n            6\n           / \\\\\n          2   8\n         / \\\\\n        1   4"},
        {"code": "            return node",
         "explain": "<p>Both children are attached; hand the finished subtree back to the parent.</p>",
         "diagram": None},
        {"code": "        return build(0, len(inorder) - 1)",
         "explain": "<p>Start with the full inorder range. The first preorder value becomes the overall root and the recursion fills in the rest.</p>",
         "diagram": "  preorder = [1, 2], inorder = [2, 1]\n  build(0, 1): root 1, mid = 1\n    left = build(0, 0) -> 2,  right = build(2, 1) -> None\n  result [1, 2]"},
    ],
    "complexity": "Time O(n), each node is created once with O(1) lookups. Space O(n) for the index map plus O(h) recursion stack.",
}

TESTS = """
s = Solution()
assert to_level_order(s.buildTree([6, 2, 1, 4, 8], [1, 2, 4, 6, 8])) == [6, 2, 8, 1, 4]
assert to_level_order(s.buildTree([1, 2], [2, 1])) == [1, 2]
assert to_level_order(s.buildTree([1, 2], [1, 2])) == [1, None, 2]
assert to_level_order(s.buildTree([3, 9, 20, 15, 7], [9, 3, 15, 20, 7])) == [3, 9, 20, None, None, 15, 7]
assert to_level_order(s.buildTree([-1], [-1])) == [-1]
assert to_level_order(s.buildTree([1, 2, 3, 4], [4, 3, 2, 1])) == [1, 2, None, 3, None, 4]
"""
