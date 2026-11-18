PROBLEM = {
    "slug": "reorder-list", "number": 143, "title": "Reorder List", "category": "Linked List", "difficulty": "Medium",
    "url": "https://leetcode.com/problems/reorder-list/", "premium": False,
    "statement_html": """<p>Given the head of a singly linked list <code>L0 -&gt; L1 -&gt; ... -&gt; Ln</code>, rearrange its nodes in place into the order <code>L0 -&gt; Ln -&gt; L1 -&gt; Ln-1 -&gt; L2 -&gt; Ln-2 -&gt; ...</code>, alternating between the front and the back. Only pointers may be changed, not node values, and the method returns nothing.</p>
<pre>
Input:  head = 10 -> 20 -> 30 -> 40 -> 50
Output: 10 -> 50 -> 20 -> 40 -> 30

Input:  head = 1 -> 2 -> 3 -> 4
Output: 1 -> 4 -> 2 -> 3
</pre>
<ul>
  <li>1 &le; number of nodes &le; 5 * 10<sup>4</sup></li>
  <li>1 &le; Node.val &le; 1000</li>
</ul>""",
    "intro_html": """<p><strong>Split at the middle, reverse the back half, then interleave.</strong> Three classic linked list moves chained together: a slow/fast pointer pair finds the midpoint, the usual three-pointer loop reverses the second half so its last node comes first, and a final pass zips the two halves together one node at a time. All three steps are O(n) and use only a handful of pointers, so no extra array is needed.</p>""",
    "blocks": [
        {"code": "from typing import Optional\n\nclass Solution:\n    def reorderList(self, head: Optional[ListNode]) -> None:",
         "explain": "<p>LeetCode calls <code>reorderList</code> with the head and ignores the return value: the list must be modified in place, so the return type is <code>None</code>.</p>",
         "diagram": None},
        {"code": "        if not head or not head.next:\n            return",
         "explain": "<p>Lists with zero or one node are already in the required order. Returning early also means the midpoint search below can assume at least two nodes.</p>",
         "diagram": None},
        {"code": "        slow, fast = head, head.next\n        while fast and fast.next:\n            slow = slow.next\n            fast = fast.next.next",
         "explain": "<p>Find the end of the first half. <code>fast</code> moves two nodes for every one that <code>slow</code> moves, so when <code>fast</code> runs out, <code>slow</code> is halfway. Starting <code>fast</code> at <code>head.next</code> makes <code>slow</code> stop on the <em>last node of the first half</em> for both odd and even lengths, which is exactly where we want to cut.</p>",
         "diagram": "  10 -> 20 -> 30 -> 40 -> 50\n  start: slow = 10, fast = 20\n  step1: slow = 20, fast = 40\n  step2: slow = 30, fast = None  -> stop\n  first half ends at 30\n\n  1 -> 2 -> 3 -> 4:  slow = 1,2  fast = 2,4 -> slow = 2 (end of half)"},
        {"code": "        second = slow.next\n        slow.next = None",
         "explain": "<p>Cut the list in two. <code>second</code> is the head of the back half and the first half is terminated with <code>None</code> so the two pieces are fully independent. For odd lengths the first half keeps the extra middle node, which is where it belongs in the final order.</p>",
         "diagram": "  first:  10 -> 20 -> 30 -> None\n  second: 40 -> 50 -> None"},
        {"code": "        prev = None\n        while second:\n            nxt = second.next\n            second.next = prev\n            prev = second\n            second = nxt",
         "explain": "<p>Reverse the back half with the standard three-pointer loop: remember the next node, flip the current node's pointer to the already reversed part, and advance. Afterwards <code>prev</code> is the head of the reversed half, which starts with the original last node.</p>",
         "diagram": "  40 -> 50 -> None\n  step1: 40.next = None,  prev = 40, second = 50\n  step2: 50.next = 40,    prev = 50, second = None\n  reversed: 50 -> 40 -> None"},
        {"code": "        first, second = head, prev",
         "explain": "<p>Set up the two heads to be zipped: <code>first</code> walks the front half from the beginning, <code>second</code> walks the reversed back half. The back half is never longer than the front half, so <code>second</code> runs out first or at the same time.</p>",
         "diagram": "  first:  10 -> 20 -> 30 -> None\n  second: 50 -> 40 -> None"},
        {"code": "        while second:\n            tmp1, tmp2 = first.next, second.next\n            first.next = second\n            second.next = tmp1\n            first, second = tmp1, tmp2",
         "explain": "<p>Interleave. Save both successors before rewiring, then insert the <code>second</code> node right after the <code>first</code> node and link it onward to the rest of the front half. Finally step both cursors. Looping on <code>second</code> handles odd lengths: when the back half is exhausted the leftover middle node is already in place as the tail of the front half, with its <code>next</code> still <code>None</code>.</p>",
         "diagram": "  round 1: tmp1=20 tmp2=40    10 -> 50 -> 20 -> 30 -> None\n           first=20 second=40\n  round 2: tmp1=30 tmp2=None  10 -> 50 -> 20 -> 40 -> 30 -> None\n           first=30 second=None -> stop\n\n  result: 10 -> 50 -> 20 -> 40 -> 30"},
    ],
    "complexity": "Time O(n): three linear passes (find middle, reverse, interleave). Space O(1), only a fixed number of pointers.",
}

TESTS = """
s = Solution()
h = build_list([10, 20, 30, 40, 50]); s.reorderList(h); assert to_list(h) == [10, 50, 20, 40, 30]
h = build_list([1, 2, 3, 4]); s.reorderList(h); assert to_list(h) == [1, 4, 2, 3]
h = build_list([1]); s.reorderList(h); assert to_list(h) == [1]
h = build_list([1, 2]); s.reorderList(h); assert to_list(h) == [1, 2]
h = build_list([1, 2, 3]); s.reorderList(h); assert to_list(h) == [1, 3, 2]
h = build_list([1, 2, 3, 4, 5, 6]); s.reorderList(h); assert to_list(h) == [1, 6, 2, 5, 3, 4]
h = build_list([5, 5, 5, 5, 5]); s.reorderList(h); assert to_list(h) == [5, 5, 5, 5, 5]
assert s.reorderList(None) is None
"""
