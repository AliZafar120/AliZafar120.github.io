PROBLEM = {
    "slug": "missing-number", "number": 268, "title": "Missing Number", "category": "Binary", "difficulty": "Easy",
    "url": "https://leetcode.com/problems/missing-number/", "premium": False,
    "statement_html": """<p>You are given a list <code>nums</code> of <code>n</code> distinct integers, each in the range 0 to <code>n</code> inclusive. That range has <code>n + 1</code> values, so exactly one of them is absent from the list. Return the absent value, ideally in O(n) time and O(1) extra space.</p>
<pre>
Input:  nums = [3, 0, 1]
Output: 2          the range is 0..3 and 2 is missing

Input:  nums = [0, 1]
Output: 2          n = 2, so the range is 0..2
</pre>
<ul>
  <li>1 &le; n &le; 10<sup>4</sup>, 0 &le; nums[i] &le; n, all values distinct</li>
  <li>Exactly one value of 0..n is missing</li>
</ul>""",
    "intro_html": """<p><strong>XOR everything together.</strong> XOR has two handy properties: <code>x ^ x = 0</code> and <code>x ^ 0 = x</code>, and the order does not matter. If we XOR all the indices 0..n with all the values in the list, every value that is present pairs up with the equal index and cancels to zero, and the only thing left standing is the missing number. This avoids the overflow worry of the sum-formula approach and needs no extra memory.</p>""",
    "blocks": [
        {"code": "from typing import List\n\nclass Solution:\n    def missingNumber(self, nums: List[int]) -> int:",
         "explain": "<p>LeetCode calls <code>missingNumber</code> with the list and expects the single absent value.</p>",
         "diagram": None},
        {"code": "        result = len(nums)",
         "explain": "<p>The indices we will XOR in run from 0 to <code>n - 1</code>, but the full range of candidates is 0 to <code>n</code>. Seeding the accumulator with <code>n</code> itself covers that last candidate without needing a special case.</p>",
         "diagram": "  nums = [3, 0, 1]   n = 3\n  candidates 0..3, indices only reach 0..2 -> start with 3\n  result = 3 = 011"},
        {"code": "        for i, num in enumerate(nums):",
         "explain": "<p>Walk the list once, getting each index and the value stored there. Both go into the XOR.</p>",
         "diagram": "  i=0 num=3    i=1 num=0    i=2 num=1"},
        {"code": "            result ^= i ^ num",
         "explain": "<p>Fold the index and the value into the accumulator. Across the whole loop every number that appears both as an index and as a value is XORed twice and vanishes. Since the values are exactly the range 0..n minus one number, only that missing number is XORed an odd number of times.</p>",
         "diagram": "  step        result\n  start        3     (011)\n  ^0 ^3  ->    0     (3^0^3 = 0)\n  ^1 ^0  ->    1     (0^1^0 = 1)\n  ^2 ^1  ->    2     (1^2^1 = 2)\n\n  overall: 3 ^ 0 ^ 1 ^ 2  ^  3 ^ 0 ^ 1   -> pairs cancel, 2 remains"},
        {"code": "        return result",
         "explain": "<p>What remains after all cancellations is the missing value. The XOR of 0..n and the XOR of the list differ by exactly one term, and that term is the answer.</p>",
         "diagram": "  nums = [0, 1]   n = 2\n  2 ^ (0^0) ^ (1^1) = 2"},
    ],
    "complexity": "Time O(n), one pass. Space O(1).",
}

TESTS = """
s = Solution()
assert s.missingNumber([3, 0, 1]) == 2
assert s.missingNumber([0, 1]) == 2
assert s.missingNumber([0]) == 1
assert s.missingNumber([1]) == 0
assert s.missingNumber([9, 6, 4, 2, 3, 5, 7, 0, 1]) == 8
assert s.missingNumber(list(range(1, 1001))) == 0
assert s.missingNumber(list(range(1000))) == 1000
"""
