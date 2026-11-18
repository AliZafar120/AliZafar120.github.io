PROBLEM = {
    "slug": "linked-list-cycle", "number": 141, "title": "Linked List Cycle", "category": "Linked List", "difficulty": "Easy",
    "url": "https://leetcode.com/problems/linked-list-cycle/", "premium": False,
    "statement_html": """<p>Given the head of a singly linked list, decide whether following <code>next</code> pointers ever loops back to a node already visited. Return <code>true</code> if the list contains such a cycle and <code>false</code> if it ends in <code>None</code>. You may not modify the nodes and should aim for O(1) extra memory.</p>
<pre>
Input:  1 -> 2 -> 3 -> 4
             ^         |
             +---------+        (4.next points back to 2)
Output: true

Input:  5 -> 6 -> None
Output: false
</pre>
<ul>
  <li>0 &le; number of nodes &le; 10<sup>4</sup></li>
  <li>Node values are integers; they are not unique and are irrelevant to the answer</li>
</ul>""",
    "intro_html": """<p><strong>Floyd's tortoise and hare.</strong> Two pointers run along the list, one moving one node per step and the other two nodes per step. If the list ends, the fast pointer hits <code>None</code> and there is no cycle. If there is a cycle, both pointers eventually enter it and the fast one laps the slow one, so they land on the same node. This uses two pointers of memory instead of a visited set.</p>""",
    "blocks": [
        {"code": "from typing import Optional\n\nclass Solution:\n    def hasCycle(self, head: Optional[ListNode]) -> bool:",
         "explain": "<p>LeetCode calls <code>hasCycle</code> with the head of the list and expects a boolean. The grader supplies <code>ListNode</code> with <code>val</code> and <code>next</code>.</p>",
         "diagram": None},
        {"code": "        slow = fast = head",
         "explain": "<p>Both runners start on the head. If the list is empty, both are <code>None</code> and the loop below never runs. Starting them together is fine because we compare them only <em>after</em> moving, so the very first check cannot be a false positive.</p>",
         "diagram": "  slow, fast\n   |\n   1 -> 2 -> 3 -> 4\n        ^         |\n        +---------+"},
        {"code": "        while fast and fast.next:",
         "explain": "<p>The fast runner moves two steps, so before each step we need both <code>fast</code> and <code>fast.next</code> to exist. If either is <code>None</code> the list has an end, and a list with an end cannot contain a cycle. Checking only <code>fast</code> is enough because the slow runner is always behind it.</p>",
         "diagram": "  5 -> 6 -> None\n  fast = 5, fast.next = 6   -> step\n  fast = None               -> stop, no cycle"},
        {"code": "            slow = slow.next\n            fast = fast.next.next",
         "explain": "<p>Tortoise advances one, hare advances two. The gap between them grows by one node per iteration. Inside a cycle of length <code>L</code>, the gap taken modulo <code>L</code> cycles through every value, so it reaches 0 within <code>L</code> iterations after both are in the loop.</p>",
         "diagram": "  step 0: slow = 1, fast = 1\n  step 1: slow = 2, fast = 3\n  step 2: slow = 3, fast = 2   (fast went 3 -> 4 -> 2)\n  step 3: slow = 4, fast = 4   MEET"},
        {"code": "            if slow is fast:\n                return True",
         "explain": "<p>Compare node identity with <code>is</code>, not values with <code>==</code>, because different nodes can hold equal values. Two runners on the same node means the hare has lapped the tortoise, which is only possible if the list loops.</p>",
         "diagram": "  slow is fast  ->  both on node 4  ->  True"},
        {"code": "        return False",
         "explain": "<p>The loop exited because the hare ran off the end, so the list terminates and has no cycle. This also covers the empty list and the single node whose <code>next</code> is <code>None</code>.</p>",
         "diagram": None},
    ],
    "complexity": "Time O(n): the slow pointer takes at most n steps before the fast pointer either ends or meets it. Space O(1), two pointers.",
}

TESTS = """
s = Solution()

def cyclic(values, pos):
    head = build_list(values)
    if pos is None: return head
    tail = head
    while tail.next: tail = tail.next
    target = head
    for _ in range(pos): target = target.next
    tail.next = target
    return head

assert s.hasCycle(cyclic([1, 2, 3, 4], 1)) is True
assert s.hasCycle(build_list([5, 6])) is False
assert s.hasCycle(None) is False
assert s.hasCycle(build_list([7])) is False
assert s.hasCycle(cyclic([7], 0)) is True
assert s.hasCycle(cyclic([1, 2], 0)) is True
assert s.hasCycle(cyclic([1, 2, 3, 4, 5, 6], 5)) is True
assert s.hasCycle(cyclic([3, 3, 3, 3], None)) is False
"""
