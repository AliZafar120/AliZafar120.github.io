PROBLEM = {
    "slug": "longest-common-subsequence", "number": 1143, "title": "Longest Common Subsequence", "category": "Dynamic Programming", "difficulty": "Medium",
    "url": "https://leetcode.com/problems/longest-common-subsequence/", "premium": False,
    "statement_html": """<p>Given two strings, return the length of the longest sequence of characters that appears in both, in the same relative order, though not necessarily adjacent. Characters may be skipped in either string. If the strings share nothing, return 0.</p>
<pre>
Input:  text1 = "acbd", text2 = "abcd"
Output: 3        "abd" or "acd" appear in both in order

Input:  text1 = "xyz", text2 = "pq"
Output: 0
</pre>
<ul>
  <li>1 &le; len(text1), len(text2) &le; 1000</li>
  <li>Only lowercase English letters</li>
</ul>""",
    "intro_html": """<p><strong>Classic 2D DP table.</strong> Let <code>dp[i][j]</code> be the LCS length of the first <code>i</code> characters of <code>text1</code> and the first <code>j</code> characters of <code>text2</code>. If the two characters at those ends match, they extend the best answer for the two shorter prefixes by one. If they do not match, at least one of them is not part of the answer, so we drop one and take the better of the two results. Filling the table row by row answers every subproblem exactly once.</p>""",
    "blocks": [
        {"code": "class Solution:\n    def longestCommonSubsequence(self, text1: str, text2: str) -> int:",
         "explain": "<p>LeetCode's signature: two strings in, one integer out. No imports are needed.</p>",
         "diagram": None},
        {"code": "        m, n = len(text1), len(text2)",
         "explain": "<p>Cache the two lengths. <code>m</code> indexes rows (prefixes of <code>text1</code>), <code>n</code> indexes columns (prefixes of <code>text2</code>).</p>",
         "diagram": "  text1 = \"acbd\"  m = 4   (rows)\n  text2 = \"abcd\"  n = 4   (columns)"},
        {"code": "        dp = [[0] * (n + 1) for _ in range(m + 1)]",
         "explain": "<p>A table with one extra row and column. Row 0 and column 0 stand for the <em>empty</em> prefix, whose LCS with anything is 0, and they stay 0. This padding means the recurrence never has to special-case <code>i - 1</code> or <code>j - 1</code> going negative. Build rows with a comprehension, not <code>[[0]*(n+1)]*(m+1)</code>, which would alias the same list.</p>",
         "diagram": "          \"\"   a   b   c   d\n     \"\"    0   0   0   0   0\n     a     0   .   .   .   .\n     c     0   .   .   .   .\n     b     0   .   .   .   .\n     d     0   .   .   .   ."},
        {"code": "        for i in range(1, m + 1):\n            for j in range(1, n + 1):",
         "explain": "<p>Fill the table row by row, left to right. Cell <code>(i, j)</code> depends only on cells above it, to its left, and diagonally up-left, all of which are complete by the time we reach it. <code>i</code> and <code>j</code> are prefix lengths, so the characters being compared are <code>text1[i - 1]</code> and <code>text2[j - 1]</code>.</p>",
         "diagram": "  cell (i, j) needs:    (i-1, j-1)   (i-1, j)\n                        (i,   j-1)   (i,   j)  <- computing"},
        {"code": "                if text1[i - 1] == text2[j - 1]:\n                    dp[i][j] = dp[i - 1][j - 1] + 1",
         "explain": "<p>The characters match, so they can be the last pair of the common subsequence. Take the best answer for both strings with this character removed (the diagonal neighbour) and add one. Matching here is always at least as good as skipping, so no <code>max</code> is needed on this branch.</p>",
         "diagram": "  i=2 (\"ac\"), j=3 (\"abc\"):  'c' == 'c'\n  dp[2][3] = dp[1][2] + 1 = 1 + 1 = 2\n\n          \"\"   a   b   c   d\n     \"\"    0   0   0   0   0\n     a     0   1   1   1   1\n     c     0   1   1  [2]  ."},
        {"code": "                else:\n                    dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])",
         "explain": "<p>No match, so the two end characters cannot both be in the answer. Either drop the last character of <code>text1</code> (look up) or drop the last of <code>text2</code> (look left), and keep the larger. The diagonal is not needed here because it is never larger than either neighbour.</p>",
         "diagram": "  i=3 (\"acb\"), j=3 (\"abc\"):  'b' != 'c'\n  dp[3][3] = max(dp[2][3], dp[3][2]) = max(2, 2) = 2\n\n          \"\"   a   b   c   d\n     a     0   1   1   1   1\n     c     0   1   1   2   2\n     b     0   1   2  [2]  ."},
        {"code": "        return dp[m][n]",
         "explain": "<p>The bottom-right cell covers the full length of both strings, so it holds the answer. Space could be cut to two rows since each row only reads the one above, but the full table is clearer and well within limits for strings up to 1000 characters.</p>",
         "diagram": "  final table, text1 = \"acbd\", text2 = \"abcd\"\n          \"\"   a   b   c   d\n     \"\"    0   0   0   0   0\n     a     0   1   1   1   1\n     c     0   1   1   2   2\n     b     0   1   2   2   2\n     d     0   1   2   2  [3]   -> return 3"},
    ],
    "complexity": "Time O(m * n), one constant-time step per cell. Space O(m * n) for the table (reducible to O(min(m, n)) with two rolling rows).",
}

TESTS = """
s = Solution()
assert s.longestCommonSubsequence("acbd", "abcd") == 3
assert s.longestCommonSubsequence("xyz", "pq") == 0
assert s.longestCommonSubsequence("abcde", "ace") == 3
assert s.longestCommonSubsequence("abc", "abc") == 3
assert s.longestCommonSubsequence("a", "a") == 1
assert s.longestCommonSubsequence("a", "b") == 0
assert s.longestCommonSubsequence("bsbininm", "jmjkbkjkv") == 1
"""
