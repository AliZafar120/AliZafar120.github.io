PROBLEM = {
    "slug": "maximum-product-subarray", "number": 152, "title": "Maximum Product Subarray",
    "category": "Array", "difficulty": "Medium",
    "url": "https://leetcode.com/problems/maximum-product-subarray/", "premium": False,
    "statement_html": """<p>Given a list of integers <code>nums</code>, find the contiguous run of one or more elements whose product is as large as possible and return that product. Elements may be negative or zero, and the answer is guaranteed to fit in a 32-bit integer.</p>
<pre>
Input:  nums = [2, -3, -4, 0, 5]
Output: 24         the run [2, -3, -4]

Input:  nums = [-5, 0, -2]
Output: 0          any run containing the 0, or just [0]
</pre>
<ul>
  <li>1 &le; len(nums) &le; 2 * 10<sup>4</sup>, -10 &le; nums[i] &le; 10</li>
  <li>The run must contain at least one element</li>
</ul>""",
    "intro_html": """<p><strong>Kadane-style scan that tracks both the largest and the smallest product ending here.</strong> With sums a negative running total is simply dropped, but with products a very negative value is valuable: one more negative number turns it into a large positive. So at each position we keep the maximum and the minimum product of a run ending there, and when the current number is negative the two swap roles. The answer is the largest maximum seen.</p>""",
    "blocks": [
        {"code": "from typing import List\n\nclass Solution:\n    def maxProduct(self, nums: List[int]) -> int:",
         "explain": "<p>LeetCode calls <code>maxProduct</code> with the list and expects the best product as an integer.</p>",
         "diagram": None},
        {"code": "        best = nums[0]",
         "explain": "<p>The largest product of any run seen so far. It starts at the first element, not at 1 or 0, because an empty run is not allowed and the list could be a single negative number.</p>",
         "diagram": "  nums = [2, -3, -4, 0, 5]\n  best = 2"},
        {"code": "        cur_max = cur_min = nums[0]",
         "explain": "<p>Two running values for runs that end at the current element: the largest product and the smallest (most negative) product. We need both because the smallest can become the largest after one more negative factor.</p>",
         "diagram": "  cur_max = 2    cur_min = 2     (runs ending at index 0)"},
        {"code": "        for num in nums[1:]:",
         "explain": "<p>Scan the rest of the list. Each step only uses the two values from the previous position, so there is no table to store.</p>",
         "diagram": None},
        {"code": "            if num < 0:\n                cur_max, cur_min = cur_min, cur_max",
         "explain": "<p>Multiplying by a negative number flips the order: what was the biggest product becomes the smallest and vice versa. Swapping the two before multiplying means the next two lines can treat positive and negative numbers identically.</p>",
         "diagram": "  num = -3 < 0  -> swap:  cur_max=2, cur_min=2   (same here)\n  num = -4 < 0  -> swap:  cur_max=-6, cur_min=-3\n                          (the -6 is now the promising one)"},
        {"code": "            cur_max = max(num, cur_max * num)",
         "explain": "<p>Best product of a run ending at <code>num</code>: either extend the (possibly swapped) best run or start fresh at <code>num</code>. Starting fresh wins when the previous product was pulled down to 0 or below.</p>",
         "diagram": "  num   cur_max*num    num   -> cur_max\n  -3      2*-3=-6     -3       -3   (restart)\n  -4     -6*-4=24     -4       24   (extend)\n   0      24*0=0       0        0\n   5       0*5=0       5        5   (restart)"},
        {"code": "            cur_min = min(num, cur_min * num)",
         "explain": "<p>Same for the smallest product. It looks useless on its own, but it is the value that a later negative number will swap into <code>cur_max</code>. Here the -6 at index 1 is what produces the 24 at index 2.</p>",
         "diagram": "  num   cur_min*num    num   -> cur_min\n  -3      2*-3=-6     -3       -6\n  -4     -3*-4=12     -4       -4\n   0      -4*0=0       0        0\n   5       0*5=0       5        0"},
        {"code": "            best = max(best, cur_max)",
         "explain": "<p>Every run ends at some index, so the global answer is the largest <code>cur_max</code> across all positions. A zero resets both running values, which correctly splits the list into independent segments.</p>",
         "diagram": "  index:     0    1    2    3    4\n  num:       2   -3   -4    0    5\n  cur_max:   2   -3   24    0    5\n  cur_min:   2   -6   -4    0    0\n  best:      2    2   24   24   24   -> answer 24"},
        {"code": "        return best",
         "explain": "<p>Return the best product found. For <code>[-5, 0, -2]</code> the two negatives are separated by a zero, so they can never be in the same run and the answer is 0.</p>",
         "diagram": "  nums = [-5, 0, -2]\n  cur_max: -5   0   0       best: -5  0  0  -> answer 0"},
    ],
    "complexity": "Time O(n), one pass. Space O(1), three variables.",
}

TESTS = """
s = Solution()
assert s.maxProduct([2, -3, -4, 0, 5]) == 24
assert s.maxProduct([-5, 0, -2]) == 0
assert s.maxProduct([-7]) == -7
assert s.maxProduct([3, 3, 3]) == 27
assert s.maxProduct([2, 3, -2, 4]) == 6
assert s.maxProduct([-2, 3, -4]) == 24
assert s.maxProduct([-2, -3, 0, -1]) == 6
"""
