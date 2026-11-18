PROBLEM = {
    "slug": "longest-increasing-subsequence", "number": 300, "title": "Longest Increasing Subsequence", "category": "Dynamic Programming", "difficulty": "Medium",
    "url": "https://leetcode.com/problems/longest-increasing-subsequence/", "premium": False,
    "statement_html": """<p>Given a list of integers, return the length of the longest subsequence whose values are strictly increasing. A subsequence keeps the original order but may skip elements. You only need the length, not the subsequence itself.</p>
<pre>
Input:  nums = [3, 1, 5, 2, 6, 4]
Output: 3        for example 1, 2, 4  or  3, 5, 6

Input:  nums = [9, 9, 9]
Output: 1        strictly increasing, so equal values do not chain
</pre>
<ul>
  <li>1 &le; len(nums) &le; 2500</li>
  <li>-10<sup>4</sup> &le; nums[i] &le; 10<sup>4</sup></li>
  <li>Follow-up: can you do better than O(n&sup2;)?</li>
</ul>""",
    "intro_html": """<p><strong>Patience sorting with binary search.</strong> We keep an array <code>tails</code> where <code>tails[i]</code> is the smallest possible last value of an increasing subsequence of length <code>i + 1</code>. That array is always sorted, so for each new number we binary-search the first tail that is <code>&ge;</code> it and overwrite it (a cheaper ending for the same length), or append if the number beats every tail (a longer subsequence). The final length of <code>tails</code> is the answer, in O(n log n) instead of the O(n&sup2;) classic DP.</p>""",
    "blocks": [
        {"code": "from bisect import bisect_left\nfrom typing import List\n\nclass Solution:\n    def lengthOfLIS(self, nums: List[int]) -> int:",
         "explain": "<p><code>bisect_left</code> from the standard library performs the binary search for us: given a sorted list and a value, it returns the leftmost index where the value could be inserted while keeping the list sorted. That is exactly \"the first element <code>&ge;</code> value\".</p>",
         "diagram": None},
        {"code": "        tails: List[int] = []",
         "explain": "<p>The core data structure. <code>tails[i]</code> stores the <em>smallest</em> value that can end an increasing subsequence of length <code>i + 1</code> seen so far. Smaller tails are better because they leave more room for future numbers to extend them. Note that <code>tails</code> is <strong>not</strong> itself a valid subsequence; it is a summary of the best endings for each length.</p>",
         "diagram": "  tails = []\n  index:     0        1        2\n  meaning:  best end  best end  best end\n            of len 1  of len 2  of len 3"},
        {"code": "        for x in nums:",
         "explain": "<p>Process the numbers left to right. Each one either improves an existing tail or creates a new, longer length. Order matters: a subsequence must respect the original positions, and visiting in order guarantees that every tail we overwrite or extend was built from earlier elements.</p>",
         "diagram": "  nums = [3, 1, 5, 2, 6, 4]\n          x=3 x=1 x=5 x=2 x=6 x=4"},
        {"code": "            i = bisect_left(tails, x)",
         "explain": "<p>Find where <code>x</code> belongs. Because <code>tails</code> is sorted (each longer subsequence needs a strictly larger ending), binary search gives the index of the first tail that is <code>&ge; x</code> in O(log n). Using <code>bisect_left</code> rather than <code>bisect_right</code> enforces <em>strictly</em> increasing: an equal value lands on itself and is overwritten, not appended after it.</p>",
         "diagram": "  tails = [1, 5],  x = 2\n  bisect_left -> i = 1   (5 is the first tail >= 2)\n\n  tails = [1, 2],  x = 6\n  bisect_left -> i = 2   (past the end: 6 beats every tail)"},
        {"code": "            if i == len(tails):\n                tails.append(x)",
         "explain": "<p>If <code>x</code> is larger than every tail, it can extend the longest subsequence found so far, so we have a new length. Append it as the best (and only) known ending for that length.</p>",
         "diagram": "  x=3: tails=[]      i=0 == len -> append  -> [3]\n  x=5: tails=[1]     i=1 == len -> append  -> [1, 5]\n  x=6: tails=[1, 2]  i=2 == len -> append  -> [1, 2, 6]"},
        {"code": "            else:\n                tails[i] = x",
         "explain": "<p>Otherwise <code>x</code> is a cheaper ending for a subsequence of length <code>i + 1</code>: there is an increasing subsequence of that length ending at <code>tails[i - 1] &lt; x</code>, extended by <code>x</code>, and <code>x &le; tails[i]</code>. Replacing keeps the array sorted and makes future extensions easier. The length does not change.</p>",
         "diagram": "  x=1: tails=[3]        i=0 -> overwrite -> [1]\n  x=2: tails=[1, 5]     i=1 -> overwrite -> [1, 2]\n  x=4: tails=[1, 2, 6]  i=2 -> overwrite -> [1, 2, 4]"},
        {"code": "        return len(tails)",
         "explain": "<p>Every index in <code>tails</code> corresponds to a length that was achieved by some real subsequence, and the array only grows when a strictly longer one appears. So its length is the length of the longest increasing subsequence. The final contents <code>[1, 2, 4]</code> happen to be a valid subsequence here, but that is not guaranteed in general; only the length is.</p>",
         "diagram": "  full trace, nums = [3, 1, 5, 2, 6, 4]\n  x=3  ->  [3]\n  x=1  ->  [1]\n  x=5  ->  [1, 5]\n  x=2  ->  [1, 2]\n  x=6  ->  [1, 2, 6]\n  x=4  ->  [1, 2, 4]      len = 3"},
    ],
    "complexity": "Time O(n log n): one binary search per element. Space O(n) for the tails array in the worst case (already sorted input).",
}

TESTS = """
s = Solution()
assert s.lengthOfLIS([3, 1, 5, 2, 6, 4]) == 3
assert s.lengthOfLIS([9, 9, 9]) == 1
assert s.lengthOfLIS([10, 9, 2, 5, 3, 7, 101, 18]) == 4
assert s.lengthOfLIS([7]) == 1
assert s.lengthOfLIS([1, 2, 3, 4, 5]) == 5
assert s.lengthOfLIS([5, 4, 3, 2, 1]) == 1
assert s.lengthOfLIS([0, 1, 0, 3, 2, 3]) == 4
"""
