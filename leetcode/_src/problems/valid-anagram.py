PROBLEM = {
    "slug": "valid-anagram", "number": 242, "title": "Valid Anagram", "category": "String", "difficulty": "Easy",
    "url": "https://leetcode.com/problems/valid-anagram/", "premium": False,
    "statement_html": """<p>Two strings are anagrams if one can be rearranged into the other, using every character exactly once. Given two lowercase strings <code>s</code> and <code>t</code>, return <code>true</code> if <code>t</code> is an anagram of <code>s</code> and <code>false</code> otherwise.</p>
<pre>
Input:  s = "listen", t = "silent"
Output: true

Input:  s = "aab", t = "abb"
Output: false        s has two a's, t has only one
</pre>
<ul>
  <li>1 &le; len(s), len(t) &le; 5 * 10<sup>4</sup></li>
  <li>Both strings contain only lowercase English letters</li>
</ul>""",
    "intro_html": """<p><strong>Character counting with a 26-slot array.</strong> Two strings are anagrams exactly when every letter occurs the same number of times in both. Instead of sorting (O(n log n)), we walk both strings once, adding one for each letter of <code>s</code> and subtracting one for each letter of <code>t</code>. If every slot ends at zero the counts matched.</p>""",
    "blocks": [
        {"code": "class Solution:\n    def isAnagram(self, s: str, t: str) -> bool:",
         "explain": "<p>LeetCode calls <code>isAnagram</code> with the two strings and expects a boolean.</p>",
         "diagram": None},
        {"code": "        if len(s) != len(t):\n            return False",
         "explain": "<p>Anagrams must have the same length. Checking this first is a cheap early exit and, more importantly, it is what allows us to walk both strings in a single <code>zip</code> below without dropping characters.</p>",
         "diagram": "  s = \"listen\" (6)   t = \"silent\" (6)   -> continue\n  s = \"ab\" (2)       t = \"abc\" (3)      -> False at once"},
        {"code": "        count = [0] * 26",
         "explain": "<p>One counter per lowercase letter, indexed by <code>ord(ch) - ord(\"a\")</code>. A fixed-size list is faster and smaller than a dictionary when the alphabet is known in advance. The slot will hold (occurrences in <code>s</code>) minus (occurrences in <code>t</code>).</p>",
         "diagram": "  index:  0  1  2  3  4 ... 25\n  letter: a  b  c  d  e ... z\n  count: [0, 0, 0, 0, 0 ... 0]"},
        {"code": "        for a, b in zip(s, t):\n            count[ord(a) - ord(\"a\")] += 1\n            count[ord(b) - ord(\"a\")] -= 1",
         "explain": "<p>Process one character from each string per iteration. Letters from <code>s</code> push their slot up, letters from <code>t</code> pull it down. If the strings are anagrams every increment is cancelled by a decrement somewhere in the pass, so the net value of every slot is zero.</p>",
         "diagram": "  s = \"aab\", t = \"abb\"\n  a/a: count[a] +1 -1 = 0\n  a/b: count[a] = 1, count[b] = -1\n  b/b: count[b] -1 +1 = -1 -> ends at count[a]=1, count[b]=-1\n\n  s = \"listen\", t = \"silent\": every letter nets to 0"},
        {"code": "        return all(c == 0 for c in count)",
         "explain": "<p>A slot above zero means <code>s</code> has extra copies of that letter; below zero means <code>t</code> does. Only when all 26 slots are exactly zero do the two strings have identical letter counts.</p>",
         "diagram": "  \"listen\"/\"silent\": count all zeros -> True\n  \"aab\"/\"abb\":       count[a]=1, count[b]=-1 -> False"},
    ],
    "complexity": "Time O(n) for one pass over both strings. Space O(1): the counter array always has 26 entries regardless of input size.",
}

TESTS = """
s = Solution()
assert s.isAnagram("listen", "silent") is True
assert s.isAnagram("aab", "abb") is False
assert s.isAnagram("a", "a") is True
assert s.isAnagram("a", "b") is False
assert s.isAnagram("ab", "abc") is False
assert s.isAnagram("rat", "car") is False
assert s.isAnagram("zzzz", "zzzz") is True
assert s.isAnagram("dormitory", "dirtyroom") is True
"""
