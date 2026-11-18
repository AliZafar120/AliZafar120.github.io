PROBLEM = {
    "slug": "unique-paths", "number": 62, "title": "Unique Paths", "category": "Dynamic Programming", "difficulty": "Medium",
    "url": "https://leetcode.com/problems/unique-paths/", "premium": False,
    "statement_html": """<p>A robot starts in the top-left cell of an <code>m</code> by <code>n</code> grid and wants to reach the bottom-right cell. At each move it may go one cell right or one cell down, never left or up. Count the number of distinct routes.</p>
<pre>
Input:  m = 3, n = 4
Output: 10

Input:  m = 1, n = 7
Output: 1        a single row: the only route is straight right
</pre>
<ul>
  <li>1 &le; m, n &le; 100</li>
  <li>The answer fits in a 32-bit integer</li>
</ul>""",
    "intro_html": """<p><strong>Grid DP with a single rolling row.</strong> The number of routes into a cell is the number of routes into the cell above plus the number into the cell on its left, since those are the only two places a move can come from. The first row and first column have exactly one route each. Because each row only depends on the row above, we keep one array and update it in place, left to right, so the space is O(n) rather than O(m n).</p>""",
    "blocks": [
        {"code": "class Solution:\n    def uniquePaths(self, m: int, n: int) -> int:",
         "explain": "<p>LeetCode passes the grid size as two integers: <code>m</code> rows and <code>n</code> columns. No imports are needed.</p>",
         "diagram": None},
        {"code": "        row = [1] * n",
         "explain": "<p>This array represents the top row of the grid. Every cell in the top row can only be reached by moving right along it, so each has exactly one route. The same array will be reused for every later row.</p>",
         "diagram": "  m = 3, n = 4\n  row 0:   1   1   1   1"},
        {"code": "        for _ in range(1, m):",
         "explain": "<p>Compute rows 1 through <code>m - 1</code>, one per iteration, overwriting <code>row</code> each time. We never need the row index itself, only the count of iterations, hence the underscore. When <code>m = 1</code> the loop does not run and the top row is the answer.</p>",
         "diagram": "  m = 3  ->  two iterations: row 1, then row 2"},
        {"code": "            for j in range(1, n):\n                row[j] += row[j - 1]",
         "explain": "<p>Walk the row left to right. Before the update, <code>row[j]</code> still holds the value from the row above (routes coming down). <code>row[j - 1]</code> has already been updated this iteration, so it holds the value for the cell to the left in the current row (routes coming from the left). Adding them in place gives the new cell value. Column 0 is skipped because its only route comes straight down, so it stays 1.</p>",
         "diagram": "  m = 3, n = 4\n  row 0:   1   1   1   1\n  row 1:   1   2   3   4     (1+1, 2+1, 3+1)\n  row 2:   1   3   6  10     (1+2, 3+3, 6+4)\n\n  computing row 1, j = 2:\n  above = row[2] = 1, left = row[1] = 2  ->  row[2] = 3"},
        {"code": "        return row[-1]",
         "explain": "<p>After the last row is processed, the final entry is the bottom-right cell, the robot's destination. For a 3 by 4 grid that is 10, which also equals the binomial coefficient C(5, 2): choose which 2 of the 5 moves go down.</p>",
         "diagram": "  final row (row 2):   1   3   6  [10]   -> return 10\n\n  m = 1, n = 7:  loop skipped, row = [1,1,1,1,1,1,1] -> 1"},
    ],
    "complexity": "Time O(m * n), one addition per cell. Space O(n) for the single rolling row.",
}

TESTS = """
s = Solution()
assert s.uniquePaths(3, 4) == 10
assert s.uniquePaths(1, 7) == 1
assert s.uniquePaths(3, 7) == 28
assert s.uniquePaths(3, 2) == 3
assert s.uniquePaths(1, 1) == 1
assert s.uniquePaths(10, 10) == 48620
assert s.uniquePaths(4, 3) == s.uniquePaths(3, 4)
"""
