PROBLEM = {
    "slug": "number-of-islands", "number": 200, "title": "Number of Islands", "category": "Graph", "difficulty": "Medium",
    "url": "https://leetcode.com/problems/number-of-islands/", "premium": False,
    "statement_html": """<p>You are given a grid of characters where <code>"1"</code> is land and <code>"0"</code> is water. An island is a group of land cells connected horizontally or vertically (not diagonally), and everything outside the grid counts as water. Count how many islands there are.</p>
<pre>
Input:  grid = [["1","1","0","0"],
                ["0","1","0","1"],
                ["0","0","0","1"],
                ["1","0","0","0"]]
Output: 3        the top-left blob, the right column pair, the bottom-left cell

Input:  grid = [["0","0"],
                ["0","0"]]
Output: 0
</pre>
<ul>
  <li>1 &le; rows, cols &le; 300</li>
  <li>Every cell is either <code>"0"</code> or <code>"1"</code></li>
</ul>""",
    "intro_html": """<p><strong>Flood fill with depth-first search.</strong> Scan the grid cell by cell. Each time we step on land that has not been claimed yet, we have found a brand new island, so we bump the counter and then \"sink\" the entire island by recursively turning every connected land cell into water. Sinking guarantees that the same island is never counted again when the scan reaches another of its cells.</p>""",
    "blocks": [
        {"code": "from typing import List\n\nclass Solution:\n    def numIslands(self, grid: List[List[str]]) -> int:",
         "explain": "<p>LeetCode calls <code>numIslands</code> with a list of lists of one-character strings and expects an integer. Note that the cells are the <em>strings</em> <code>\"0\"</code> and <code>\"1\"</code>, not numbers.</p>",
         "diagram": None},
        {"code": "        if not grid:\n            return 0\n        rows, cols = len(grid), len(grid[0])\n        count = 0",
         "explain": "<p>Handle the degenerate empty input, remember the grid size for the bounds checks, and start the island counter at zero.</p>",
         "diagram": "  grid = 1 1 0 0      rows = 4, cols = 4\n         0 1 0 1      count = 0\n         0 0 0 1\n         1 0 0 0"},
        {"code": "        def sink(r: int, c: int) -> None:\n            if r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] != \"1\":\n                return",
         "explain": "<p>The flood fill. It is written as a nested function so it can read <code>grid</code>, <code>rows</code> and <code>cols</code> directly. The guard stops the recursion when we step off the grid or onto water, which includes land we have already sunk. Putting the bounds check inside the callee keeps the recursive calls below trivially short.</p>",
         "diagram": "  sink(-1, 0)  -> off grid, return\n  sink(0, 2)   -> grid[0][2] == \"0\", return\n  sink(0, 0)   -> land, keep going"},
        {"code": "            grid[r][c] = \"0\"",
         "explain": "<p>Mark the cell as visited by turning it into water in place. This saves a separate visited set and is the standard interview trick, but it does mutate the caller's grid; say so in an interview, and copy the grid first if the input must be preserved.</p>",
         "diagram": "  before sink(0,0)      after marking (0,0)\n  1 1 0 0               0 1 0 0\n  0 1 0 1               0 1 0 1"},
        {"code": "            sink(r + 1, c)\n            sink(r - 1, c)\n            sink(r, c + 1)\n            sink(r, c - 1)",
         "explain": "<p>Spread to the four neighbours. Each call either returns at once (water, off-grid, or already sunk) or sinks a new land cell and keeps spreading. Since every land cell is turned to water the first time it is touched, each cell is processed at most once across the whole run.</p>",
         "diagram": "  sink(0,0): mark -> sink(1,0) water, sink(-1,0) off\n             sink(0,1): mark -> sink(1,1): mark -> all 4 stop\n                               sink(0,2) water\n  island 1 fully sunk:\n  0 0 0 0\n  0 0 0 1\n  0 0 0 1\n  1 0 0 0"},
        {"code": "        for r in range(rows):\n            for c in range(cols):\n                if grid[r][c] == \"1\":\n                    count += 1\n                    sink(r, c)",
         "explain": "<p>The outer scan. Whenever we meet land it must belong to an island we have not seen, because every island found so far has been sunk. Count it, then sink it so none of its other cells trigger the <code>if</code> again. Scanning order does not matter; row-major is just the natural way to write it.</p>",
         "diagram": "  scan hits (0,0) -> count = 1, sink island 1\n  scan hits (1,3) -> count = 2, sink (1,3) and (2,3)\n  scan hits (3,0) -> count = 3, sink (3,0)\n  remaining cells are all \"0\""},
        {"code": "        return count",
         "explain": "<p>Every island was counted exactly once, when the scan first stepped on it.</p>",
         "diagram": None},
    ],
    "complexity": "Time O(rows * cols): every cell is visited by the scan once and sunk at most once. Space O(rows * cols) in the worst case for the recursion stack (a grid that is all land).",
}

TESTS = """
s = Solution()
g = [["1","1","0","0"],["0","1","0","1"],["0","0","0","1"],["1","0","0","0"]]
assert s.numIslands(g) == 3
assert s.numIslands([["0","0"],["0","0"]]) == 0
assert s.numIslands([["1"]]) == 1
assert s.numIslands([["0"]]) == 0
assert s.numIslands([["1","1","1"],["1","1","1"]]) == 1
assert s.numIslands([["1","0","1"],["0","1","0"],["1","0","1"]]) == 5
assert s.numIslands([["1","1","1","1","0"],["1","1","0","1","0"],["1","1","0","0","0"],["0","0","0","0","0"]]) == 1
"""
