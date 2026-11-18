PROBLEM = {
    "slug": "remove-nth-node-from-end-of-list", "number": 19, "title": "Remove Nth Node From End of List", "category": "Linked List", "difficulty": "Medium",
    "url": "https://leetcode.com/problems/remove-nth-node-from-end-of-list/", "premium": False,
    "statement_html": """<p>Given the head of a singly linked list and an integer <code>n</code>, delete the node that is <code>n</code>-th from the <em>end</em> (so <code>n = 1</code> removes the last node) and return the head of the resulting list. Try to do it in a single pass without first counting the length.</p>
<pre>
Input:  head = 3 -> 8 -> 2 -> 7 -> 5, n = 2
Output: 3 -> 8 -> 2 -> 5            (7 was 2nd from the end)

Input:  head = 6, n = 1
Output: (empty)
</pre>
<ul>
  <li>1 &le; number of nodes &le; 30</li>
  <li>1 &le; n &le; number of nodes, so the target always exists</li>
</ul>""",
    "intro_html": """<p><strong>Two pointers kept <code>n</code> nodes apart, starting from a dummy head.</strong> Send a <code>fast</code> pointer <code>n</code> steps ahead, then move <code>fast</code> and <code>slow</code> together until <code>fast</code> is on the last node. At that moment <code>slow</code> is just <em>before</em> the node to delete, so one pointer rewrite removes it. The dummy node in front of the head lets this work even when the node to delete is the head itself.</p>""",
    "blocks": [
        {"code": "from typing import Optional\n\nclass Solution:\n    def removeNthFromEnd(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:",
         "explain": "<p>LeetCode calls <code>removeNthFromEnd</code> with the head and <code>n</code>, and expects the new head. The grader provides <code>ListNode</code>.</p>",
         "diagram": None},
        {"code": "        dummy = ListNode(0, head)",
         "explain": "<p>A sentinel node placed before the real head. Deleting a node requires a pointer to the node <em>before</em> it, and when the head is the victim there is no such node. The dummy plays that role, so the deletion code needs no special case.</p>",
         "diagram": "  dummy -> 3 -> 8 -> 2 -> 7 -> 5 -> None        n = 2"},
        {"code": "        fast = slow = dummy",
         "explain": "<p>Both pointers begin at the dummy. We want <code>slow</code> to end up one node before the target, and starting it at the dummy (one node before the head) is what produces that offset.</p>",
         "diagram": "  fast, slow\n   |\n  dummy -> 3 -> 8 -> 2 -> 7 -> 5 -> None"},
        {"code": "        for _ in range(n):\n            fast = fast.next",
         "explain": "<p>Create a gap of exactly <code>n</code> nodes between the two pointers. The constraint <code>n &le; length</code> guarantees <code>fast</code> never runs past the end here.</p>",
         "diagram": "  after 2 steps:\n  slow         fast\n   |            |\n  dummy -> 3 -> 8 -> 2 -> 7 -> 5 -> None"},
        {"code": "        while fast.next:\n            fast = fast.next\n            slow = slow.next",
         "explain": "<p>Advance both pointers in lockstep until <code>fast</code> reaches the final node. Since the gap stays at <code>n</code>, when <code>fast</code> is on the last node (position <code>length</code>), <code>slow</code> is on position <code>length - n</code>, which is exactly the node before the <code>n</code>-th from the end.</p>",
         "diagram": "  step 1:   slow = 3, fast = 2\n  step 2:   slow = 8, fast = 7\n  step 3:   slow = 2, fast = 5   fast.next is None -> stop\n\n                      slow         fast\n                       |            |\n  dummy -> 3 -> 8 -> 2 -> 7 -> 5 -> None\n                          ^ target"},
        {"code": "        slow.next = slow.next.next",
         "explain": "<p>Unlink the target by making its predecessor skip over it. Nothing else references the removed node, so it is simply dropped. For the single node case <code>slow</code> is still the dummy and this sets <code>dummy.next</code> to <code>None</code>.</p>",
         "diagram": "  dummy -> 3 -> 8 -> 2 -+   7   +-> 5 -> None\n                        +---------+\n\n  head = 6, n = 1:  fast = 6, slow = dummy, loop skipped\n                    dummy.next = 6.next = None"},
        {"code": "        return dummy.next",
         "explain": "<p>Return whatever follows the dummy. Normally that is the original head; if the head itself was removed it is the second node, or <code>None</code> for a list that became empty.</p>",
         "diagram": "  return 3 -> 8 -> 2 -> 5"},
    ],
    "complexity": "Time O(L) for a list of length L, a single pass. Space O(1), two pointers and one dummy node.",
}

TESTS = """
s = Solution()
assert to_list(s.removeNthFromEnd(build_list([3, 8, 2, 7, 5]), 2)) == [3, 8, 2, 5]
assert s.removeNthFromEnd(build_list([6]), 1) is None
assert to_list(s.removeNthFromEnd(build_list([1, 2]), 2)) == [2]
assert to_list(s.removeNthFromEnd(build_list([1, 2]), 1)) == [1]
assert to_list(s.removeNthFromEnd(build_list([1, 2, 3, 4, 5]), 5)) == [2, 3, 4, 5]
assert to_list(s.removeNthFromEnd(build_list([1, 2, 3, 4, 5]), 1)) == [1, 2, 3, 4]
assert to_list(s.removeNthFromEnd(build_list([9, 9, 9]), 2)) == [9, 9]
"""
