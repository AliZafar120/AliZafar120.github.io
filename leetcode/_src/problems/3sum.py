PROBLEM = {
    "slug": "3sum", "number": 15, "title": "3Sum", "category": "Array", "difficulty": "Medium",
    "url": "https://leetcode.com/problems/3sum/", "premium": False,
    "statement_html": """<p>Given a list of integers <code>nums</code>, return every distinct triple of values <code>[a, b, c]</code>, taken from three different positions, such that <code>a + b + c = 0</code>. Two triples with the same three values in a different order count as the same triple and must appear only once. The output order does not matter.</p>
<pre>
Input:  nums = [-3, 1, 2, -1, 0, 2]
Output: [[-3, 1, 2], [-1, 0, 1]]

Input:  nums = [1, 2, 3]
Output: []
</pre>
<ul>
  <li>3 &le; len(nums) &le; 3000, -10<sup>5</sup> &le; nums[i] &le; 10<sup>5</sup></li>
  <li>The result must not contain duplicate triples</li>
</ul>""",
    "intro_html": """<p><strong>Sort, then fix one element and run two pointers on the rest.</strong> After sorting, for each position <code>i</code> we look for two later elements that sum to <code>-nums[i]</code> by walking a left pointer and a right pointer towards each other: too small means move left up, too big means move right down. Sorting also puts equal values side by side, which lets us skip duplicates and guarantee unique triples. Total O(n&sup2;) instead of the O(n&sup3;) triple loop.</p>""",
    "blocks": [
        {"code": "from typing import List\n\nclass Solution:\n    def threeSum(self, nums: List[int]) -> List[List[int]]:",
         "explain": "<p>LeetCode calls <code>threeSum</code> with the list and expects a list of triples, in any order.</p>",
         "diagram": None},
        {"code": "        nums.sort()",
         "explain": "<p>Sorting is what makes the two-pointer walk valid (moving a pointer changes the sum in a predictable direction) and groups duplicate values together so we can skip them. O(n log n), cheaper than the O(n&sup2;) main loop.</p>",
         "diagram": "  nums = [-3, 1, 2, -1, 0, 2]\n  sorted: [-3, -1, 0, 1, 2, 2]\n  index    0   1  2  3  4  5"},
        {"code": "        result = []",
         "explain": "<p>Collects the triples. Each one is appended as <code>[nums[i], nums[lo], nums[hi]]</code>, which is in sorted order because the indices are increasing.</p>",
         "diagram": None},
        {"code": "        for i in range(len(nums) - 2):",
         "explain": "<p>Fix the first element of the triple. Stopping two short of the end leaves room for the other two elements to its right.</p>",
         "diagram": "  [-3, -1, 0, 1, 2, 2]\n    i                       first candidate nums[i] = -3"},
        {"code": "            if i > 0 and nums[i] == nums[i - 1]:\n                continue",
         "explain": "<p>Skip a first element equal to the previous one. Every triple starting with that value was already found when <code>i - 1</code> was the first element, so processing it again would only produce duplicates.</p>",
         "diagram": "  [-3, -1, -1, 0, 1, 1, 2]\n           i             nums[2] == nums[1] -> skip"},
        {"code": "            lo, hi = i + 1, len(nums) - 1",
         "explain": "<p>The two pointers for the remaining pair, starting at the opposite ends of the part of the list to the right of <code>i</code>.</p>",
         "diagram": "  [-3, -1, 0, 1, 2, 2]\n    i   lo          hi"},
        {"code": "            while lo < hi:\n                total = nums[i] + nums[lo] + nums[hi]",
         "explain": "<p>While the pointers have not crossed, compute the sum of the current candidate triple. The two pointers must be at different positions, hence strict <code>&lt;</code>.</p>",
         "diagram": "  i=0 (-3), lo=1 (-1), hi=5 (2):  total = -3 + -1 + 2 = -2"},
        {"code": "                if total < 0:\n                    lo += 1",
         "explain": "<p>The sum is too small. Because the list is sorted, moving <code>lo</code> right is the only move that can increase it. Moving <code>hi</code> left would only make it smaller.</p>",
         "diagram": "  total=-2 < 0  -> lo=2:  -3 + 0 + 2 = -1 < 0  -> lo=3\n  [-3, -1, 0, 1, 2, 2]\n    i         lo    hi"},
        {"code": "                elif total > 0:\n                    hi -= 1",
         "explain": "<p>The sum is too large, so shrink it by moving <code>hi</code> left onto a smaller value. Each step moves exactly one pointer, so the pair search is O(n) per <code>i</code>.</p>",
         "diagram": "  i=1 (-1), lo=2 (0), hi=5 (2):  -1 + 0 + 2 = 1 > 0 -> hi=4\n  lo=2, hi=4:                    -1 + 0 + 2 = 1 > 0 -> hi=3"},
        {"code": "                else:\n                    result.append([nums[i], nums[lo], nums[hi]])",
         "explain": "<p>Exactly zero: record the triple. We do not stop here, since other pairs further inside the window may also work with the same <code>nums[i]</code>.</p>",
         "diagram": "  i=0, lo=3, hi=5:  -3 + 1 + 2 = 0  -> append [-3, 1, 2]\n  i=1, lo=2, hi=3:  -1 + 0 + 1 = 0  -> append [-1, 0, 1]"},
        {"code": "                    lo += 1\n                    while lo < hi and nums[lo] == nums[lo - 1]:\n                        lo += 1",
         "explain": "<p>Advance past the value just used, and keep advancing while it repeats, so the same pair is not recorded twice. Only <code>lo</code> needs the skip: with <code>nums[i]</code> and <code>nums[lo]</code> fixed there is only one <code>nums[hi]</code> that sums to zero, so the next loop iteration will move <code>hi</code> on its own.</p>",
         "diagram": "  [-2, 0, 0, 0, 2, 2]  i=0: lo=1, hi=5 -> 0 -> append [-2, 0, 2]\n  lo=2: nums[2]==nums[1] -> lo=3: nums[3]==nums[2] -> lo=4\n  lo=4, hi=5: -2 + 2 + 2 = 2 > 0 -> hi=4, loop ends"},
        {"code": "        return result",
         "explain": "<p>Every zero-sum triple has been found exactly once. If nothing summed to zero the list is empty.</p>",
         "diagram": "  nums = [1, 2, 3]: every total is positive -> result = []"},
    ],
    "complexity": "Time O(n^2): O(n log n) sort plus an O(n) two-pointer walk for each of n first elements. Space O(1) extra beyond the output (sorting in place).",
}

TESTS = """
s = Solution()
def norm(ts): return sorted(sorted(t) for t in ts)
assert norm(s.threeSum([-3, 1, 2, -1, 0, 2])) == [[-3, 1, 2], [-1, 0, 1]]
assert s.threeSum([1, 2, 3]) == []
assert norm(s.threeSum([0, 0, 0])) == [[0, 0, 0]]
assert norm(s.threeSum([0, 0, 0, 0])) == [[0, 0, 0]]
assert norm(s.threeSum([-1, 0, 1, 2, -1, -4])) == [[-1, -1, 2], [-1, 0, 1]]
assert norm(s.threeSum([-2, 0, 0, 0, 2, 2])) == [[-2, 0, 2], [0, 0, 0]]
assert s.threeSum([5, -1, 3]) == []
"""
