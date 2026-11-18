PROBLEM = {
    "slug": "word-search-ii", "number": 212, "title": "Word Search II", "category": "Tree", "difficulty": "Hard",
    "url": "https://leetcode.com/problems/word-search-ii/", "premium": False,
    "statement_html": """<p>You are given a grid of lowercase letters <code>board</code> and a list of distinct <code>words</code>. Return every word that can be spelled by starting at some cell and moving to a horizontally or vertically adjacent cell for each following letter, never reusing a cell within one word. Words may be returned in any order.</p>
<pre>
Input:  board = [["c","a","t"],
                 ["o","d","e"],
                 ["r","n","s"]]
        words = ["cat", "code", "corn", "rod", "ten", "cats"]
Output: ["cat", "code", "corn", "rod"]
        "ten" fails: after t -> e the only "n" is diagonal to "e";
        "cats" fails: it needs an "s" next to "t", and only "e" is there

Input:  board = [["a"]],  words = ["a", "aa"]
Output: ["a"]
</pre>
<ul>
  <li>1 &le; rows, cols &le; 12; 1 &le; len(words) &le; 3 &middot; 10<sup>4</sup>; 1 &le; len(word) &le; 10</li>
  <li>All words are distinct and consist of lowercase letters</li>
</ul>""",
    "intro_html": """<p><strong>Trie-guided DFS with pruning.</strong> Searching the board once per word is far too slow, so we put all the words into a trie and run one depth-first search from every cell that follows the trie and the board <em>simultaneously</em>: a step is taken only if the next letter is a child of the current trie node. The trie stores each complete word at its end node so a hit can be recorded directly. After a word is found it is removed from the trie, and trie nodes that become empty are deleted, so later searches never re-explore paths that cannot produce anything new.</p>""",
    "blocks": [
        {"code": "from typing import List\n\nclass Solution:\n    def findWords(self, board: List[List[str]], words: List[str]) -> List[str]:",
         "explain": "<p>LeetCode calls <code>findWords</code> with the grid and the word list and accepts the found words in any order.</p>",
         "diagram": None},
        {"code": "        root = {}\n        for word in words:\n            node = root\n            for ch in word:\n                node = node.setdefault(ch, {})\n            node[\"$\"] = word",
         "explain": "<p>Build the trie as nested dicts. Instead of a boolean end marker we store the <strong>word itself</strong> under <code>\"$\"</code>: when the DFS reaches that node it can append the word without reconstructing it from the path.</p>",
         "diagram": "  words = [\"cat\", \"code\", \"corn\", \"rod\", \"ten\", \"cats\"]\n  root\n   c -- a -- t $\"cat\" -- s $\"cats\"\n   |    o -- d -- e $\"code\"\n   |         r -- n $\"corn\"\n   r -- o -- d $\"rod\"\n   t -- e -- n $\"ten\""},
        {"code": "        rows, cols = len(board), len(board[0])\n        found = []",
         "explain": "<p>Grid dimensions for bounds checks and the output list. Because each word is removed from the trie the moment it is found, <code>found</code> never receives duplicates even if the word can be spelled in several places.</p>",
         "diagram": "  board:  c a t\n          o d e      rows = 3, cols = 3\n          r n s      found = []"},
        {"code": "        def dfs(r: int, c: int, parent: dict) -> None:\n            ch = board[r][c]\n            node = parent[ch]",
         "explain": "<p><code>dfs</code> is called only when <code>board[r][c]</code> is a child of <code>parent</code>, so the lookup always succeeds. <code>node</code> is the trie position after consuming this cell's letter. We keep <code>parent</code> too because we may want to delete <code>node</code> from it on the way back.</p>",
         "diagram": "  dfs(0, 0, root): ch = \"c\", node = root[\"c\"]\n  dfs(0, 1, node): ch = \"a\", node = root[\"c\"][\"a\"]\n  dfs(0, 2, node): ch = \"t\", node = root[\"c\"][\"a\"][\"t\"]"},
        {"code": "            word = node.pop(\"$\", None)\n            if word is not None:\n                found.append(word)",
         "explain": "<p>If a word ends here, record it and <em>remove the marker</em> in the same step. Popping means a second path spelling the same word finds nothing, which both prevents duplicates and lets the pruning below delete the node once its children are gone.</p>",
         "diagram": "  at (0,2) \"t\": node = {\"$\": \"cat\", \"s\": {...}}\n  pop \"$\" -> word = \"cat\" -> found = [\"cat\"]\n  node is now {\"s\": {\"$\": \"cats\"}}"},
        {"code": "            board[r][c] = \"#\"",
         "explain": "<p>Mark the cell as used for the duration of this path. Overwriting the board avoids a separate visited set; <code>\"#\"</code> is never a trie key, so a neighbour check against it fails automatically.</p>",
         "diagram": "  exploring \"c\" -> \"a\" -> \"t\":\n      # # #\n      o d e     the top row is temporarily blocked\n      r n s"},
        {"code": "            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):\n                nr, nc = r + dr, c + dc\n                if 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] in node:\n                    dfs(nr, nc, node)",
         "explain": "<p>Try the four neighbours, but only step onto one whose letter continues some word in the trie. This is the trie doing the pruning: most of the grid is never explored because nothing in the word list starts that way.</p>",
         "diagram": "  from (0,2) \"t\" with node = {\"s\": {...}}:\n    (1,2) \"e\" in node? no\n    (0,1) \"#\" in node? no   -> no recursion, \"cats\" is dead\n\n  from (1,0) \"o\" (via \"c\") with node = {\"d\": ..., \"r\": ...}:\n    (2,0) \"r\" in node -> dfs -> (2,1) \"n\" -> \"corn\"\n    (1,1) \"d\" in node -> dfs -> (1,2) \"e\" -> \"code\""},
        {"code": "            board[r][c] = ch",
         "explain": "<p>Backtrack: restore the letter so other paths can use this cell. The DFS leaves the board exactly as it found it.</p>",
         "diagram": "  after returning from (0,2): board[0][2] = \"t\" again\n      c a t\n      o d e\n      r n s"},
        {"code": "            if not node:\n                parent.pop(ch)",
         "explain": "<p>Prune. If this trie node has no children left and no word marker, nothing below it can ever be found again, so unlink it from its parent. Over time the trie shrinks to just the words still outstanding, and once it is empty every later DFS stops at the first check.</p>",
         "diagram": "  after \"cat\" and the failed \"cats\" search: node for \"t\" still\n  holds {\"s\": ...}, so it stays.\n  after \"rod\" is found: node for \"d\" is {} -> pop \"d\" from \"o\"\n  then \"o\" is {} -> popped from \"r\"; \"r\" is {} -> popped from root"},
        {"code": "        for r in range(rows):\n            for c in range(cols):\n                if board[r][c] in root:\n                    dfs(r, c, root)\n        return found",
         "explain": "<p>Start a search from every cell whose letter is a first letter of some remaining word. Cells like <code>\"d\"</code> or <code>\"s\"</code> in the example are skipped outright. Return the collected words.</p>",
         "diagram": "  (0,0) \"c\" in root -> dfs -> finds \"corn\", \"code\", \"cat\"\n  (0,1) \"a\" not in root -> skip\n  (0,2) \"t\" in root -> \"e\" at (1,2) -> no \"n\" next to it -> dead\n  (2,0) \"r\" in root -> \"o\" at (1,0) -> \"d\" at (1,1) -> finds \"rod\"\n  found = [\"corn\", \"code\", \"cat\", \"rod\"]"},
    ],
    "complexity": "Time O(R * C * 4 * 3^(L-1)) in the worst case, where L is the longest word, but the trie pruning makes typical inputs far faster. Space O(total characters in words) for the trie plus O(L) recursion depth.",
}

TESTS = """
s = Solution()
board = [["c","a","t"],["o","d","e"],["r","n","s"]]
assert sorted(s.findWords(board, ["cat", "code", "corn", "rod", "ten", "cats"])) == ["cat", "code", "corn", "rod"]
assert board == [["c","a","t"],["o","d","e"],["r","n","s"]]
assert sorted(s.findWords([["a"]], ["a", "aa"])) == ["a"]
assert s.findWords([["a","b"],["c","d"]], ["abcb"]) == []
board2 = [["o","a","a","n"],["e","t","a","e"],["i","h","k","r"],["i","f","l","v"]]
assert sorted(s.findWords(board2, ["oath","pea","eat","rain"])) == ["eat", "oath"]
assert sorted(s.findWords([["a","a"]], ["aaa"])) == []
assert sorted(s.findWords([["a","b"],["a","b"]], ["ab", "ba", "aa", "bb"])) == ["aa", "ab", "ba", "bb"]
assert sorted(s.findWords([["x"]], ["y"])) == []
"""
