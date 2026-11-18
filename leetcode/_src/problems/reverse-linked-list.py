PROBLEM = {
    "slug": "reverse-linked-list", "number": 206, "title": "Reverse Linked List", "category": "Linked List", "difficulty": "Easy",
    "url": "https://leetcode.com/problems/reverse-linked-list/", "premium": False,
    "statement_html": """<p>Given the head of a singly linked list, reverse the list in place and return the new head. Each node has a <code>val</code> and a <code>next</code> pointer; you must rewire the pointers rather than build a new list of copied values.</p>
<pre>
Input:  head = 4 -> 7 -> 1 -> 9
Output: 9 -> 1 -> 7 -> 4

Input:  head = (empty)
Output: (empty)
</pre>
<ul>
  <li>0 &le; number of nodes &le; 5000</li>
  <li>-5000 &le; Node.val &le; 5000</li>
</ul>""",
    "intro_html": """<p><strong>Iterative pointer reversal with two cursors.</strong> Walk the list once, carrying <code>prev</code> (the already reversed part) and <code>cur</code> (the node we are about to flip). At each step we save <code>cur.next</code>, point <code>cur</code> backwards at <code>prev</code>, and advance both cursors. When <code>cur</code> falls off the end, <code>prev</code> is the new head.</p>""",
    "blocks": [
        {"code": "from typing import Optional\n\nclass Solution:\n    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:",
         "explain": "<p>LeetCode calls <code>reverseList</code> with the head node (or <code>None</code> for an empty list) and expects the head of the reversed list. <code>ListNode</code> is provided by the grader.</p>",
         "diagram": None},
        {"code": "        prev = None\n        cur = head",
         "explain": "<p>Two cursors. <code>prev</code> is the head of the reversed portion built so far, which starts out empty. <code>cur</code> is the first node still in original order. Starting <code>prev</code> at <code>None</code> is what gives the old head its terminating <code>None</code> once it becomes the tail.</p>",
         "diagram": "  prev = None\n  cur\n   |\n   4 -> 7 -> 1 -> 9 -> None"},
        {"code": "        while cur:",
         "explain": "<p>Keep going while there is a node left to flip. Every node passes through <code>cur</code> exactly once, so this is a single linear pass.</p>",
         "diagram": None},
        {"code": "            nxt = cur.next",
         "explain": "<p>Save the rest of the list before we overwrite <code>cur.next</code>. This is the one step people forget: once we point <code>cur</code> backwards, its old forward link is gone, and <code>nxt</code> is the only way to reach the remaining nodes.</p>",
         "diagram": "  prev = None\n  cur  nxt\n   |    |\n   4 -> 7 -> 1 -> 9 -> None"},
        {"code": "            cur.next = prev",
         "explain": "<p>The actual reversal: the current node now points at the part of the list that is already reversed. On the first iteration that is <code>None</code>, so the old head correctly becomes the new tail.</p>",
         "diagram": "          cur  nxt\n           |    |\n  None <-  4    7 -> 1 -> 9 -> None\n  prev"},
        {"code": "            prev = cur\n            cur = nxt",
         "explain": "<p>Advance both cursors one step to the right. <code>prev</code> now heads a reversed list that is one node longer, and <code>cur</code> resumes at the node we saved. The two sub-lists never share a node, so nothing is lost.</p>",
         "diagram": "  after step 1:  None <- 4    7 -> 1 -> 9 -> None\n                       prev  cur\n  after step 2:  None <- 4 <- 7    1 -> 9 -> None\n                            prev  cur\n  after step 3:  None <- 4 <- 7 <- 1    9 -> None\n                                 prev  cur\n  after step 4:  None <- 4 <- 7 <- 1 <- 9    None\n                                      prev  cur"},
        {"code": "        return prev",
         "explain": "<p>When <code>cur</code> is <code>None</code> every node has been flipped and <code>prev</code> sits on the last original node, which is the new head. For an empty list the loop never runs and we return <code>None</code>, as required.</p>",
         "diagram": "  prev = 9 -> 1 -> 7 -> 4 -> None"},
    ],
    "complexity": "Time O(n), one pass over the list. Space O(1), only two or three pointers regardless of length.",
}

TESTS = """
s = Solution()
assert to_list(s.reverseList(build_list([4, 7, 1, 9]))) == [9, 1, 7, 4]
assert s.reverseList(None) is None
assert to_list(s.reverseList(build_list([3]))) == [3]
assert to_list(s.reverseList(build_list([1, 2]))) == [2, 1]
assert to_list(s.reverseList(build_list([1, 2, 3, 4, 5]))) == [5, 4, 3, 2, 1]
h = build_list([10, 20, 30]); third = h.next.next
r = s.reverseList(h)
assert r is third and to_list(r) == [30, 20, 10] and h.next is None
"""
