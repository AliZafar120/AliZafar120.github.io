PROBLEM = {
    "slug": "word-break", "number": 139, "title": "Word Break", "category": "Dynamic Programming", "difficulty": "Medium",
    "url": "https://leetcode.com/problems/word-break/", "premium": False,
    "statement_html": """<p>Given a string <code>s</code> and a list of dictionary words, decide whether <code>s</code> can be split into a sequence of one or more dictionary words placed back to back with nothing left over. A word may be reused any number of times.</p>
<pre>
Input:  s = "catsdog", wordDict = ["cats", "dog", "cat"]
Output: True        "cats" + "dog"

Input:  s = "catsan", wordDict = ["cat", "cats", "and"]
Output: False       after "cats" or "cat" nothing matches the rest
</pre>
<ul>
  <li>1 &le; len(s) &le; 300, 1 &le; len(wordDict) &le; 1000</li>
  <li>Words are distinct, all lowercase letters</li>
</ul>""",
    "intro_html": """<p><strong>DP over prefixes.</strong> Let <code>dp[i]</code> be True when the first <code>i</code> characters of <code>s</code> can be fully segmented. A prefix of length <code>i</code> is breakable if some shorter breakable prefix of length <code>j</code> is followed by a dictionary word <code>s[j:i]</code>. Fill the table from the empty prefix up to the whole string; the last entry is the answer. A set makes each word lookup O(1).</p>""",
    "blocks": [
        {"code": "from typing import List\n\nclass Solution:\n    def wordBreak(self, s: str, wordDict: List[str]) -> bool:",
         "explain": "<p>The LeetCode signature: the string to split and the list of allowed words, returning a boolean.</p>",
         "diagram": None},
        {"code": "        words = set(wordDict)",
         "explain": "<p>Convert the list to a set so that asking \"is this substring a word?\" costs O(1) instead of scanning up to 1000 entries every time. The inner loop below asks that question O(n&sup2;) times, so this matters.</p>",
         "diagram": "  wordDict = [\"cats\", \"dog\", \"cat\"]\n  words    = {\"cats\", \"dog\", \"cat\"}     O(1) membership"},
        {"code": "        dp = [False] * (len(s) + 1)\n        dp[0] = True",
         "explain": "<p>One slot per prefix length, 0 through <code>len(s)</code>. <code>dp[0]</code> is the empty prefix, which is trivially segmented (zero words), and it is the anchor every real segmentation grows from. Everything else starts False until proven otherwise.</p>",
         "diagram": "  s = \"catsdog\"\n  i:    0   1   2   3   4   5   6   7\n  dp:   T   F   F   F   F   F   F   F"},
        {"code": "        for i in range(1, len(s) + 1):",
         "explain": "<p>Decide each prefix length in increasing order. When we reach <code>i</code>, every <code>dp[j]</code> for <code>j &lt; i</code> is already final, which is what lets us build on them.</p>",
         "diagram": "  i = 1: \"c\"      i = 4: \"cats\"\n  i = 2: \"ca\"     i = 5: \"catsd\"\n  i = 3: \"cat\"    i = 7: \"catsdog\""},
        {"code": "            for j in range(i):\n                if dp[j] and s[j:i] in words:\n                    dp[i] = True\n                    break",
         "explain": "<p>Try every split point <code>j</code> before <code>i</code>. The prefix up to <code>j</code> must itself be breakable, and the piece from <code>j</code> to <code>i</code> must be a dictionary word. One success is enough, so <code>break</code> as soon as we find it. Checking <code>dp[j]</code> first short-circuits and avoids building the substring for dead prefixes.</p>",
         "diagram": "  s = \"catsdog\"\n  i=3: j=0  dp[0]=T  s[0:3]=\"cat\"  in words  -> dp[3]=T\n  i=4: j=0  dp[0]=T  s[0:4]=\"cats\" in words  -> dp[4]=T\n  i=5: j=3  dp[3]=T  s[3:5]=\"sd\"   no\n       j=4  dp[4]=T  s[4:5]=\"d\"    no        -> dp[5]=F\n  i=7: j=3  dp[3]=T  s[3:7]=\"sdog\" no\n       j=4  dp[4]=T  s[4:7]=\"dog\"  in words  -> dp[7]=T"},
        {"code": "        return dp[len(s)]",
         "explain": "<p>The last slot says whether the entire string is breakable. Every True in the table was justified by a real sequence of words, so this is exact, not a heuristic.</p>",
         "diagram": "  s = \"catsdog\"\n  i:    0   1   2   3   4   5   6   7\n  dp:   T   F   F   T   T   F   F   T    -> True\n\n  s = \"catsan\", words = {cat, cats, and}\n  i:    0   1   2   3   4   5   6\n  dp:   T   F   F   T   T   F   F        -> False"},
    ],
    "complexity": "Time O(n^2 * L) where n = len(s) and L is the longest word (slicing); space O(n) for the table plus the word set.",
}

TESTS = """
s = Solution()
assert s.wordBreak("catsdog", ["cats", "dog", "cat"]) is True
assert s.wordBreak("catsan", ["cat", "cats", "and"]) is False
assert s.wordBreak("leetcode", ["leet", "code"]) is True
assert s.wordBreak("applepenapple", ["apple", "pen"]) is True
assert s.wordBreak("catsandog", ["cats", "dog", "sand", "and", "cat"]) is False
assert s.wordBreak("a", ["a"]) is True
assert s.wordBreak("b", ["a"]) is False
assert s.wordBreak("aaaa", ["aa"]) is True
"""
