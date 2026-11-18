PROBLEM = {
    "slug": "longest-palindromic-substring", "number": 5, "title": "Longest Palindromic Substring", "category": "String", "difficulty": "Medium",
    "url": "https://leetcode.com/problems/longest-palindromic-substring/", "premium": False,
    "statement_html": """<p>Given a string <code>s</code>, return the longest contiguous substring of <code>s</code> that reads the same forwards and backwards. If several palindromes share the maximum length, any one of them is accepted.</p>
<pre>
Input:  s = "forgeeksskeeg"
Output: "geeksskeeg"

Input:  s = "abc"
Output: "a"           (or "b" or "c"; every single character is a palindrome)
</pre>
<ul>
  <li>1 &le; len(s) &le; 1000</li>
  <li><code>s</code> consists of digits and English letters</li>
</ul>""",
    "intro_html": """<p><strong>Expand around every center.</strong> A palindrome is symmetric about its middle, so each palindrome in <code>s</code> is determined by a center and how far it can grow. There are <code>2n - 1</code> possible centers: each character (odd length) and each gap between two characters (even length). For each one we push two pointers outwards while the characters match, and keep the widest result. That is O(n&sup2;) in the worst case but needs only O(1) extra space and beats the O(n&sup2;) DP table on both memory and simplicity.</p>""",
    "blocks": [
        {"code": "class Solution:\n    def longestPalindrome(self, s: str) -> str:",
         "explain": "<p>LeetCode calls <code>longestPalindrome</code> with the string and expects the substring itself, not its length. We will track the best window as a pair of slice bounds.</p>",
         "diagram": None},
        {"code": "        start, end = 0, 0",
         "explain": "<p>The best palindrome found so far, stored as the half-open slice <code>s[start:end]</code>. It begins empty; the very first expansion will replace it with at least a single character.</p>",
         "diagram": "  s = \"forgeeksskeeg\"\n  start=0 end=0   -> s[0:0] = \"\"  (length 0)"},
        {"code": "        def expand(lo: int, hi: int) -> None:\n            nonlocal start, end",
         "explain": "<p>A helper that grows a palindrome outward from the seed <code>s[lo..hi]</code>. It is a closure so it can read <code>s</code> and update the shared <code>start</code>/<code>end</code>; <code>nonlocal</code> is what lets it assign to those outer variables instead of making local ones.</p>",
         "diagram": "  odd seed:  lo = hi = i          s[i] alone\n  even seed: lo = i, hi = i + 1   the gap between s[i] and s[i+1]"},
        {"code": "            while lo >= 0 and hi < len(s) and s[lo] == s[hi]:\n                lo -= 1\n                hi += 1",
         "explain": "<p>Push the two pointers apart while they stay inside the string and the characters mirror each other. When the loop stops, the pointers have gone <em>one step too far</em>: the palindrome is <code>s[lo+1 .. hi-1]</code>.</p>",
         "diagram": "  s = \"forgeeksskeeg\"   seed lo=6, hi=7 (the gap \"k|s\")\n  s[6]=k s[7]=s  -> mismatch, stop at once\n\n  seed lo=7, hi=8 (the gap \"s|s\")\n  s[7]=s s[8]=s  match -> lo=6 hi=9\n  s[6]=k s[9]=k  match -> lo=5 hi=10\n  s[5]=e s[10]=e match -> lo=4 hi=11\n  s[4]=e s[11]=e match -> lo=3 hi=12\n  s[3]=g s[12]=g match -> lo=2 hi=13\n  hi=13 == len(s)  -> stop; palindrome is s[3:13]"},
        {"code": "            if hi - lo - 1 > end - start:\n                start, end = lo + 1, hi",
         "explain": "<p>The palindrome length is <code>hi - lo - 1</code> because both pointers overshot by one. If it beats the current record we store the slice bounds <code>lo + 1</code> and <code>hi</code>, which match Python slicing exactly.</p>",
         "diagram": "  lo=2, hi=13  -> length 13 - 2 - 1 = 10\n  previous best: end - start = 1\n  10 > 1  -> start, end = 3, 13   (s[3:13] = \"geeksskeeg\")"},
        {"code": "        for i in range(len(s)):\n            expand(i, i)\n            expand(i, i + 1)",
         "explain": "<p>Try every center. <code>expand(i, i)</code> seeds an odd-length palindrome on character <code>i</code>; <code>expand(i, i + 1)</code> seeds an even-length one on the gap after it. When <code>i + 1</code> is out of range the <code>while</code> condition fails immediately, so no bounds check is needed here.</p>",
         "diagram": "  s = \"abc\"\n  i=0: expand(0,0) -> \"a\" len 1 -> best = s[0:1]\n       expand(0,1) -> a != b, len 0\n  i=1: expand(1,1) -> \"b\" len 1, not longer\n       expand(1,2) -> b != c, len 0\n  i=2: expand(2,2) -> \"c\" len 1, not longer\n       expand(2,3) -> hi out of range, len 0"},
        {"code": "        return s[start:end]",
         "explain": "<p>Slice out the recorded window. Because every single character was tried as an odd center, the result is never empty for a non-empty input.</p>",
         "diagram": "  s = \"forgeeksskeeg\"   start=3 end=13 -> \"geeksskeeg\""},
    ],
    "complexity": "Time O(n^2): 2n - 1 centers, each expanding at most n/2 steps. Space O(1) beyond the output slice.",
}

TESTS = """
s = Solution()
assert s.longestPalindrome("forgeeksskeeg") == "geeksskeeg"
assert s.longestPalindrome("abc") in ("a", "b", "c")
assert s.longestPalindrome("babad") in ("bab", "aba")
assert s.longestPalindrome("cbbd") == "bb"
assert s.longestPalindrome("a") == "a"
assert s.longestPalindrome("aaaa") == "aaaa"
assert s.longestPalindrome("racecarxyz") == "racecar"
assert s.longestPalindrome("ab") in ("a", "b")
"""
