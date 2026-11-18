PROBLEM = {
    "slug": "pacific-atlantic-water-flow", "number": 417, "title": "Pacific Atlantic Water Flow", "category": "Graph", "difficulty": "Medium",
    "url": "https://leetcode.com/problems/pacific-atlantic-water-flow/", "premium": False,
    "statement_html": """<p>A rectangular island is described by a grid of heights. The Pacific Ocean touches the top edge and the left edge; the Atlantic touches the bottom edge and the right edge. Rain falling on a cell can flow to any of its four neighbours whose height is <strong>less than or equal</strong> to its own, and it drains into an ocean when it leaves the grid. Return the coordinates of every cell from which water can reach <em>both</em> oceans, in any order.</p>
<pre>
Input:  heights = [[1, 3, 2],
                   [4, 2, 5]]
Output: [[0, 1], [0, 2], [1, 0], [1, 2]]
        (0,0) is on the Pacific coast but both neighbours are higher,
        so its water never reaches the Atlantic

Input:  heights = [[5]]
Output: [[0, 0]]
</pre>
<ul>
  <li>1 &le; rows, cols &le; 200</li>
  <li>0 &le; heights[r][c] &le; 10<sup>5</sup></li>
</ul>""",
    "intro_html": """<p><strong>Reverse depth-first search from the coastlines.</strong> Instead of asking for each cell \"where does its water go\" (which repeats work for every cell), we start on each coast and climb <em>uphill</em>: a cell is reachable from an ocean if a neighbour that already reaches the ocean is no higher than it. One DFS from the Pacific coast and one from the Atlantic coast mark two sets of cells; the answer is their intersection.</p>""",
    "blocks": [
        {"code": "from typing import List\n\nclass Solution:\n    def pacificAtlantic(self, heights: List[List[int]]) -> List[List[int]]:",
         "explain": "<p>LeetCode calls <code>pacificAtlantic</code> with the height grid and expects a list of <code>[row, col]</code> pairs. Any order is accepted, which is why we can collect the answer from a set at the end.</p>",
         "diagram": None},
        {"code": "        if not heights or not heights[0]:\n            return []\n        rows, cols = len(heights), len(heights[0])",
         "explain": "<p>Guard against an empty grid, then cache the dimensions so the bounds checks inside the DFS stay short and cheap.</p>",
         "diagram": "  heights = [[1, 3, 2],\n             [4, 2, 5]]     rows = 2, cols = 3"},
        {"code": "        pacific, atlantic = set(), set()",
         "explain": "<p>Two visited sets of <code>(row, col)</code> tuples, one per ocean. A cell lands in <code>pacific</code> once we have shown water from it can reach the Pacific, and likewise for <code>atlantic</code>. Keeping them separate is essential: the final answer needs cells that are in both.</p>",
         "diagram": "  pacific  = {}      Pacific  touches row 0 and column 0\n  atlantic = {}      Atlantic touches row 1 and column 2"},
        {"code": "        def dfs(r: int, c: int, reached: set) -> None:\n            reached.add((r, c))",
         "explain": "<p>A nested helper so it can see <code>heights</code>, <code>rows</code> and <code>cols</code> without passing them around. The call means \"cell <code>(r, c)</code> drains into this ocean\", so the first thing we do is record it. Marking <em>before</em> recursing is what prevents infinite loops between two equal-height neighbours.</p>",
         "diagram": None},
        {"code": "            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):\n                nr, nc = r + dr, c + dc",
         "explain": "<p>Visit the four orthogonal neighbours. The tuple of direction offsets is the usual grid idiom; it avoids writing four near-identical blocks.</p>",
         "diagram": "  from (0, 2):  down (1, 2)   up (-1, 2)   right (0, 3)   left (0, 1)"},
        {"code": "                if (0 <= nr < rows and 0 <= nc < cols\n                        and (nr, nc) not in reached\n                        and heights[nr][nc] >= heights[r][c]):\n                    dfs(nr, nc, reached)",
         "explain": "<p>Three conditions: the neighbour is inside the grid, we have not already marked it for this ocean, and it is <strong>at least as high</strong> as the current cell. That last test is the forward rule (water flows down or flat) read backwards: if water flows from the neighbour to us, and we reach the ocean, then so does the neighbour. Recursing on a 200 by 200 grid is fine on LeetCode; an explicit stack would do the same job if recursion depth were a concern.</p>",
         "diagram": "  Pacific climb from (0, 2) height 2:\n    (1, 2) height 5 >= 2 and not reached -> dfs(1, 2)\n      (1, 1) height 2 < 5  -> stop\n    (0, 1) height 3 >= 2 but already reached -> skip"},
        {"code": "        for c in range(cols):\n            dfs(0, c, pacific)\n            dfs(rows - 1, c, atlantic)",
         "explain": "<p>Launch the climbs from the horizontal coasts: every cell in the top row drains into the Pacific, every cell in the bottom row into the Atlantic. Because <code>dfs</code> adds the cell before checking anything, a coast cell is always marked even if it is a local minimum.</p>",
         "diagram": "  top row    (0,0) (0,1) (0,2)  -> pacific\n  bottom row (1,0) (1,1) (1,2)  -> atlantic"},
        {"code": "        for r in range(rows):\n            dfs(r, 0, pacific)\n            dfs(r, cols - 1, atlantic)",
         "explain": "<p>Same for the vertical coasts: left column to the Pacific, right column to the Atlantic. The corner cells are started twice for the same ocean, but the second call returns immediately after re-adding an existing set member, so no harm done.</p>",
         "diagram": "  after all climbs (P = reaches Pacific, A = reaches Atlantic)\n        col0  col1  col2\n  row0   P     PA    PA\n  row1   PA    A     PA\n  (0,0) height 1 is below both neighbours  -> Pacific only\n  (1,1) height 2 is below all three        -> Atlantic only"},
        {"code": "        return [[r, c] for r, c in pacific & atlantic]",
         "explain": "<p>Set intersection gives exactly the cells that reach both oceans. We convert each tuple back into the <code>[row, col]</code> list form that LeetCode expects.</p>",
         "diagram": "  pacific & atlantic = {(0,1), (0,2), (1,0), (1,2)}\n  -> [[0,1], [0,2], [1,0], [1,2]]   (any order)"},
    ],
    "complexity": "Time O(rows * cols): each cell is marked at most once per ocean, so at most twice. Space O(rows * cols) for the two sets and the recursion stack.",
}

TESTS = """
s = Solution()
assert sorted(s.pacificAtlantic([[1, 3, 2], [4, 2, 5]])) == [[0, 1], [0, 2], [1, 0], [1, 2]]
assert s.pacificAtlantic([[5]]) == [[0, 0]]
assert sorted(s.pacificAtlantic([[1, 2], [3, 4]])) == [[0, 1], [1, 0], [1, 1]]
assert sorted(s.pacificAtlantic([[2, 2], [2, 2]])) == [[0, 0], [0, 1], [1, 0], [1, 1]]
assert sorted(s.pacificAtlantic([[1, 2, 3], [8, 9, 4], [7, 6, 5]])) == [[0, 2], [1, 0], [1, 1], [1, 2], [2, 0], [2, 1], [2, 2]]
assert sorted(s.pacificAtlantic([[1, 2, 2, 3, 5], [3, 2, 3, 4, 4], [2, 4, 5, 3, 1], [6, 7, 1, 4, 5], [5, 1, 1, 2, 4]])) == [[0, 4], [1, 3], [1, 4], [2, 2], [3, 0], [3, 1], [4, 0]]
"""
