PROBLEM = {
    "slug": "merge-two-sorted-lists", "number": 21, "title": "Merge Two Sorted Lists", "category": "Linked List", "difficulty": "Easy",
    "url": "https://leetcode.com/problems/merge-two-sorted-lists/", "premium": False,
    "statement_html": """<p>You are given the heads of two linked lists whose values are each in non-decreasing order. Splice the existing nodes together into one sorted list and return its head. Do not allocate new nodes for the values; reuse the ones you are given.</p>
<pre>
Input:  list1 = 1 -> 4 -> 6,  list2 = 2 -> 3 -> 7 -> 8
Output: 1 -> 2 -> 3 -> 4 -> 6 -> 7 -> 8

Input:  list1 = (empty),  list2 = 5
Output: 5
</pre>
<ul>
  <li>0 &le; nodes in each list &le; 50</li>
  <li>-100 &le; Node.val &le; 100, each list is already sorted</li>
</ul>""",
    "intro_html": """<p><strong>Two pointers with a dummy head.</strong> Keep a cursor on the front of each list and repeatedly attach the smaller front node to the end of the output. A throwaway <code>dummy</code> node sits in front of the result so that the first real node is appended with exactly the same code as every other node, with no special case for an empty result. When one list is exhausted the other is already sorted, so we attach it whole.</p>""",
    "blocks": [
        {"code": "from typing import Optional\n\nclass Solution:\n    def mergeTwoLists(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:",
         "explain": "<p>LeetCode calls <code>mergeTwoLists</code> with two heads, either of which may be <code>None</code>, and expects the head of the merged list.</p>",
         "diagram": None},
        {"code": "        dummy = ListNode()\n        tail = dummy",
         "explain": "<p>The <strong>dummy head</strong> trick. <code>dummy</code> is a placeholder node whose <code>next</code> will become the answer. <code>tail</code> always points at the last node of the merged list so far. Because <code>tail</code> starts at a real node, we can write <code>tail.next = ...</code> immediately without first asking \"is the result still empty?\".</p>",
         "diagram": "  dummy -> None          list1: 1 -> 4 -> 6\n  tail = dummy           list2: 2 -> 3 -> 7 -> 8"},
        {"code": "        while list1 and list2:",
         "explain": "<p>While both lists still have nodes, we must compare their fronts to decide which comes next. As soon as one list runs out, comparison is no longer needed.</p>",
         "diagram": None},
        {"code": "            if list1.val <= list2.val:\n                tail.next = list1\n                list1 = list1.next",
         "explain": "<p>If <code>list1</code>'s front is smaller or equal, link it onto the result and advance <code>list1</code>. Using <code>&lt;=</code> rather than <code>&lt;</code> takes from <code>list1</code> on ties, which keeps the merge stable (equal values keep their original relative order).</p>",
         "diagram": "  1 <= 2:  dummy -> 1          list1: 4 -> 6\n                    tail?      list2: 2 -> 3 -> 7 -> 8"},
        {"code": "            else:\n                tail.next = list2\n                list2 = list2.next",
         "explain": "<p>Otherwise <code>list2</code>'s front is strictly smaller: link it and advance <code>list2</code>. Only the chosen list moves; the other list's front stays put to be compared again next round.</p>",
         "diagram": "  4 > 2:   dummy -> 1 -> 2     list1: 4 -> 6\n                                list2: 3 -> 7 -> 8\n  4 > 3:   dummy -> 1 -> 2 -> 3\n                                list2: 7 -> 8"},
        {"code": "            tail = tail.next",
         "explain": "<p>Whichever node we just attached is now the end of the merged list, so move <code>tail</code> onto it. This single line serves both branches, which is why it sits after the <code>if/else</code>.</p>",
         "diagram": "  dummy -> 1 -> 2 -> 3 -> 4 -> 6\n                                tail\n  list1: None       list2: 7 -> 8"},
        {"code": "        tail.next = list1 or list2",
         "explain": "<p>At least one list is now empty. The other one (if any) is already sorted and every value in it is at least as large as <code>tail</code>, so we attach the whole remainder in one assignment instead of looping. <code>list1 or list2</code> picks whichever is not <code>None</code>; if both are <code>None</code> it correctly assigns <code>None</code>.</p>",
         "diagram": "  list1 or list2  ->  7 -> 8\n  dummy -> 1 -> 2 -> 3 -> 4 -> 6 -> 7 -> 8"},
        {"code": "        return dummy.next",
         "explain": "<p>Skip the placeholder and return the first real node. If both inputs were empty, <code>dummy.next</code> is still <code>None</code>, which is the right answer.</p>",
         "diagram": "  return 1 -> 2 -> 3 -> 4 -> 6 -> 7 -> 8"},
    ],
    "complexity": "Time O(n + m), each node is linked once. Space O(1): only the dummy node and two cursors are allocated, the input nodes are reused.",
}

TESTS = """
s = Solution()
assert to_list(s.mergeTwoLists(build_list([1, 4, 6]), build_list([2, 3, 7, 8]))) == [1, 2, 3, 4, 6, 7, 8]
assert to_list(s.mergeTwoLists(None, build_list([5]))) == [5]
assert s.mergeTwoLists(None, None) is None
assert to_list(s.mergeTwoLists(build_list([1, 2, 3]), None)) == [1, 2, 3]
assert to_list(s.mergeTwoLists(build_list([2, 2]), build_list([2, 2]))) == [2, 2, 2, 2]
assert to_list(s.mergeTwoLists(build_list([-3, 0, 9]), build_list([-5, 10]))) == [-5, -3, 0, 9, 10]
a = build_list([1, 3]); b = build_list([2]); a3 = a.next
m = s.mergeTwoLists(a, b)
assert m is a and m.next is b and m.next.next is a3 and a3.next is None
"""
