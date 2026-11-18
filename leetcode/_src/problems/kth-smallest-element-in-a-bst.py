PROBLEM = {
    "slug": "kth-smallest-element-in-a-bst", "number": 230, "title": "Kth Smallest Element in a BST", "category": "Tree", "difficulty": "Medium",
    "url": "https://leetcode.com/problems/kth-smallest-element-in-a-bst/", "premium": False,
    "statement_html": """<p>Given the root of a binary search tree and an integer <code>k</code>, return the <code>k</code>-th smallest value in the tree, counting from 1. The BST property guarantees that an inorder traversal visits the values in increasing order.</p>
<pre>
Input:  root = [7, 3, 9, 1, 5],  k = 3
            7
           / \\
          3   9
         / \\
        1   5
Output: 5             sorted values are 1, 3, 5, 7, 9

Input:  root = [2, 1],  k = 1
Output: 1
</pre>
<ul>
  <li>1 &le; k &le; number of nodes &le; 10<sup>4</sup></li>
  <li>0 &le; Node.val &le; 10<sup>4</sup></li>
</ul>""",
    "intro_html": """<p><strong>Iterative inorder traversal with a stack, stopping early.</strong> Inorder on a BST yields values in sorted order, so the k-th value visited is the answer. Doing the traversal with an explicit stack instead of recursion lets us stop the moment we have popped <code>k</code> nodes, rather than visiting the whole tree. The stack holds the path of nodes whose left side has been explored but who have not themselves been visited yet.</p>""",
    "blocks": [
        {"code": "from typing import Optional\n\nclass Solution:\n    def kthSmallest(self, root: Optional[TreeNode], k: int) -> int:",
         "explain": "<p>LeetCode calls <code>kthSmallest</code> with the root and <code>k</code> and expects the value, not the node. The tree is guaranteed to have at least <code>k</code> nodes.</p>",
         "diagram": None},
        {"code": "        stack = []\n        node = root",
         "explain": "<p><code>stack</code> replaces the call stack of a recursive inorder walk. <code>node</code> is the cursor: the subtree we are about to dive into. Starting at the root with an empty stack mirrors the initial recursive call.</p>",
         "diagram": "  tree [7, 3, 9, 1, 5], k = 3\n  stack = []    node = 7"},
        {"code": "        while True:",
         "explain": "<p>Loop until we return from inside. Because <code>k</code> is at most the node count, the return is guaranteed to happen before the traversal runs out, so no separate exit condition is needed.</p>",
         "diagram": None},
        {"code": "            while node:\n                stack.append(node)\n                node = node.left",
         "explain": "<p>Go as far left as possible, pushing every node passed. The leftmost node is the smallest not yet visited, and everything pushed above it on the stack is waiting for its turn once its left side is done.</p>",
         "diagram": "  push 7, go left\n  push 3, go left\n  push 1, go left -> None\n  stack = [7, 3, 1]   (top is 1)"},
        {"code": "            node = stack.pop()\n            k -= 1",
         "explain": "<p>Pop the next node in sorted order and <em>visit</em> it: that is one more of the small values accounted for, so decrement <code>k</code>. Counting down rather than up saves a second variable.</p>",
         "diagram": "  pop 1 -> k = 2    stack = [7, 3]\n  pop 3 -> k = 1    stack = [7]\n  pop 5 -> k = 0    stack = [7]"},
        {"code": "            if k == 0:\n                return node.val",
         "explain": "<p>If this was the k-th pop, its value is the answer. Returning here is the early exit: in the example the right subtree under 9 is never touched.</p>",
         "diagram": "  k = 3: 1st pop = 1, 2nd pop = 3, 3rd pop = 5 -> return 5\n  node 7 and node 9 are never visited"},
        {"code": "            node = node.right",
         "explain": "<p>Not done yet, so continue with the right subtree of the node just visited. Its values are the next larger ones. The outer loop's left-dive then pushes that subtree's leftmost path; if the right child is <code>None</code> the dive does nothing and the next pop takes the parent waiting on the stack.</p>",
         "diagram": "  after pop 1: node = 1.right = None -> next pop is 3\n  after pop 3: node = 3.right = 5    -> push 5, pop 5\n  stack = [7]  at that moment"},
    ],
    "complexity": "Time O(h + k): the initial dive costs the height, then each of the k visits is amortised O(1). Space O(h) for the stack.",
}

TESTS = """
s = Solution()
assert s.kthSmallest(build_tree([7, 3, 9, 1, 5]), 3) == 5
assert s.kthSmallest(build_tree([2, 1]), 1) == 1
assert s.kthSmallest(build_tree([2, 1]), 2) == 2
assert s.kthSmallest(build_tree([5]), 1) == 5
assert s.kthSmallest(build_tree([3, 1, 4, None, 2]), 1) == 1
assert s.kthSmallest(build_tree([5, 3, 6, 2, 4, None, None, 1]), 3) == 3
assert s.kthSmallest(build_tree([7, 3, 9, 1, 5]), 5) == 9
assert s.kthSmallest(build_tree([1, None, 2, None, 3]), 3) == 3
"""
