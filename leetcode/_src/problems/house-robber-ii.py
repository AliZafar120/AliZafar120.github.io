PROBLEM = {
    "slug": "house-robber-ii", "number": 213, "title": "House Robber II", "category": "Dynamic Programming", "difficulty": "Medium",
    "url": "https://leetcode.com/problems/house-robber-ii/", "premium": False,
    "statement_html": """<p>Same setup as House Robber, but the houses stand in a circle, so the first and last houses are also neighbours and cannot both be robbed. Given the cash in each house, return the maximum total you can collect without robbing two adjacent houses.</p>
<pre>
Input:  nums = [6, 1, 1, 5]
Output: 7        houses 1 and 3: 1 + 5 (6 + 5 is not allowed, they are adjacent)

Input:  nums = [3]
Output: 3
</pre>
<ul>
  <li>1 &le; len(nums) &le; 100</li>
  <li>0 &le; nums[i] &le; 1000</li>
</ul>""",
    "intro_html": """<p><strong>Two linear passes.</strong> The circle only adds one rule: house 0 and house n-1 cannot both be taken. So any valid plan either leaves out the first house or leaves out the last one (or both). Run the ordinary linear House Robber DP once on <code>nums[1:]</code> and once on <code>nums[:-1]</code>, and return the better of the two. A single house is the one case where both slices are empty, so handle it first.</p>""",
    "blocks": [
        {"code": "from typing import List\n\nclass Solution:\n    def rob(self, nums: List[int]) -> int:",
         "explain": "<p>Same signature as the original House Robber. The circular arrangement is implied by the problem, not by the input.</p>",
         "diagram": None},
        {"code": "        if len(nums) == 1:\n            return nums[0]",
         "explain": "<p>With one house there is no neighbour to conflict with, and both slices used below would be empty and return 0, which is wrong. Take its cash directly.</p>",
         "diagram": "  nums = [3]  ->  3"},
        {"code": "        return max(self._rob_line(nums[1:]), self._rob_line(nums[:-1]))",
         "explain": "<p>Break the circle in the two possible ways. <code>nums[1:]</code> drops the first house, so the last house is free to be taken; <code>nums[:-1]</code> drops the last house, freeing the first. Each slice is an ordinary straight row. The best circular plan skips at least one of the two ends, so it is found by one of these calls.</p>",
         "diagram": "  nums = [6, 1, 1, 5]   (6 and 5 are neighbours in the circle)\n  drop first:  [1, 1, 5]  ->  line best = 6   (1 + 5)\n  drop last:   [6, 1, 1]  ->  line best = 7   (6 + 1)\n  max(6, 7) = 7"},
        {"code": "    def _rob_line(self, houses: List[int]) -> int:",
         "explain": "<p>A helper that solves the straight-row version. Keeping it separate avoids writing the DP twice and makes the two-pass idea visible at a glance.</p>",
         "diagram": None},
        {"code": "        prev, cur = 0, 0",
         "explain": "<p><code>cur</code> is the best total over the houses seen so far; <code>prev</code> is the best total excluding the most recent house. Both start at 0, which also makes an empty slice return 0 cleanly.</p>",
         "diagram": "  before start:   prev = 0   cur = 0"},
        {"code": "        for x in houses:\n            prev, cur = cur, max(cur, prev + x)",
         "explain": "<p>For each house, either skip it (keep <code>cur</code>) or rob it (add to <code>prev</code>, the best total that does not touch the neighbour just before). Then slide the window so the old <code>cur</code> becomes the new <code>prev</code>.</p>",
         "diagram": "  houses = [6, 1, 1]   (circle with last house removed)\n  x=6:  max(0, 0+6) = 6    prev=0  cur=6\n  x=1:  max(6, 0+1) = 6    prev=6  cur=6\n  x=1:  max(6, 6+1) = 7    prev=6  cur=7\n\n  houses = [1, 1, 5]   (circle with first house removed)\n  x=1:  max(0, 0+1) = 1    prev=0  cur=1\n  x=1:  max(1, 0+1) = 1    prev=1  cur=1\n  x=5:  max(1, 1+5) = 6    prev=1  cur=6"},
        {"code": "        return cur",
         "explain": "<p>The best total for this straight row. The caller compares the two rows and keeps the larger.</p>",
         "diagram": "  _rob_line([6, 1, 1]) = 7\n  _rob_line([1, 1, 5]) = 6     -> answer 7"},
    ],
    "complexity": "Time O(n): two linear passes. Space O(1) beyond the two slices (which could be avoided with index bounds).",
}

TESTS = """
s = Solution()
assert s.rob([6, 1, 1, 5]) == 7
assert s.rob([3]) == 3
assert s.rob([2, 3, 2]) == 3
assert s.rob([1, 2, 3, 1]) == 4
assert s.rob([1, 2, 3]) == 3
assert s.rob([5, 5]) == 5
assert s.rob([0, 0, 0]) == 0
assert s.rob([200, 3, 140, 20, 10]) == 340
"""
