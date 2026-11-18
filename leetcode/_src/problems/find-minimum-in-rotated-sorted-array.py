PROBLEM = {
    "slug": "find-minimum-in-rotated-sorted-array", "number": 153, "title": "Find Minimum in Rotated Sorted Array",
    "category": "Array", "difficulty": "Medium",
    "url": "https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/", "premium": False,
    "statement_html": """<p>A list of <em>distinct</em> integers was sorted in increasing order and then rotated: some prefix was cut off and appended to the end. For example <code>[1, 3, 5, 7, 9]</code> rotated by 3 becomes <code>[5, 7, 9, 1, 3]</code>. Given the rotated list, return its smallest element in O(log n) time.</p>
<pre>
Input:  nums = [5, 7, 9, 1, 3]
Output: 1

Input:  nums = [2, 4, 6]
Output: 2          rotated by 0, already sorted
</pre>
<ul>
  <li>1 &le; len(nums) &le; 5000, all values distinct</li>
  <li>The list was sorted ascending before rotation; O(log n) is required</li>
</ul>""",
    "intro_html": """<p><strong>Binary search on the rotation point.</strong> A rotated sorted list has two sorted halves, and the minimum is the first element of the second half. Comparing the middle element with the <em>last</em> element tells us which side the minimum is on: if the middle is bigger than the last, the drop happens to the right of the middle; otherwise the minimum is at the middle or to its left. Halving each time gives O(log n).</p>""",
    "blocks": [
        {"code": "from typing import List\n\nclass Solution:\n    def findMin(self, nums: List[int]) -> int:",
         "explain": "<p>LeetCode calls <code>findMin</code> with the rotated list and expects the minimum value, not its index.</p>",
         "diagram": None},
        {"code": "        lo, hi = 0, len(nums) - 1",
         "explain": "<p>The search window, inclusive on both ends. The invariant we will maintain: the minimum is always somewhere in <code>nums[lo..hi]</code>.</p>",
         "diagram": "  nums = [5, 7, 9, 1, 3]\n  index   0  1  2  3  4\n          lo          hi"},
        {"code": "        while lo < hi:",
         "explain": "<p>Keep shrinking until the window is a single element. Using <code>lo &lt; hi</code> rather than <code>&lt;=</code> is deliberate: when they meet we have the answer and must not look further.</p>",
         "diagram": None},
        {"code": "            mid = (lo + hi) // 2",
         "explain": "<p>The middle index, rounded down. Rounding down matters together with <code>hi = mid</code> below: it guarantees <code>mid &lt; hi</code> inside the loop, so the window always shrinks and the loop cannot spin.</p>",
         "diagram": "  lo=0, hi=4 -> mid=2   nums[mid]=9"},
        {"code": "            if nums[mid] > nums[hi]:\n                lo = mid + 1",
         "explain": "<p>If the middle value is larger than the last value, the list is not sorted between <code>mid</code> and <code>hi</code>, so the drop (and the minimum) lies strictly to the right of <code>mid</code>. The middle itself cannot be the minimum because something to its right is smaller.</p>",
         "diagram": "  [5, 7, 9, 1, 3]   nums[2]=9 > nums[4]=3\n   lo    mid   hi   -> minimum is right of mid -> lo = 3"},
        {"code": "            else:\n                hi = mid",
         "explain": "<p>Otherwise <code>nums[mid..hi]</code> is in sorted order, so nothing right of <code>mid</code> can be smaller than <code>nums[mid]</code>. The minimum is at <code>mid</code> or to its left; keep <code>mid</code> in the window since it may be the answer.</p>",
         "diagram": "  lo=3, hi=4 -> mid=3   nums[3]=1 <= nums[4]=3\n  [5, 7, 9, 1, 3]   -> hi = 3\n            lo hi\n  now lo == hi == 3, loop ends"},
        {"code": "        return nums[lo]",
         "explain": "<p>The window has collapsed to one index and the invariant says the minimum is inside it. For an unrotated list the first branch never fires and <code>hi</code> walks down to 0.</p>",
         "diagram": "  nums = [2, 4, 6]\n  lo=0 hi=2 mid=1: 4 <= 6 -> hi=1\n  lo=0 hi=1 mid=0: 2 <= 4 -> hi=0   -> nums[0] = 2"},
    ],
    "complexity": "Time O(log n), the window halves every step. Space O(1).",
}

TESTS = """
s = Solution()
assert s.findMin([5, 7, 9, 1, 3]) == 1
assert s.findMin([2, 4, 6]) == 2
assert s.findMin([8]) == 8
assert s.findMin([2, 1]) == 1
assert s.findMin([4, 5, 6, 7, 0, 1, 2]) == 0
assert s.findMin([3, 1, 2]) == 1
assert s.findMin([11, 13, 15, 17]) == 11
"""
