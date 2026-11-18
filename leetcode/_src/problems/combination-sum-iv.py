PROBLEM = {
    "slug": "combination-sum-iv", "number": 377, "title": "Combination Sum IV", "category": "Dynamic Programming", "difficulty": "Medium",
    "url": "https://leetcode.com/problems/combination-sum-iv/", "premium": False,
    "statement_html": """<p>You are given a list of distinct positive integers and a target. Count how many ordered sequences drawn from the list (with repetition allowed) sum to the target. Sequences that use the same numbers in a different order count separately, so this is really counting <em>permutations</em>, despite the title.</p>
<pre>
Input:  nums = [2, 3], target = 7
Output: 3        2+2+3, 2+3+2, 3+2+2

Input:  nums = [1, 2], target = 4
Output: 5        1111, 112, 121, 211, 22
</pre>
<ul>
  <li>1 &le; len(nums) &le; 200, 1 &le; nums[i] &le; 1000, all distinct</li>
  <li>1 &le; target &le; 1000</li>
  <li>The answer fits in a 32-bit integer</li>
</ul>""",
    "intro_html": """<p><strong>1D DP over the running total.</strong> Let <code>dp[t]</code> be the number of ordered sequences that sum to <code>t</code>. Any such sequence ends with some number <code>x</code> from the list, and what comes before it is a sequence summing to <code>t - x</code>, so <code>dp[t] = sum(dp[t - x])</code> over all <code>x &le; t</code>. Because we iterate the total in the outer loop and the numbers in the inner loop, every order of the same numbers is counted separately, which is exactly what this variant asks for.</p>""",
    "blocks": [
        {"code": "from typing import List\n\nclass Solution:\n    def combinationSum4(self, nums: List[int], target: int) -> int:",
         "explain": "<p>LeetCode's signature for the fourth Combination Sum problem: the candidate numbers and the target, returning a count rather than the sequences themselves.</p>",
         "diagram": None},
        {"code": "        dp = [0] * (target + 1)\n        dp[0] = 1",
         "explain": "<p>One counter per total from 0 up to <code>target</code>. <code>dp[0] = 1</code> says there is exactly one way to make zero: the empty sequence. It is not an answer by itself, but it is the base every real sequence is built from, since a sequence consisting of just <code>x</code> is \"empty sequence, then <code>x</code>\".</p>",
         "diagram": "  nums = [2, 3], target = 7\n  t:    0   1   2   3   4   5   6   7\n  dp:   1   0   0   0   0   0   0   0"},
        {"code": "        for t in range(1, target + 1):",
         "explain": "<p>Fill totals in increasing order. The outer loop runs over the total so that when we compute <code>dp[t]</code>, every <code>dp[t - x]</code> is final. Putting the total on the outside (and numbers inside) is also what makes different orders count separately; swapping the loops would count each multiset once, which is the Coin Change II problem instead.</p>",
         "diagram": "  t = 1, 2, 3, ..., 7     each total reads only smaller totals"},
        {"code": "            for x in nums:\n                if x <= t:\n                    dp[t] += dp[t - x]",
         "explain": "<p>Consider <code>x</code> as the <em>last</em> number in the sequence. Every sequence that reaches <code>t - x</code> becomes a sequence reaching <code>t</code> by appending <code>x</code>, and different last numbers give different sequences, so the counts simply add. Skip any <code>x</code> larger than <code>t</code>, which would need a negative remainder.</p>",
         "diagram": "  nums = [2, 3]\n  t=2: x=2 -> dp[0]=1              dp[2] = 1\n  t=3: x=2 -> dp[1]=0, x=3 -> dp[0]=1   dp[3] = 1\n  t=4: x=2 -> dp[2]=1, x=3 -> dp[1]=0   dp[4] = 1\n  t=5: x=2 -> dp[3]=1, x=3 -> dp[2]=1   dp[5] = 2\n  t=6: x=2 -> dp[4]=1, x=3 -> dp[3]=1   dp[6] = 2\n  t=7: x=2 -> dp[5]=2, x=3 -> dp[4]=1   dp[7] = 3"},
        {"code": "        return dp[target]",
         "explain": "<p>The last slot counts every ordered sequence summing exactly to the target. The three sequences for the example are the two ways to reach 5 (2+3, 3+2) extended by 2, plus the one way to reach 4 (2+2) extended by 3.</p>",
         "diagram": "  final table, nums = [2, 3], target = 7\n  t:    0   1   2   3   4   5   6   7\n  dp:   1   0   1   1   1   2   2   3    -> return 3\n\n  nums = [1, 2], target = 4  (Fibonacci-like)\n  t:    0   1   2   3   4\n  dp:   1   1   2   3   5                -> return 5"},
    ],
    "complexity": "Time O(target * len(nums)). Space O(target) for the table.",
}

TESTS = """
s = Solution()
assert s.combinationSum4([2, 3], 7) == 3
assert s.combinationSum4([1, 2], 4) == 5
assert s.combinationSum4([1, 2, 3], 4) == 7
assert s.combinationSum4([9], 3) == 0
assert s.combinationSum4([5], 5) == 1
assert s.combinationSum4([3, 1, 2], 5) == 13
"""
