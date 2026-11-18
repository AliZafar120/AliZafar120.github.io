PROBLEM = {
    "slug": "best-time-to-buy-and-sell-stock", "number": 121, "title": "Best Time to Buy and Sell Stock",
    "category": "Array", "difficulty": "Easy",
    "url": "https://leetcode.com/problems/best-time-to-buy-and-sell-stock/", "premium": False,
    "statement_html": """<p>You are given a list <code>prices</code> where <code>prices[i]</code> is the price of one share on day <code>i</code>. You may buy on one day and sell on a <em>later</em> day, at most once. Return the largest profit you can make; if no profitable trade exists, return 0.</p>
<pre>
Input:  prices = [6, 2, 8, 1, 5]
Output: 6        buy at 2 (day 1), sell at 8 (day 2)

Input:  prices = [9, 7, 4, 3]
Output: 0        prices only fall, so do not trade
</pre>
<ul>
  <li>1 &le; len(prices) &le; 10<sup>5</sup>, 0 &le; prices[i] &le; 10<sup>4</sup></li>
  <li>You must buy before you sell, and you make at most one trade</li>
</ul>""",
    "intro_html": """<p><strong>One pass tracking the lowest price so far.</strong> The best day to sell on is only as good as the cheapest day before it, so while scanning left to right we keep the minimum price seen and ask, for each day, what selling today would earn. The larger of all those answers is the result. This replaces the O(n&sup2;) check of every buy/sell pair with a single linear sweep.</p>""",
    "blocks": [
        {"code": "from typing import List\n\nclass Solution:\n    def maxProfit(self, prices: List[int]) -> int:",
         "explain": "<p>LeetCode calls <code>maxProfit</code> with the list of daily prices and expects a single integer, the best profit.</p>",
         "diagram": None},
        {"code": "        min_price = float(\"inf\")",
         "explain": "<p>The cheapest price seen <em>so far</em>, which is the best possible buy day for anything to the right. Starting at infinity means the very first real price will replace it immediately.</p>",
         "diagram": "  min_price = inf        (nothing seen yet)"},
        {"code": "        best = 0",
         "explain": "<p>The best profit found so far. Starting at 0 covers the case where every trade would lose money: we simply never trade and return 0.</p>",
         "diagram": "  prices = [6, 2, 8, 1, 5]\n  min_price = inf   best = 0"},
        {"code": "        for price in prices:",
         "explain": "<p>Walk the days in order. Order matters: when we look at a price, <code>min_price</code> only contains days strictly before it, which is exactly the rule that you must buy before you sell.</p>",
         "diagram": None},
        {"code": "            if price < min_price:\n                min_price = price",
         "explain": "<p>A new low. Buying here beats every earlier buy day for all future sales, so record it. There is no point computing a profit on this day: selling on the cheapest day so far cannot beat anything.</p>",
         "diagram": "  price=6  6 < inf  -> min_price = 6\n  price=2  2 < 6    -> min_price = 2\n  price=8  8 < 2 ?  no\n  price=1  1 < 2    -> min_price = 1\n  price=5  5 < 1 ?  no"},
        {"code": "            elif price - min_price > best:\n                best = price - min_price",
         "explain": "<p>Otherwise this day is a candidate sell day. The profit from buying at the lowest earlier price and selling now is <code>price - min_price</code>; keep it if it beats the best so far. Note that when price drops to a new low at day 3 (value 1), the earlier profit of 6 is not lost: <code>best</code> remembers it.</p>",
         "diagram": "  price   min_price   profit   best\n    6        6          -       0\n    2        2          -       0\n    8        2          6       6   <- new best\n    1        1          -       6\n    5        1          4       6"},
        {"code": "        return best",
         "explain": "<p>After the sweep, <code>best</code> holds the maximum of selling on every day against the cheapest earlier day, which covers every valid trade exactly once.</p>",
         "diagram": "  prices = [9, 7, 4, 3]\n  min_price: 9 -> 7 -> 4 -> 3, never a profitable sell\n  best stays 0"},
    ],
    "complexity": "Time O(n), one pass. Space O(1), two variables.",
}

TESTS = """
s = Solution()
assert s.maxProfit([6, 2, 8, 1, 5]) == 6
assert s.maxProfit([9, 7, 4, 3]) == 0
assert s.maxProfit([5]) == 0
assert s.maxProfit([3, 3, 3]) == 0
assert s.maxProfit([1, 2, 3, 4, 5]) == 4
assert s.maxProfit([2, 10, 1, 5]) == 8
"""
