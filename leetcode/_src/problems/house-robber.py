PROBLEM = {
    "slug": "house-robber", "number": 198, "title": "House Robber", "category": "Dynamic Programming", "difficulty": "Medium",
    "url": "https://leetcode.com/problems/house-robber/", "premium": False,
    "statement_html": """<p>A row of houses each holds some amount of cash. You may take the cash from any set of houses as long as no two chosen houses are next to each other (adjacent houses share an alarm). Return the largest total you can collect.</p>
<pre>
Input:  nums = [4, 1, 2, 9, 1]
Output: 13        houses 0 and 3: 4 + 9

Input:  nums = [6]
Output: 6
</pre>
<ul>
  <li>1 &le; len(nums) &le; 100</li>
  <li>0 &le; nums[i] &le; 400</li>
</ul>""",
    "intro_html": """<p><strong>Linear DP with two rolling values.</strong> For each house the best total up to that point is either the best total up to the previous house (skip this one) or this house's cash plus the best total up to the house two back (take this one). Only the last two results are ever needed, so two variables replace the whole table and the space drops to O(1).</p>""",
    "blocks": [
        {"code": "from typing import List\n\nclass Solution:\n    def rob(self, nums: List[int]) -> int:",
         "explain": "<p>The LeetCode signature: a list of non-negative cash amounts in, the best total out.</p>",
         "diagram": None},
        {"code": "        prev, cur = 0, 0",
         "explain": "<p><code>cur</code> is the best total using houses seen so far; <code>prev</code> is the best total using houses up to but excluding the most recent one. Before any house is seen both are 0: with nothing to rob, the best haul is nothing.</p>",
         "diagram": "  houses: [4, 1, 2, 9, 1]\n  before start:   prev = 0   cur = 0"},
        {"code": "        for x in nums:",
         "explain": "<p>Visit each house once, left to right. We only need its cash value, not its index, because the adjacency rule is encoded by which of the two running values we are allowed to add to.</p>",
         "diagram": "  x = 4,  x = 1,  x = 2,  x = 9,  x = 1"},
        {"code": "            prev, cur = cur, max(cur, prev + x)",
         "explain": "<p>Two choices for house <code>x</code>: <strong>skip</strong> it and keep <code>cur</code>, or <strong>rob</strong> it and add its cash to <code>prev</code>, the best total that does not include the neighbour just before. Take the larger. The window then slides forward: the old <code>cur</code> becomes the new <code>prev</code>. Python evaluates the right side first, so both reads see the old values.</p>",
         "diagram": "  nums = [4, 1, 2, 9, 1]\n  x=4:  max(0, 0+4)  = 4    prev=0  cur=4\n  x=1:  max(4, 0+1)  = 4    prev=4  cur=4\n  x=2:  max(4, 4+2)  = 6    prev=4  cur=6\n  x=9:  max(6, 4+9)  = 13   prev=6  cur=13\n  x=1:  max(13, 6+1) = 13   prev=13 cur=13"},
        {"code": "        return cur",
         "explain": "<p>After the last house, <code>cur</code> is the best total over the whole row. For a single house the loop runs once and returns its cash, so no special case is needed.</p>",
         "diagram": "  nums = [6]\n  x=6:  max(0, 0+6) = 6   -> return 6"},
    ],
    "complexity": "Time O(n), one pass. Space O(1), two integers.",
}

TESTS = """
s = Solution()
assert s.rob([4, 1, 2, 9, 1]) == 13
assert s.rob([6]) == 6
assert s.rob([1, 2, 3, 1]) == 4
assert s.rob([2, 7, 9, 3, 1]) == 12
assert s.rob([0, 0]) == 0
assert s.rob([2, 1, 1, 2]) == 4
"""
