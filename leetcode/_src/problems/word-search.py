PROBLEM = {
    "slug": "word-search", "number": 79, "title": "Word Search", "category": "Matrix", "difficulty": "Medium",
    "url": "https://leetcode.com/problems/word-search/", "premium": False,
    "statement_html": """<p>Given a grid of letters and a target word, decide whether the word can be traced through the grid by starting on any cell and stepping to an edge-sharing neighbour (up, down, left or right) for each following letter. A cell may be used at most once within a single trace.</p>
<pre>
Input:  board = [["C", "A", "T"],
                 ["X", "O", "S"],
                 ["D", "G", "E"]],  word = "CATS"
Output: True        C(0,0) -> A(0,1) -> T(0,2) -> S(1,2)

Input:  same board, word = "CAST"
Output: False       after C, A there is no adjacent S
</pre>
<ul>
  <li>1 &le; rows, cols &le; 6, 1 &le; len(word) &le; 15</li>
  <li>Letters only; diagonal moves are not allowed</li>
</ul>""",
    "intro_html": """<p><strong>Depth-first search with in-place marking.</strong> From every cell that matches the first letter, recursively try to match the rest of the word in the four neighbouring cells. To stop a path from revisiting a cell, overwrite it with a placeholder while it is on the current path and restore it on the way back (backtracking). This avoids a separate visited set and keeps the extra memory down to the recursion stack.</p>""",
    "blocks": [
        {"code": "from typing import List\n\nclass Solution:\n    def exist(self, board: List[List[str]], word: str) -> bool:\n        rows, cols = len(board), len(board[0])",
         "explain": "<p>LeetCode's signature takes the grid as a list of single-character lists and the word as a string. We cache the dimensions for the bounds checks that follow.</p>",
         "diagram": None},
        {"code": "        def dfs(r: int, c: int, k: int) -> bool:\n            if k == len(word):\n                return True",
         "explain": "<p>The recursive worker: can we match <code>word[k:]</code> starting at cell <code>(r, c)</code>? The first check is the success condition. If <code>k</code> has reached the end of the word, every letter has already been matched on the path that led here, so we report True before even looking at the cell.</p>",
         "diagram": "  word = \"CATS\"   k indexes the letter we are looking for\n  k=0 'C'   k=1 'A'   k=2 'T'   k=3 'S'   k=4 -> done, True"},
        {"code": "            if r < 0 or r >= rows or c < 0 or c >= cols or board[r][c] != word[k]:\n                return False",
         "explain": "<p>Fail fast. The cell may be off the grid (we call <code>dfs</code> on neighbours without checking bounds first, so the check lives here), or it may hold the wrong letter. A cell that is currently on the path holds the placeholder <code>\"#\"</code>, which never equals a letter, so this same test also rejects revisits.</p>",
         "diagram": "  board            looking for 'S' (k=3) from T at (0,2):\n  C A T            (-1,2) off grid      -> False\n  X O S            (1,2) = 'S' matches  -> continue\n  D G E            (0,3) off grid      -> False\n                   (0,1) = '#' (on path) -> False"},
        {"code": "            saved, board[r][c] = board[r][c], \"#\"",
         "explain": "<p>The letter matched, so this cell joins the current path. Remember its letter and overwrite it with a marker so deeper recursive calls cannot step back onto it. This is the in-place alternative to a visited set.</p>",
         "diagram": "  after matching C, A, T on the path:\n  # # #\n  X O S\n  D G E"},
        {"code": "            found = (dfs(r + 1, c, k + 1) or dfs(r - 1, c, k + 1)\n                     or dfs(r, c + 1, k + 1) or dfs(r, c - 1, k + 1))",
         "explain": "<p>Try to match the next letter in each of the four neighbours. The <code>or</code> chain short-circuits: as soon as one direction returns True, the others are skipped, since a single valid trace is enough. Diagonals are deliberately absent.</p>",
         "diagram": "  from T at (0,2), k+1 = 3 ('S'):\n  down  (1,2) -> 'S'  -> dfs(1,2,3) -> ... k=4 -> True\n  up, right, left: not evaluated (short-circuit)"},
        {"code": "            board[r][c] = saved\n            return found",
         "explain": "<p>Backtrack: put the original letter back so that other paths, starting from other cells or going through other neighbours, see the real grid. This runs whether or not the search below succeeded, which keeps the board unchanged after <code>exist</code> returns.</p>",
         "diagram": "  word = \"CAST\": C(0,0) -> A(0,1), then looking for 'S':\n  neighbours of A are C(#), T, O  -> all False\n  restore A, return False; restore C, return False\n\n  board is back to:   C A T / X O S / D G E"},
        {"code": "        for r in range(rows):\n            for c in range(cols):\n                if dfs(r, c, 0):\n                    return True\n        return False",
         "explain": "<p>The word may start anywhere, so launch a search from every cell. The first letter check inside <code>dfs</code> immediately rejects cells that do not match <code>word[0]</code>, so most starts are cheap. If no starting cell leads to a full match, the word is not in the grid.</p>",
         "diagram": "  word = \"CATS\"\n  start (0,0) 'C' == 'C' -> dfs ... -> True   return True\n\n  word = \"CAST\"\n  start (0,0) 'C' -> fails (shown above)\n  starts (0,1) .. (2,2): first letter != 'C' -> False\n  return False"},
    ],
    "complexity": "Time O(rows * cols * 3^L) where L = len(word): each start can branch three ways per letter after the first. Space O(L) for the recursion stack; the board is marked in place.",
}

TESTS = """
s = Solution()
b = [["C", "A", "T"], ["X", "O", "S"], ["D", "G", "E"]]
assert s.exist(b, "CATS") is True
assert s.exist(b, "CAST") is False
assert s.exist(b, "XOG") is True
assert s.exist(b, "DOG") is False
assert b == [["C", "A", "T"], ["X", "O", "S"], ["D", "G", "E"]]
b2 = [["A", "B", "C", "E"], ["S", "F", "C", "S"], ["A", "D", "E", "E"]]
assert s.exist(b2, "ABCCED") is True
assert s.exist(b2, "SEE") is True
assert s.exist(b2, "ABCB") is False
assert s.exist([["a"]], "a") is True
assert s.exist([["a"]], "b") is False
assert s.exist([["a", "b"], ["c", "d"]], "abdca") is False
assert s.exist([["a", "a"]], "aaa") is False
"""
