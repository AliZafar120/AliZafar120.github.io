PROBLEM = {
    "slug": "maximum-subarray", "number": 53, "title": "Maximum Subarray", "category": "Array", "difficulty": "Medium",
    "url": "https://leetcode.com/problems/maximum-subarray/", "premium": False,
    "statement_html": """<p>Given a list of integers <code>nums</code>, find the contiguous run of one or more elements whose sum is as large as possible, and return that sum. The run must be consecutive in the original order; you cannot skip elements.</p>
<pre>
Input:  nums = [-3, 4, -1, 2, -5, 3]
Output: 5          the run [4, -1, 2]

Input:  nums = [-4, -2, -7]
Output: -2         a single element is a valid run
</pre>
<ul>
  <li>1 &le; len(nums) &le; 10<sup>5</sup>, -10<sup>4</sup> &le; nums[i] &le; 10<sup>4</sup></li>
  <li>The run must contain at least one element</li>
</ul>""",
    "intro_html": """<p><strong>Kadane's algorithm: a running sum that restarts when it turns negative.</strong> Scanning left to right, we track the best sum of a run that <em>ends at the current element</em>. That is either the element alone or the element added to the best run ending just before it, whichever is larger. A negative running sum can only hurt what follows, so the max naturally drops it. The global answer is the largest value this running sum ever takes.</p>""",
    "blocks": [
        {"code": "from typing import List\n\nclass Solution:\n    def maxSubArray(self, nums: List[int]) -> int:",
         "explain": "<p>LeetCode calls <code>maxSubArray</code> with the list and expects the best sum as an integer, not the run itself.</p>",
         "diagram": None},
        {"code": "        best = nums[0]",
         "explain": "<p>The best sum found anywhere so far. It starts at the first element rather than 0 because an empty run is not allowed: if every number is negative, the answer is the least negative one, and starting at 0 would wrongly return 0.</p>",
         "diagram": "  nums = [-3, 4, -1, 2, -5, 3]\n  best = -3"},
        {"code": "        current = nums[0]",
         "explain": "<p>The best sum of a run that ends exactly at the element we are looking at. For the first element that run is just the element itself.</p>",
         "diagram": "  current = -3     (best run ending at index 0)"},
        {"code": "        for num in nums[1:]:",
         "explain": "<p>Visit the remaining elements in order. Each step extends the picture by one position, using only the state from the position before it.</p>",
         "diagram": None},
        {"code": "            current = max(num, current + num)",
         "explain": "<p>The key decision. A run ending at <code>num</code> either extends the best run that ended just before (<code>current + num</code>) or starts fresh at <code>num</code>. Starting fresh wins exactly when <code>current</code> is negative, because carrying a negative sum forward can only lower the total.</p>",
         "diagram": "  num    current+num   num   -> current\n   4       -3+4=1       4        4   (restart)\n  -1        4-1=3      -1        3   (extend)\n   2        3+2=5       2        5   (extend)\n  -5        5-5=0      -5        0   (extend)\n   3        0+3=3       3        3   (either)"},
        {"code": "            best = max(best, current)",
         "explain": "<p>Every run ends <em>somewhere</em>, so the overall maximum is the largest &quot;best run ending here&quot; across all positions. We fold each new <code>current</code> into <code>best</code> as we go.</p>",
         "diagram": "  index:    0   1   2   3   4   5\n  num:     -3   4  -1   2  -5   3\n  current: -3   4   3   5   0   3\n  best:    -3   4   4   5   5   5   -> answer 5"},
        {"code": "        return best",
         "explain": "<p>After the pass <code>best</code> holds the maximum over every possible ending position, which covers every contiguous run.</p>",
         "diagram": "  nums = [-4, -2, -7]\n  current: -4  -2  -7       (each restart beats extending)\n  best:    -4  -2  -2       -> answer -2"},
    ],
    "complexity": "Time O(n), one pass. Space O(1).",
}

TESTS = """
s = Solution()
assert s.maxSubArray([-3, 4, -1, 2, -5, 3]) == 5
assert s.maxSubArray([-4, -2, -7]) == -2
assert s.maxSubArray([7]) == 7
assert s.maxSubArray([1, 1, 1, 1]) == 4
assert s.maxSubArray([-2, 1, -3, 4, -1, 2, 1, -5, 4]) == 6
assert s.maxSubArray([5, -9, 6]) == 6
"""
