PROBLEM = {
    "slug": "climbing-stairs", "number": 70, "title": "Climbing Stairs", "category": "Dynamic Programming", "difficulty": "Easy",
    "url": "https://leetcode.com/problems/climbing-stairs/", "premium": False,
    "statement_html": """<p>A staircase has <code>n</code> steps. From any step you may move up by 1 step or by 2 steps. Count how many distinct sequences of moves take you from the ground to the top. Two sequences are different if the order of moves differs, so 1-then-2 and 2-then-1 are both counted.</p>
<pre>
Input:  n = 4
Output: 5        1+1+1+1, 1+1+2, 1+2+1, 2+1+1, 2+2

Input:  n = 1
Output: 1
</pre>
<ul>
  <li>1 &le; n &le; 45</li>
  <li>The answer always fits in a 32-bit integer</li>
</ul>""",
    "intro_html": """<p><strong>Bottom-up DP with two variables.</strong> The last move onto step <code>n</code> came either from step <code>n-1</code> or from step <code>n-2</code>, so <code>ways(n) = ways(n-1) + ways(n-2)</code>. That is the Fibonacci recurrence. Since each value depends only on the two before it, we never need an array: two integers rolled forward through a loop give O(1) space.</p>""",
    "blocks": [
        {"code": "class Solution:\n    def climbStairs(self, n: int) -> int:",
         "explain": "<p>LeetCode calls <code>climbStairs</code> with the number of steps and expects an integer count back. No imports are needed because the input is a single <code>int</code>.</p>",
         "diagram": None},
        {"code": "        if n <= 2:\n            return n",
         "explain": "<p>The two smallest staircases are the base cases. One step has exactly one way (a single 1-move). Two steps have two ways (1+1 or a single 2-move). Both happen to equal <code>n</code>, so one line covers both and the loop below can safely assume <code>n &ge; 3</code>.</p>",
         "diagram": "  n = 1:  [1]          -> 1 way\n  n = 2:  [1,1] [2]    -> 2 ways"},
        {"code": "        prev, cur = 1, 2",
         "explain": "<p>Seed the rolling window. <code>prev</code> holds the count for the step two below the one we are about to compute, <code>cur</code> the count for the step just below. Starting at <code>ways(1) = 1</code> and <code>ways(2) = 2</code>, the next value to compute is <code>ways(3)</code>.</p>",
         "diagram": "  step:   1    2    3    4\n  ways:   1    2    ?    ?\n         prev  cur"},
        {"code": "        for _ in range(3, n + 1):",
         "explain": "<p>Compute <code>ways(3)</code>, then <code>ways(4)</code>, up to <code>ways(n)</code>, one per iteration. We do not need the loop variable itself, only the number of iterations, hence the underscore. The range has <code>n - 2</code> entries, which is exactly how many values remain after the two base cases.</p>",
         "diagram": "  n = 4  ->  range(3, 5) = 3, 4   (two iterations)"},
        {"code": "            prev, cur = cur, prev + cur",
         "explain": "<p>The recurrence in one line. The new count is <code>prev + cur</code>: every route to the step below extended by a 1-move, plus every route to the step two below extended by a 2-move. Those two groups cannot overlap because their final moves differ. At the same time the window slides: the old <code>cur</code> becomes the new <code>prev</code>. Python evaluates the right side first, so both reads see the old values.</p>",
         "diagram": "  n = 4\n  start:    prev=1  cur=2\n  iter 3:   prev=2  cur=1+2=3     ways(3)=3\n  iter 4:   prev=3  cur=2+3=5     ways(4)=5"},
        {"code": "        return cur",
         "explain": "<p>After the last iteration <code>cur</code> holds <code>ways(n)</code>. Only two integers were ever stored, so the space is O(1) regardless of <code>n</code>.</p>",
         "diagram": "  step:   1    2    3    4    5    6\n  ways:   1    2    3    5    8   13     return cur"},
    ],
    "complexity": "Time O(n), one loop iteration per step. Space O(1), just two integers.",
}

TESTS = """
s = Solution()
assert s.climbStairs(4) == 5
assert s.climbStairs(1) == 1
assert s.climbStairs(2) == 2
assert s.climbStairs(3) == 3
assert s.climbStairs(6) == 13
assert s.climbStairs(45) == 1836311903
"""
