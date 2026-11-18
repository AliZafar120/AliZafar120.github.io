PROBLEM = {
    "slug": "container-with-most-water", "number": 11, "title": "Container With Most Water",
    "category": "Array", "difficulty": "Medium",
    "url": "https://leetcode.com/problems/container-with-most-water/", "premium": False,
    "statement_html": """<p>You are given a list <code>height</code> of vertical wall heights standing at positions 0, 1, 2, ... along a line. Pick two walls; together with the ground they form a container whose capacity is the distance between them times the height of the <em>shorter</em> wall (water would spill over the shorter one). Return the largest capacity any pair of walls can hold.</p>
<pre>
Input:  height = [3, 9, 2, 7, 5]
Output: 15        walls at index 1 (9) and 4 (5): width 3, height 5

Input:  height = [2, 2]
Output: 2
</pre>
<ul>
  <li>2 &le; len(height) &le; 10<sup>5</sup>, 0 &le; height[i] &le; 10<sup>4</sup></li>
  <li>Walls cannot be tilted; the shorter wall sets the water level</li>
</ul>""",
    "intro_html": """<p><strong>Two pointers moving inwards from both ends.</strong> Start with the widest possible container and compute its area. Then move the pointer at the <em>shorter</em> wall inwards: keeping the shorter wall and narrowing the width can never produce a larger area, so that wall is finished and can be dropped. Repeat until the pointers meet. Every wall is dropped at most once, so the whole search is O(n) instead of O(n&sup2;).</p>""",
    "blocks": [
        {"code": "from typing import List\n\nclass Solution:\n    def maxArea(self, height: List[int]) -> int:",
         "explain": "<p>LeetCode calls <code>maxArea</code> with the list of wall heights and expects the best capacity as an integer.</p>",
         "diagram": None},
        {"code": "        left, right = 0, len(height) - 1",
         "explain": "<p>The two walls under consideration, starting at the two ends. This is the widest container possible, so any later container must make up for lost width with a taller limiting wall.</p>",
         "diagram": "  height = [3, 9, 2, 7, 5]\n  index     0  1  2  3  4\n           left        right"},
        {"code": "        best = 0",
         "explain": "<p>The largest area seen so far. Zero is a safe start since areas are never negative.</p>",
         "diagram": None},
        {"code": "        while left < right:",
         "explain": "<p>Continue while the two pointers still describe two different walls. Each iteration moves one pointer one step, so there are at most n - 1 iterations.</p>",
         "diagram": None},
        {"code": "            width = right - left\n            area = width * min(height[left], height[right])",
         "explain": "<p>The current container: its width is the index distance, and its water level is the shorter of the two walls, because water above that level spills out.</p>",
         "diagram": "  left=0 (3), right=4 (5):  width 4, level min(3,5)=3 -> area 12\n\n        9\n        |     7\n        |     |  5\n     3  |     |  |      water level 3 across width 4\n     |  |  2  |  |\n     0  1  2  3  4"},
        {"code": "            best = max(best, area)",
         "explain": "<p>Record the area if it beats the best so far. The answer is the maximum over all containers we evaluate.</p>",
         "diagram": "  step  left right  width  level  area  best\n   1     0    4      4      3     12    12\n   2     1    4      3      5     15    15\n   3     1    3      2      7     14    15\n   4     1    2      1      2      2    15"},
        {"code": "            if height[left] < height[right]:\n                left += 1\n            else:\n                right -= 1",
         "explain": "<p>Move the pointer at the shorter wall. Why is it safe to abandon that wall? Any other container using it would be narrower (the other pointer moves inwards) and its level could still not exceed this short wall, so it cannot beat the area we just measured. The taller wall, on the other hand, may yet pair well with something inside.</p>",
         "diagram": "  3 < 5  -> drop left wall (3):   left=1\n  9 >= 5 -> drop right wall (5):  right=3\n  9 >= 7 -> drop right wall (7):  right=2\n  9 >= 2 -> drop right wall (2):  right=1 -> left == right, stop"},
        {"code": "        return best",
         "explain": "<p>Every wall has been the limiting wall of exactly one measured container at the moment it was dropped, and the argument above shows none of the skipped pairs could do better.</p>",
         "diagram": "  height = [2, 2]: one container, width 1, level 2 -> 2"},
    ],
    "complexity": "Time O(n), each pointer moves at most n steps in total. Space O(1).",
}

TESTS = """
s = Solution()
assert s.maxArea([3, 9, 2, 7, 5]) == 15
assert s.maxArea([2, 2]) == 2
assert s.maxArea([1, 8, 6, 2, 5, 4, 8, 3, 7]) == 49
assert s.maxArea([0, 5]) == 0
assert s.maxArea([4, 4, 4, 4]) == 12
assert s.maxArea([1, 2, 1]) == 2
"""
