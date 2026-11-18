PROBLEM = {
    "slug": "valid-palindrome", "number": 125, "title": "Valid Palindrome", "category": "String", "difficulty": "Easy",
    "url": "https://leetcode.com/problems/valid-palindrome/", "premium": False,
    "statement_html": """<p>Given a string <code>s</code>, decide whether it reads the same forwards and backwards once you ignore every character that is not a letter or a digit and treat upper and lower case as equal. Spaces, punctuation and symbols are simply skipped.</p>
<pre>
Input:  s = "No lemon, no melon!"
Output: true          cleaned up it is "nolemonnomelon"

Input:  s = "ab_c"
Output: false         cleaned up it is "abc"

Input:  s = ".,"
Output: true          nothing is left, and an empty string is a palindrome
</pre>
<ul>
  <li>1 &le; len(s) &le; 2 &middot; 10<sup>5</sup></li>
  <li><code>s</code> contains printable ASCII characters only</li>
</ul>""",
    "intro_html": """<p><strong>Two pointers that skip the junk.</strong> One index starts at the left end and one at the right end. Each pointer first steps over characters that are not alphanumeric, then the two characters are compared case-insensitively. If they differ the answer is no; otherwise both pointers move inwards. This avoids building a cleaned copy of the string, so it runs in constant extra space.</p>""",
    "blocks": [
        {"code": "class Solution:\n    def isPalindrome(self, s: str) -> bool:",
         "explain": "<p>LeetCode calls <code>isPalindrome</code> with the raw string and expects a boolean. We will work directly on <code>s</code> without creating a filtered copy.</p>",
         "diagram": None},
        {"code": "        i, j = 0, len(s) - 1",
         "explain": "<p>The two pointers: <code>i</code> at the first character, <code>j</code> at the last. They will walk towards each other and meet in the middle.</p>",
         "diagram": "  s = \"No lemon, no melon!\"\n       i                 j\n       0                 18"},
        {"code": "        while i < j:",
         "explain": "<p>Keep going while the pointers have not crossed. When <code>i == j</code> there is a single middle character that trivially matches itself, and once they cross every pair has been checked. Both cases end the loop.</p>",
         "diagram": None},
        {"code": "            while i < j and not s[i].isalnum():\n                i += 1",
         "explain": "<p>Advance the left pointer past anything that is not a letter or digit. <code>str.isalnum</code> does that test for us. The extra <code>i &lt; j</code> guard stops the pointer running off the end when the tail of the string is all punctuation.</p>",
         "diagram": "  s = \"No lemon, no melon!\"\n  i=2 is \" \"  -> skip\n  i=3 is \"l\"  -> stop here"},
        {"code": "            while i < j and not s[j].isalnum():\n                j -= 1",
         "explain": "<p>The mirror image for the right pointer: move left past non-alphanumeric characters. On the first iteration it skips the trailing <code>\"!\"</code>.</p>",
         "diagram": "  s = \"No lemon, no melon!\"\n  j=18 is \"!\"  -> skip\n  j=17 is \"n\"  -> stop here"},
        {"code": "            if s[i].lower() != s[j].lower():\n                return False",
         "explain": "<p>Both pointers now sit on real characters. Compare them after lowering case so that <code>\"N\"</code> and <code>\"n\"</code> count as equal. A single mismatch settles the question, so we return at once.</p>",
         "diagram": "  s = \"ab_c\"\n  i=0 \"a\"   j=3 \"c\"   -> \"a\" != \"c\" -> return False"},
        {"code": "            i += 1\n            j -= 1",
         "explain": "<p>The pair matched, so move both pointers one step inwards. The skipping loops at the top of the <code>while</code> will handle any junk that follows.</p>",
         "diagram": "  s = \"No lemon, no melon!\"\n  pairs compared (after lowering):\n  (0,17) n n   (1,16) o o   (3,15) l l   (4,14) e e\n  (5,13) m m   (6,12) o o   (7,10) n n   (10,10) stop"},
        {"code": "        return True",
         "explain": "<p>The pointers met without finding a mismatch, so every character has a matching partner. This also covers strings whose cleaned version is empty, such as <code>\".,\"</code>: the skipping loops push <code>i</code> up to <code>j</code> and the outer loop ends immediately.</p>",
         "diagram": "  s = \".,\"\n  i=0 j=1   skip \".\" -> i=1   i < j false -> loop ends -> True"},
    ],
    "complexity": "Time O(n): each pointer moves at most n steps in total. Space O(1), no copy of the string is made.",
}

TESTS = """
s = Solution()
assert s.isPalindrome("No lemon, no melon!") is True
assert s.isPalindrome("ab_c") is False
assert s.isPalindrome(".,") is True
assert s.isPalindrome("A man, a plan, a canal: Panama") is True
assert s.isPalindrome("race a car") is False
assert s.isPalindrome("a") is True
assert s.isPalindrome("0P") is False
assert s.isPalindrome("1a1") is True
"""
