PROBLEM = {
    "slug": "set-matrix-zeroes", "number": 73, "title": "Set Matrix Zeroes", "category": "Matrix", "difficulty": "Medium",
    "url": "https://leetcode.com/problems/set-matrix-zeroes/", "premium": False,
    "statement_html": """<p>Given a grid of integers, find every cell that holds 0 and set its entire row and entire column to 0. Do it in place. The catch is that newly written zeros must not trigger further clearing; only the zeros present in the original grid count.</p>
<pre>
Input:  matrix = [[1, 2, 3],
                  [4, 0, 6],
                  [7, 8, 9]]
Output: [[1, 0, 3],
         [0, 0, 0],
         [7, 0, 9]]

Input:  matrix = [[0, 5],
                  [3, 4]]
Output: [[0, 0],
         [0, 4]]
</pre>
<ul>
  <li>1 &le; rows, cols &le; 200</li>
  <li>Follow-up: O(1) extra space, not O(rows + cols)</li>
</ul>""",
    "intro_html": """<p><strong>Use the first row and first column as marker storage.</strong> The obvious approach records which rows and columns need clearing in two extra arrays. To get O(1) extra space, we store those same flags <em>inside</em> the matrix: cell <code>[i][0]</code> marks row <code>i</code> and cell <code>[0][j]</code> marks column <code>j</code>. The only complication is that the first row and column then play two roles, so we note up front whether they themselves need clearing and handle them last.</p>""",
    "blocks": [
        {"code": "from typing import List\n\nclass Solution:\n    def setZeroes(self, matrix: List[List[int]]) -> None:",
         "explain": "<p>The method returns nothing. LeetCode inspects <code>matrix</code> after the call, so every change must be made to the list of lists we were handed.</p>",
         "diagram": None},
        {"code": "        rows, cols = len(matrix), len(matrix[0])",
         "explain": "<p>Cache the dimensions. The problem guarantees at least one row and one column, so <code>matrix[0]</code> is safe.</p>",
         "diagram": "  matrix = [[1, 2, 3],\n            [4, 0, 6],\n            [7, 8, 9]]     rows = 3, cols = 3"},
        {"code": "        first_row_zero = any(matrix[0][j] == 0 for j in range(cols))\n        first_col_zero = any(matrix[i][0] == 0 for i in range(rows))",
         "explain": "<p>Before we start writing markers into row 0 and column 0, record whether they contain any original zero. Once markers are written, a 0 in <code>matrix[0][j]</code> could mean \"column j must be cleared\" or \"this cell was 0 originally\", and we would not be able to tell. Two booleans resolve that ambiguity at O(1) cost.</p>",
         "diagram": "  row 0:   1 2 3         -> first_row_zero = False\n  col 0:   1 4 7         -> first_col_zero = False"},
        {"code": "        for i in range(1, rows):\n            for j in range(1, cols):\n                if matrix[i][j] == 0:\n                    matrix[i][0] = 0\n                    matrix[0][j] = 0",
         "explain": "<p>Scan the inner region (everything except row 0 and column 0). Each 0 found leaves two marks: a 0 at the start of its row and a 0 at the top of its column. Those header cells are being repurposed as flags. We skip row 0 and column 0 in this scan because their zeros were already captured by the two booleans.</p>",
         "diagram": "  found matrix[1][1] == 0\n  mark matrix[1][0] = 0  (row 1 flagged)\n  mark matrix[0][1] = 0  (col 1 flagged)\n\n      1 [0] 3\n     [0] 0  6\n      7  8  9"},
        {"code": "        for i in range(1, rows):\n            for j in range(1, cols):\n                if matrix[i][0] == 0 or matrix[0][j] == 0:\n                    matrix[i][j] = 0",
         "explain": "<p>Second pass over the same inner region: a cell is cleared if its row flag or its column flag is set. Reading the flags while writing only inner cells is safe because inner writes never touch row 0 or column 0, so the flags stay intact until this pass is done.</p>",
         "diagram": "  flags: row 1 set, col 1 set\n  (1,1): row flag -> 0      (1,2): row flag -> 0\n  (2,1): col flag -> 0      (2,2): neither  -> keep 9\n\n      1  0  3\n      0  0  0\n      7  0  9"},
        {"code": "        if first_row_zero:\n            for j in range(cols):\n                matrix[0][j] = 0",
         "explain": "<p>Now the flags have served their purpose, so we can finally overwrite row 0 if it originally held a zero. Doing this earlier would have destroyed the column flags.</p>",
         "diagram": "  matrix = [[0, 5],\n            [3, 4]]       first_row_zero = True\n  after:    [0, 0]        row 0 cleared"},
        {"code": "        if first_col_zero:\n            for i in range(rows):\n                matrix[i][0] = 0",
         "explain": "<p>Same for column 0, the last step. In the first example neither boolean is set, so the matrix is already in its final form; in the second example both are set and both clears run, producing <code>[[0, 0], [0, 4]]</code>.</p>",
         "diagram": "  matrix = [[0, 5],\n            [3, 4]]       first_col_zero = True\n  after:    [[0, 0],\n             [0, 4]]"},
    ],
    "complexity": "Time O(rows * cols), two passes over the grid. Space O(1) extra: two booleans, with flags stored in the matrix itself.",
}

TESTS = """
s = Solution()
m = [[1, 2, 3], [4, 0, 6], [7, 8, 9]]; s.setZeroes(m); assert m == [[1, 0, 3], [0, 0, 0], [7, 0, 9]]
m = [[0, 5], [3, 4]]; s.setZeroes(m); assert m == [[0, 0], [0, 4]]
m = [[1, 1, 1], [1, 0, 1], [1, 1, 1]]; s.setZeroes(m); assert m == [[1, 0, 1], [0, 0, 0], [1, 0, 1]]
m = [[0, 1, 2, 0], [3, 4, 5, 2], [1, 3, 1, 5]]; s.setZeroes(m); assert m == [[0, 0, 0, 0], [0, 4, 5, 0], [0, 3, 1, 0]]
m = [[7]]; s.setZeroes(m); assert m == [[7]]
m = [[0]]; s.setZeroes(m); assert m == [[0]]
m = [[1, 2], [3, 4]]; s.setZeroes(m); assert m == [[1, 2], [3, 4]]
m = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]; s.setZeroes(m); assert m == [[1, 2, 0], [4, 5, 0], [0, 0, 0]]
"""
