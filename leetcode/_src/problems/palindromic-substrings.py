PROBLEM = {
    "slug": "palindromic-substrings", "number": 647, "title": "Palindromic Substrings", "category": "String", "difficulty": "Medium",
    "url": "https://leetcode.com/problems/palindromic-substrings/", "premium": False,
    "statement_html": """<p>Given a string <code>s</code>, count how many of its contiguous substrings are palindromes. Substrings are identified by their position, so the same text appearing at two different places counts twice. Every single character is a palindrome on its own.</p>
<pre>
Input:  s = "xyx"
Output: 4             "x", "y", "x", "xyx"

Input:  s = "zzz"
Output: 6             "z" x3, "zz" x2, "zzz" x1
</pre>
<ul>
  <li>1 &le; len(s) &le; 1000</li>
  <li><code>s</code> consists of lowercase English letters</li>
</ul>""",
    "intro_html": """<p><strong>Expand around every center and count the steps.</strong> Each palindrome has a unique center: a character for odd lengths or a gap between two characters for even lengths. From each of the <code>2n - 1</code> centers we push two pointers outwards; every successful match is one more palindrome. Summing those counts over all centers counts every palindromic substring exactly once in O(n&sup2;) time and O(1) space.</p>""",
    "blocks": [
        {"code": "class Solution:\n    def countSubstrings(self, s: str) -> int:",
         "explain": "<p>LeetCode calls <code>countSubstrings</code> with the string and expects an integer. We never need to materialise the substrings themselves, only count them.</p>",
         "diagram": None},
        {"code": "        total = 0",
         "explain": "<p>The running count of palindromes found. Each center will contribute zero or more to it.</p>",
         "diagram": "  total = 0"},
        {"code": "        def expand(lo: int, hi: int) -> int:\n            count = 0",
         "explain": "<p>A helper that starts from the seed <code>s[lo..hi]</code> and returns how many palindromes are centred there. Each time the window grows by one on each side we have a new, longer palindrome, so the number of successful expansions is the count.</p>",
         "diagram": "  odd center:  lo = hi = i          starts on one character\n  even center: lo = i, hi = i + 1   starts on a gap"},
        {"code": "            while lo >= 0 and hi < len(s) and s[lo] == s[hi]:\n                count += 1\n                lo -= 1\n                hi += 1\n            return count",
         "explain": "<p>While both pointers are in bounds and the characters mirror each other, the window <code>s[lo..hi]</code> is a palindrome: count it and widen. The first mismatch (or the string edge) ends this center for good, because a wider window can never be a palindrome if the inner one is not.</p>",
         "diagram": "  s = \"zzz\"   seed lo=1, hi=1 (odd, centre \"z\")\n  s[1]=z s[1]=z match -> count=1  (\"z\")     lo=0 hi=2\n  s[0]=z s[2]=z match -> count=2  (\"zzz\")   lo=-1 hi=3\n  lo < 0 -> stop, return 2\n\n  seed lo=1, hi=2 (even, gap \"z|z\")\n  s[1]=z s[2]=z match -> count=1  (\"zz\")    lo=0 hi=3\n  hi == 3 -> stop, return 1"},
        {"code": "        for i in range(len(s)):\n            total += expand(i, i)\n            total += expand(i, i + 1)",
         "explain": "<p>Visit every center. <code>expand(i, i)</code> handles palindromes of odd length centred on character <code>i</code>; <code>expand(i, i + 1)</code> handles even lengths centred on the gap after it. The <code>while</code> guard makes the last even seed harmless when <code>i + 1 == len(s)</code>.</p>",
         "diagram": "  s = \"xyx\"\n  i=0: expand(0,0)=1 (\"x\")      expand(0,1)=0 (x != y)\n  i=1: expand(1,1)=2 (\"y\",\"xyx\") expand(1,2)=0 (y != x)\n  i=2: expand(2,2)=1 (\"x\")      expand(2,3)=0 (out of range)\n  total = 1 + 0 + 2 + 0 + 1 + 0 = 4"},
        {"code": "        return total",
         "explain": "<p>Every palindrome has exactly one center, so no substring was counted twice and none was missed. Return the sum.</p>",
         "diagram": "  s = \"zzz\"\n  odd centres:  1 + 2 + 1 = 4      (\"z\", \"z\", \"z\", \"zzz\")\n  even centres: 1 + 1 + 0 = 2      (\"zz\", \"zz\")\n  total = 6"},
    ],
    "complexity": "Time O(n^2): 2n - 1 centers, each expanding at most n/2 steps. Space O(1).",
}

TESTS = """
s = Solution()
assert s.countSubstrings("xyx") == 4
assert s.countSubstrings("zzz") == 6
assert s.countSubstrings("abc") == 3
assert s.countSubstrings("aaa") == 6
assert s.countSubstrings("a") == 1
assert s.countSubstrings("abba") == 6
assert s.countSubstrings("ab") == 2
"""
