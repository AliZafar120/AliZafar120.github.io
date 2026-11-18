PROBLEM = {
    "slug": "merge-k-sorted-lists", "number": 23, "title": "Merge k Sorted Lists", "category": "Linked List", "difficulty": "Hard",
    "url": "https://leetcode.com/problems/merge-k-sorted-lists/", "premium": False,
    "statement_html": """<p>You are given a list of <code>k</code> linked lists, each sorted in non-decreasing order. Merge all of them into a single sorted linked list, reusing the existing nodes, and return its head. Some of the <code>k</code> lists may be empty, and <code>k</code> itself may be zero.</p>
<pre>
Input:  lists = [1 -> 5 -> 9,  2 -> 3,  4 -> 8 -> 10]
Output: 1 -> 2 -> 3 -> 4 -> 5 -> 8 -> 9 -> 10

Input:  lists = [(empty), (empty)]
Output: (empty)
</pre>
<ul>
  <li>0 &le; k &le; 10<sup>4</sup>, total number of nodes &le; 10<sup>4</sup></li>
  <li>-10<sup>4</sup> &le; Node.val &le; 10<sup>4</sup>, each list is sorted</li>
</ul>""",
    "intro_html": """<p><strong>A min-heap of list fronts.</strong> At any moment the next output node must be the smallest of the <code>k</code> current front nodes. A heap answers \"which front is smallest\" in O(log k) instead of scanning all <code>k</code>. We seed the heap with the head of every non-empty list, then repeatedly pop the minimum, append it to the output, and push that node's successor. A dummy head keeps the appending code uniform.</p>""",
    "blocks": [
        {"code": "import heapq\nfrom typing import List, Optional\n\nclass Solution:\n    def mergeKLists(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:",
         "explain": "<p>LeetCode calls <code>mergeKLists</code> with a Python list of heads and expects one merged head. <code>heapq</code> is the standard library's binary min-heap operating on a plain list.</p>",
         "diagram": None},
        {"code": "        heap = []\n        for i, node in enumerate(lists):\n            if node:\n                heapq.heappush(heap, (node.val, i, node))",
         "explain": "<p>Seed the heap with the front of every non-empty list. Each entry is a tuple <code>(val, i, node)</code>. Tuples compare element by element, so the heap orders by <code>val</code> first. <strong>The index <code>i</code> is essential:</strong> when two values tie, Python would move on to compare the third element, and <code>ListNode</code> objects do not support <code>&lt;</code>, which raises <code>TypeError</code>. The list index is always unique, so the comparison is settled before it ever reaches the node.</p>",
         "diagram": "  lists[0] = 1 -> 5 -> 9\n  lists[1] = 2 -> 3\n  lists[2] = 4 -> 8 -> 10\n\n  heap = [(1, 0, n1), (2, 1, n2), (4, 2, n4)]\n\n  with ties, e.g. (3, 0, nodeA) vs (3, 1, nodeB):\n  3 == 3 -> compare 0 < 1 -> settled, nodes never compared"},
        {"code": "        dummy = ListNode()\n        tail = dummy",
         "explain": "<p>Dummy head pattern: <code>tail</code> always points at the last node of the merged output. Starting from a placeholder means the first real node is appended with the same <code>tail.next = node</code> as all the rest.</p>",
         "diagram": "  dummy -> None\n  tail = dummy"},
        {"code": "        while heap:\n            val, i, node = heapq.heappop(heap)",
         "explain": "<p>While any list still has nodes, pop the smallest front. Because every list is individually sorted and the heap holds exactly one front per non-exhausted list, this node is the global minimum of everything not yet output. Unpacking the tuple gives us back the index so we can reuse it when we push the successor.</p>",
         "diagram": "  heap = [(1,0,n1), (2,1,n2), (4,2,n4)]  ->  pop (1, 0, n1)"},
        {"code": "            tail.next = node\n            tail = node",
         "explain": "<p>Link the popped node onto the output and advance <code>tail</code>. The node's own <code>next</code> still points into its original list for now; it will be overwritten on the next iteration or set to <code>None</code> naturally when it is the last node overall.</p>",
         "diagram": "  dummy -> 1\n           tail"},
        {"code": "            if node.next:\n                heapq.heappush(heap, (node.next.val, i, node.next))",
         "explain": "<p>Replace the consumed front with the next node of the <em>same</em> list, carrying the same index <code>i</code>. If that list is now exhausted we push nothing, and the heap shrinks by one. The heap therefore never holds more than <code>k</code> entries, which bounds every operation at O(log k).</p>",
         "diagram": "  pop (1,0,n1): push (5,0,n5)   heap=[(2,1),(4,2),(5,0)]  out: 1\n  pop (2,1,n2): push (3,1,n3)   heap=[(3,1),(4,2),(5,0)]  out: 1 2\n  pop (3,1,n3): list 1 done     heap=[(4,2),(5,0)]        out: 1 2 3\n  pop (4,2,n4): push (8,2,n8)   heap=[(5,0),(8,2)]        out: 1 2 3 4\n  pop (5,0,n5): push (9,0,n9)   heap=[(8,2),(9,0)]        ...\n  pop 8, pop 9, pop 10          heap=[]   out: 1 2 3 4 5 8 9 10"},
        {"code": "        return dummy.next",
         "explain": "<p>Skip the placeholder and return the first real node. When every input list was empty the heap started empty, the loop never ran, and we return <code>None</code>.</p>",
         "diagram": None},
    ],
    "complexity": "Time O(N log k) where N is the total number of nodes and k the number of lists: each node is pushed and popped once at O(log k). Space O(k) for the heap.",
}

TESTS = """
s = Solution()
assert to_list(s.mergeKLists([build_list([1, 5, 9]), build_list([2, 3]), build_list([4, 8, 10])])) == [1, 2, 3, 4, 5, 8, 9, 10]
assert s.mergeKLists([None, None]) is None
assert s.mergeKLists([]) is None
assert to_list(s.mergeKLists([build_list([7])])) == [7]
assert to_list(s.mergeKLists([None, build_list([1, 2]), None])) == [1, 2]
assert to_list(s.mergeKLists([build_list([3, 3]), build_list([3]), build_list([3, 3, 3])])) == [3, 3, 3, 3, 3, 3]
assert to_list(s.mergeKLists([build_list([-2, 4]), build_list([-5, 0, 6]), build_list([1])])) == [-5, -2, 0, 1, 4, 6]
"""
