PROBLEM = {
    "slug": "coin-change", "number": 322, "title": "Coin Change", "category": "Dynamic Programming", "difficulty": "Medium",
    "url": "https://leetcode.com/problems/coin-change/", "premium": False,
    "statement_html": """<p>You have coins of a few given denominations and an unlimited supply of each. Return the smallest number of coins whose values add up exactly to <code>amount</code>. If no combination reaches the amount, return <code>-1</code>.</p>
<pre>
Input:  coins = [1, 3, 4], amount = 6
Output: 2        3 + 3 (greedy 4 + 1 + 1 would use 3 coins)

Input:  coins = [5], amount = 7
Output: -1
</pre>
<ul>
  <li>1 &le; len(coins) &le; 12, each coin value between 1 and 2<sup>31</sup> - 1</li>
  <li>0 &le; amount &le; 10<sup>4</sup></li>
</ul>""",
    "intro_html": """<p><strong>Bottom-up DP over amounts.</strong> Let <code>dp[a]</code> be the fewest coins that make amount <code>a</code>. The last coin used in an optimal answer has some value <code>c</code>, and what remains is an optimal answer for <code>a - c</code>, so <code>dp[a] = 1 + min(dp[a - c])</code> over all coins that fit. Filling the table from 0 up to <code>amount</code> guarantees every <code>dp[a - c]</code> is already known when we need it. Greedy fails here (see the first example), which is exactly why DP is needed.</p>""",
    "blocks": [
        {"code": "from typing import List\n\nclass Solution:\n    def coinChange(self, coins: List[int], amount: int) -> int:",
         "explain": "<p>The LeetCode signature: a list of coin values and the target amount, returning an integer count or <code>-1</code>.</p>",
         "diagram": None},
        {"code": "        INF = amount + 1",
         "explain": "<p>A sentinel meaning \"not reachable yet\". Any real answer uses at most <code>amount</code> coins (all 1s), so <code>amount + 1</code> is safely larger than every valid count while still being a small integer we can add 1 to without overflow worries. Using <code>float('inf')</code> would also work but mixes types.</p>",
         "diagram": "  amount = 6  ->  INF = 7   (no real answer can need 7 coins)"},
        {"code": "        dp = [INF] * (amount + 1)\n        dp[0] = 0",
         "explain": "<p>One table slot per amount from 0 to <code>amount</code>, all unreachable to start. The only free fact is <code>dp[0] = 0</code>: making nothing takes zero coins. Every other entry will be derived from smaller ones.</p>",
         "diagram": "  a:    0   1   2   3   4   5   6\n  dp:   0   7   7   7   7   7   7"},
        {"code": "        for a in range(1, amount + 1):",
         "explain": "<p>Walk the amounts in increasing order. When we process <code>a</code>, every smaller amount is final, so <code>dp[a - c]</code> is trustworthy for any coin <code>c &le; a</code>. This ordering is what makes the bottom-up approach correct.</p>",
         "diagram": "  a = 1, 2, 3, 4, 5, 6   (each one sees only finished smaller slots)"},
        {"code": "            for c in coins:\n                if c <= a and dp[a - c] + 1 < dp[a]:\n                    dp[a] = dp[a - c] + 1",
         "explain": "<p>Try every coin as the <em>last</em> coin placed. The coin must not exceed <code>a</code>, and using it costs one coin on top of the best way to make the remainder. Keep the smallest total. If the remainder is unreachable, <code>dp[a - c]</code> is <code>INF</code>, so <code>INF + 1</code> never beats anything real and the slot stays <code>INF</code>.</p>",
         "diagram": "  coins = [1, 3, 4]\n  a=1: c=1 -> dp[0]+1 = 1                 dp[1] = 1\n  a=2: c=1 -> dp[1]+1 = 2                 dp[2] = 2\n  a=3: c=1 -> 3, c=3 -> dp[0]+1 = 1       dp[3] = 1\n  a=4: c=1 -> 2, c=3 -> 2, c=4 -> 1       dp[4] = 1\n  a=5: c=1 -> 2, c=3 -> 3, c=4 -> 2       dp[5] = 2\n  a=6: c=1 -> 3, c=3 -> dp[3]+1 = 2, c=4 -> 3   dp[6] = 2"},
        {"code": "        return dp[amount] if dp[amount] != INF else -1",
         "explain": "<p>The last slot is the answer, unless it was never updated, in which case no combination of coins reaches the amount and the problem asks for <code>-1</code>. For <code>amount = 0</code> the table is just <code>[0]</code> and we correctly return 0.</p>",
         "diagram": "  final table, coins = [1, 3, 4], amount = 6\n  a:    0   1   2   3   4   5   6\n  dp:   0   1   2   1   1   2   2    -> return 2\n\n  coins = [5], amount = 7\n  a:    0   1   2   3   4   5   6   7\n  dp:   0   8   8   8   8   1   8   8    -> dp[7] == INF -> -1"},
    ],
    "complexity": "Time O(amount * len(coins)), one inner pass per table slot. Space O(amount) for the table.",
}

TESTS = """
s = Solution()
assert s.coinChange([1, 3, 4], 6) == 2
assert s.coinChange([5], 7) == -1
assert s.coinChange([1, 2, 5], 11) == 3
assert s.coinChange([2], 3) == -1
assert s.coinChange([1], 0) == 0
assert s.coinChange([7], 7) == 1
assert s.coinChange([186, 419, 83, 408], 6249) == 20
"""
