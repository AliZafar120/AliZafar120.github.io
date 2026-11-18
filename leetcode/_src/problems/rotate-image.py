PROBLEM = {
    "slug": "rotate-image", "number": 48, "title": "Rotate Image", "category": "Matrix", "difficulty": "Medium",
    "url": "https://leetcode.com/problems/rotate-image/", "premium": False,
    "statement_html": """<p>You are given a square grid of integers. Rotate it 90 degrees clockwise in place: modify the given list of lists rather than returning a new one. After the rotation the old top row should be the new right column, read top to bottom.</p>
<pre>
Input:  matrix = [[1, 2, 3],
                  [4, 5, 6],
                  [7, 8, 9]]
Output: [[7, 4, 1],
         [8, 5, 2],
         [9, 6, 3]]

Input:  matrix = [[1, 2],
                  [3, 4]]
Output: [[3, 1],
         [4, 2]]
</pre>
<ul>
  <li>1 &le; n &le; 20, the matrix is n by n</li>
  <li>Must be done in place with O(1) extra memory</li>
</ul>""",
    "intro_html": """<p><strong>Transpose, then reverse each row.</strong> A clockwise rotation sends the element at <code>(i, j)</code> to <code>(j, n-1-i)</code>. That is the composition of two simple in-place operations: transposing swaps <code>(i, j)</code> with <code>(j, i)</code>, and reversing every row then maps column <code>i</code> to column <code>n-1-i</code>. Each step is a handful of swaps with no temporary matrix.</p>""",
    "blocks": [
        {"code": "from typing import List\n\nclass Solution:\n    def rotate(self, matrix: List[List[int]]) -> None:",
         "explain": "<p>The method returns <code>None</code>; LeetCode checks the contents of <code>matrix</code> after the call. So every change must happen on the lists we were given, not on a copy.</p>",
         "diagram": None},
        {"code": "        n = len(matrix)",
         "explain": "<p>The matrix is square, so one dimension is enough for both the row and column loops.</p>",
         "diagram": "  matrix = [[1, 2, 3],\n            [4, 5, 6],\n            [7, 8, 9]]      n = 3"},
        {"code": "        for i in range(n):\n            for j in range(i + 1, n):",
         "explain": "<p>Visit only the cells strictly above the main diagonal. Transposing swaps <code>(i, j)</code> with <code>(j, i)</code>, so each pair of mirrored cells needs exactly one swap. Starting <code>j</code> at <code>i + 1</code> ensures we never touch a pair twice (which would undo it) and never swap a diagonal cell with itself.</p>",
         "diagram": "  cells visited (i, j), j > i:\n\n      .  (0,1) (0,2)\n      .    .   (1,2)\n      .    .     .\n\n  each is swapped with its mirror (j, i) below the diagonal"},
        {"code": "                matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]",
         "explain": "<p>The swap itself, using tuple assignment so no temporary variable is needed. After the loop, what used to be row <code>i</code> is now column <code>i</code>. At this point the matrix is the transpose, which is the rotation's mirror image.</p>",
         "diagram": "  before          after transpose\n  1 2 3           1 4 7\n  4 5 6    ->     2 5 8\n  7 8 9           3 6 9\n\n  swaps: (0,1)<->(1,0): 2<->4   (0,2)<->(2,0): 3<->7\n         (1,2)<->(2,1): 6<->8"},
        {"code": "        for row in matrix:\n            row.reverse()",
         "explain": "<p>Flip every row left to right. The transpose placed the old top row <code>1 2 3</code> in the first column reading downward, but a clockwise rotation needs it in the <em>last</em> column. Reversing each row moves column 0 to column <code>n - 1</code> and so on. <code>list.reverse()</code> works in place, so the original list objects are modified as required.</p>",
         "diagram": "  after transpose    after reversing rows\n  1 4 7              7 4 1\n  2 5 8      ->      8 5 2\n  3 6 9              9 6 3\n\n  old top row 1 2 3 is now the right column, top to bottom"},
    ],
    "complexity": "Time O(n^2): each cell is touched once by the transpose and once by the reversal. Space O(1), all swaps are in place.",
}

TESTS = """
s = Solution()
m = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]; s.rotate(m); assert m == [[7, 4, 1], [8, 5, 2], [9, 6, 3]]
m = [[1, 2], [3, 4]]; s.rotate(m); assert m == [[3, 1], [4, 2]]
m = [[5]]; s.rotate(m); assert m == [[5]]
m = [[5, 1, 9, 11], [2, 4, 8, 10], [13, 3, 6, 7], [15, 14, 12, 16]]; s.rotate(m); assert m == [[15, 13, 2, 5], [14, 3, 4, 1], [12, 6, 8, 9], [16, 7, 10, 11]]
m = [[1, 2], [3, 4]]; s.rotate(m); s.rotate(m); s.rotate(m); s.rotate(m); assert m == [[1, 2], [3, 4]]
"""
