PROBLEM = {
    "slug": "minimum-window-substring", "number": 76, "title": "Minimum Window Substring", "category": "String", "difficulty": "Hard",
    "url": "https://leetcode.com/problems/minimum-window-substring/", "premium": False,
    "statement_html": """<p>Given two strings <code>s</code> and <code>t</code>, find the shortest contiguous substring of <code>s</code> that contains every character of <code>t</code>, counting multiplicity (if <code>t</code> has two <code>a</code>'s the window needs at least two <code>a</code>'s). Return that substring, or the empty string if none exists. The answer is guaranteed to be unique when it exists.</p>
<pre>
Input:  s = "xaybzcab", t = "abc"
Output: "cab"          "aybzc" and "bzca" also qualify but are longer

Input:  s = "a", t = "aa"
Output: ""
</pre>
<ul>
  <li>1 &le; len(s), len(t) &le; 10<sup>5</sup></li>
  <li>Both strings consist of uppercase and lowercase English letters</li>
</ul>""",
    "intro_html": """<p><strong>Sliding window with need and have counters.</strong> <code>need</code> is the multiset of letters required by <code>t</code>. We expand a window over <code>s</code> to the right, counting letters; when a letter's count reaches what <code>need</code> demands we say that letter is \"satisfied\" and bump <code>have</code>. Once <code>have</code> equals the number of distinct required letters the window is valid, so we record it and shrink from the left as far as possible before expanding again. Comparing the two integers <code>have</code> and <code>required</code> replaces a full dictionary comparison at every step.</p>""",
    "blocks": [
        {"code": "from collections import Counter\n\nclass Solution:\n    def minWindow(self, s: str, t: str) -> str:",
         "explain": "<p>LeetCode calls <code>minWindow</code> with the haystack <code>s</code> and the pattern <code>t</code>, expecting the shortest covering substring. <code>Counter</code> builds a letter histogram in one call.</p>",
         "diagram": None},
        {"code": "        if not t or not s:\n            return \"\"",
         "explain": "<p>Nothing to search for, or nothing to search in. Returning early avoids edge cases in the loop.</p>",
         "diagram": None},
        {"code": "        need = Counter(t)\n        window = {}\n        have, required = 0, len(need)",
         "explain": "<p><code>need[ch]</code> is how many of <code>ch</code> the window must contain. <code>window</code> counts what the current window actually holds. <code>required</code> is the number of distinct letters to satisfy, and <code>have</code> counts how many of them are currently satisfied. The window is valid exactly when <code>have == required</code>.</p>",
         "diagram": "  s = \"xaybzcab\", t = \"abc\"\n  need = {a:1, b:1, c:1}   required = 3\n  window = {}              have = 0"},
        {"code": "        best = (float(\"inf\"), 0, 0)\n        left = 0",
         "explain": "<p><code>best</code> remembers the smallest valid window as <code>(length, left, right)</code>, starting at infinity so any real window beats it. We store indices rather than slicing strings inside the loop, which keeps each step O(1).</p>",
         "diagram": "  best = (inf, 0, 0)   left = 0"},
        {"code": "        for right, ch in enumerate(s):\n            window[ch] = window.get(ch, 0) + 1",
         "explain": "<p>Extend the window by one character and count it. Letters that are not in <code>t</code> are counted too, harmlessly; they simply never affect <code>have</code>.</p>",
         "diagram": "  right=0 x  window = {x:1}\n  right=1 a  window = {x:1, a:1}\n  right=2 y  window = {x:1, a:1, y:1}"},
        {"code": "            if ch in need and window[ch] == need[ch]:\n                have += 1",
         "explain": "<p>Did this letter just become satisfied? We test <code>==</code> rather than <code>&gt;=</code> so that <code>have</code> is incremented exactly once per letter, at the moment its count crosses the threshold, not on every surplus copy.</p>",
         "diagram": "  right=1 a  window[a]=1 == need[a]=1 -> have = 1\n  right=3 b  window[b]=1 == need[b]=1 -> have = 2\n  right=5 c  window[c]=1 == need[c]=1 -> have = 3 == required"},
        {"code": "            while have == required:\n                if right - left + 1 < best[0]:\n                    best = (right - left + 1, left, right)",
         "explain": "<p>While the window covers <code>t</code>, it is a candidate: record it if it is the shortest so far. We then try to make it shorter from the left (next block); the loop repeats as long as the window stays valid.</p>",
         "diagram": "  right=5  window s[0..5] = \"xaybzc\" len 6 -> best = (6, 0, 5)"},
        {"code": "                window[s[left]] -= 1\n                if s[left] in need and window[s[left]] < need[s[left]]:\n                    have -= 1\n                left += 1",
         "explain": "<p>Shrink by dropping the leftmost character. If that character was required and its count just fell below what is needed, the window is no longer valid, so <code>have</code> drops and the <code>while</code> ends; otherwise the window is still valid and we record the shorter one on the next iteration. Each index is removed at most once, so the total shrinking work is O(n).</p>",
         "diagram": "  drop x (left=0): not needed              still valid, best=(5,1,5)\n  drop a (left=1): window[a]=0 < 1 -> have=2, left=2, loop ends\n  right=6 a: have=3 -> window s[2..6]=\"ybzca\" len 5, not shorter\n    drop y, drop b -> have=2, left=4\n  right=7 b: have=3 -> window s[4..7]=\"zcab\" len 4 -> best=(4,4,7)\n    drop z -> \"cab\" len 3 -> best=(3,5,7)\n    drop c -> have=2, left=6, done"},
        {"code": "        return \"\" if best[0] == float(\"inf\") else s[best[1]:best[2] + 1]",
         "explain": "<p>If <code>best</code> never changed, no window ever covered <code>t</code> and we return the empty string. Otherwise slice the recorded window out of <code>s</code>, remembering that the right index is inclusive.</p>",
         "diagram": "  best = (3, 5, 7) -> s[5:8] = \"cab\"\n  s = \"a\", t = \"aa\": have never reaches 1 -> best unchanged -> \"\""},
    ],
    "complexity": "Time O(|s| + |t|): each index of s enters the window once and leaves at most once. Space O(|s| + |t|) for the two count dictionaries in the worst case, bounded by the alphabet size in practice.",
}

TESTS = """
s = Solution()
assert s.minWindow("xaybzcab", "abc") == "cab"
assert s.minWindow("a", "aa") == ""
assert s.minWindow("a", "a") == "a"
assert s.minWindow("ab", "b") == "b"
assert s.minWindow("ADOBECODEBANC", "ABC") == "BANC"
assert s.minWindow("aaab", "ab") == "ab"
assert s.minWindow("abc", "d") == ""
assert s.minWindow("aAbB", "Ab") == "Ab"
assert s.minWindow("bbaac", "aab") == "baa"
"""
