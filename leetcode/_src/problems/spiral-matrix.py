PROBLEM = {
    "slug": "spiral-matrix", "number": 54, "title": "Spiral Matrix", "category": "Matrix", "difficulty": "Medium",
    "url": "https://leetcode.com/problems/spiral-matrix/", "premium": False,
    "statement_html": """<p>Given a rectangular grid of integers, return all its values in spiral order: start at the top-left, move right along the top row, then down the right column, then left along the bottom row, then up the left column, and keep circling inward until every cell has been visited once.</p>
<pre>
Input:  matrix = [[1,  2,  3,  4],
                  [5,  6,  7,  8],
                  [9, 10, 11, 12]]
Output: [1, 2, 3, 4, 8, 12, 11, 10, 9, 5, 6, 7]

Input:  matrix = [[1], [2], [3]]
Output: [1, 2, 3]
</pre>
<ul>
  <li>1 &le; rows, cols &le; 10</li>
  <li>-100 &le; matrix[i][j] &le; 100</li>
</ul>""",
    "intro_html": """<p><strong>Four shrinking bounds.</strong> Keep four indices for the unvisited rectangle: <code>top</code>, <code>bottom</code>, <code>left</code>, <code>right</code>. Each lap reads the top row, the right column, the bottom row and the left column, and after reading each side we move that bound inward by one. The lap ends when the bounds cross. Two guards prevent the bottom row or left column from being read twice when the remaining rectangle is a single row or a single column.</p>""",
    "blocks": [
        {"code": "from typing import List\n\nclass Solution:\n    def spiralOrder(self, matrix: List[List[int]]) -> List[int]:",
         "explain": "<p>LeetCode's signature: a list of rows in, a flat list of values in spiral order out.</p>",
         "diagram": None},
        {"code": "        out: List[int] = []\n        top, bottom = 0, len(matrix) - 1\n        left, right = 0, len(matrix[0]) - 1",
         "explain": "<p>The result list plus the four bounds, all inclusive. Initially the rectangle is the whole matrix: rows <code>top..bottom</code> and columns <code>left..right</code>. Everything inside these bounds is still unread.</p>",
         "diagram": "  3 x 4 matrix:  top=0  bottom=2  left=0  right=3\n\n       left           right\n  top    1   2   3   4\n         5   6   7   8\n  bottom 9  10  11  12"},
        {"code": "        while top <= bottom and left <= right:",
         "explain": "<p>Keep peeling off laps while the rectangle still has at least one row and one column. Each lap moves every bound inward, so the loop always terminates.</p>",
         "diagram": "  lap 1: rows 0..2, cols 0..3   (outer ring)\n  lap 2: rows 1..1, cols 1..2   (what is left: 6 7)\n  then top=2 > bottom=1 -> stop"},
        {"code": "            for j in range(left, right + 1):\n                out.append(matrix[top][j])\n            top += 1",
         "explain": "<p>Read the top row from left to right, then retire it by moving <code>top</code> down one. The row is now outside the rectangle and will never be read again.</p>",
         "diagram": "  read row 0:  1 2 3 4      out = [1, 2, 3, 4]\n  top -> 1\n\n         .   .   .   .\n  top    5   6   7   8\n  bottom 9  10  11  12"},
        {"code": "            for i in range(top, bottom + 1):\n                out.append(matrix[i][right])\n            right -= 1",
         "explain": "<p>Read the right column from the new <code>top</code> down to <code>bottom</code>, then retire that column by moving <code>right</code> left. Starting at the updated <code>top</code> is what avoids re-reading the corner cell 4.</p>",
         "diagram": "  read col 3, rows 1..2:  8 12     out = [1,2,3,4,8,12]\n  right -> 2\n\n         .   .   .   .\n  top    5   6   7   .\n  bottom 9  10  11   .\n       left   right"},
        {"code": "            if top <= bottom:\n                for j in range(right, left - 1, -1):\n                    out.append(matrix[bottom][j])\n                bottom -= 1",
         "explain": "<p>Read the bottom row right to left, but only if a bottom row distinct from the top row still exists. Without this guard, a rectangle that has shrunk to a single row (like the middle of a 3 by 4 matrix) would be read once as the top row and again, reversed, as the bottom row. The <code>range</code> runs backwards and stops at <code>left</code> inclusive, hence <code>left - 1</code>.</p>",
         "diagram": "  top=1 <= bottom=2, so read row 2, cols 2..0:  11 10 9\n  out = [1,2,3,4,8,12,11,10,9]\n  bottom -> 1\n\n         .   .   .   .\n  top    5   6   7   .     (bottom now == top)\n         .   .   .   ."},
        {"code": "            if left <= right:\n                for i in range(bottom, top - 1, -1):\n                    out.append(matrix[i][left])\n                left += 1",
         "explain": "<p>Read the left column bottom to top, guarded the same way: skip it if the rectangle has collapsed to a single column, which was already fully read as the right column. Then retire the column.</p>",
         "diagram": "  left=0 <= right=2, so read col 0, rows 1..1:  5\n  out = [1,2,3,4,8,12,11,10,9,5]\n  left -> 1\n\n  lap 2: top=1 bottom=1 left=1 right=2\n    top row 1, cols 1..2:  6 7     top -> 2\n    right col, rows 2..1:  (empty) right -> 1\n    top=2 > bottom=1: skip bottom row\n    left=1 <= right=1: rows 1..2 upward = (empty)\n  out = [1,2,3,4,8,12,11,10,9,5,6,7]"},
        {"code": "        return out",
         "explain": "<p>Every cell was appended exactly once: each side read is immediately retired, and the two guards stop the degenerate double reads. The output length always equals <code>rows * cols</code>.</p>",
         "diagram": "  [[1], [2], [3]]:  top row -> 1, right col rows 1..2 -> 2 3,\n  then right=-1 so the guards skip the rest.   out = [1, 2, 3]"},
    ],
    "complexity": "Time O(rows * cols), each cell visited once. Space O(1) extra beyond the output list.",
}

TESTS = """
s = Solution()
assert s.spiralOrder([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]) == [1, 2, 3, 4, 8, 12, 11, 10, 9, 5, 6, 7]
assert s.spiralOrder([[1], [2], [3]]) == [1, 2, 3]
assert s.spiralOrder([[1, 2, 3], [4, 5, 6], [7, 8, 9]]) == [1, 2, 3, 6, 9, 8, 7, 4, 5]
assert s.spiralOrder([[1, 2, 3]]) == [1, 2, 3]
assert s.spiralOrder([[7]]) == [7]
assert s.spiralOrder([[1, 2], [3, 4]]) == [1, 2, 4, 3]
assert s.spiralOrder([[1, 2], [3, 4], [5, 6]]) == [1, 2, 4, 6, 5, 3]
assert s.spiralOrder([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]]) == [1, 2, 3, 4, 8, 12, 16, 15, 14, 13, 9, 5, 6, 7, 11, 10]
"""
