PROBLEM = {
    "slug": "longest-repeating-character-replacement", "number": 424, "title": "Longest Repeating Character Replacement", "category": "String", "difficulty": "Medium",
    "url": "https://leetcode.com/problems/longest-repeating-character-replacement/", "premium": False,
    "statement_html": """<p>You are given a string of uppercase letters and an integer <code>k</code>. You may change at most <code>k</code> characters to any other uppercase letter. Return the length of the longest substring that can be turned into a run of one repeated letter using at most <code>k</code> changes.</p>
<pre>
Input:  s = "AABCCBB", k = 2
Output: 5            "BCCBB" -> change the two C's -> "BBBBB"

Input:  s = "ABC", k = 0
Output: 1
</pre>
<ul>
  <li>1 &le; len(s) &le; 10<sup>5</sup>, only uppercase English letters</li>
  <li>0 &le; k &le; len(s)</li>
</ul>""",
    "intro_html": """<p><strong>Sliding window tracking the most frequent letter.</strong> A window is fixable with <code>k</code> changes exactly when <code>window length - count of its most common letter &le; k</code>: keep the majority letter and rewrite everything else. We grow the window from the right, keep letter counts, and shrink from the left whenever the condition breaks. A neat trick lets <code>max_freq</code> never decrease, because a window that was once the best can only be beaten by a longer window with a higher majority count.</p>""",
    "blocks": [
        {"code": "from collections import defaultdict\n\nclass Solution:\n    def characterReplacement(self, s: str, k: int) -> int:",
         "explain": "<p>LeetCode calls <code>characterReplacement</code> with the string and the change budget <code>k</code>, and expects an integer. <code>defaultdict(int)</code> lets us increment a letter's count without checking whether the key exists.</p>",
         "diagram": None},
        {"code": "        count = defaultdict(int)\n        left = 0\n        max_freq = 0\n        best = 0",
         "explain": "<p>Window state. <code>count</code> holds how many of each letter are currently inside <code>s[left..right]</code>. <code>max_freq</code> is the highest single-letter count we have ever observed in any window. <code>best</code> is the longest valid window so far.</p>",
         "diagram": "  s = \"AABCCBB\", k = 2\n  count = {}   left = 0   max_freq = 0   best = 0"},
        {"code": "        for right, ch in enumerate(s):\n            count[ch] += 1",
         "explain": "<p>Extend the window one character to the right and record the new letter. Every character enters the window exactly once.</p>",
         "diagram": "  right=0 A: count = {A:1}\n  right=1 A: count = {A:2}\n  right=2 B: count = {A:2, B:1}"},
        {"code": "            max_freq = max(max_freq, count[ch])",
         "explain": "<p>Only the letter we just added can have raised the maximum, so one comparison keeps <code>max_freq</code> current. Note that we never lower it when letters leave the window. That is deliberate: <code>best</code> can only improve if a future window has a strictly higher majority count, so a stale (too high) <code>max_freq</code> can never produce a window longer than one that was genuinely valid. The answer stays correct and we avoid a 26-letter rescan per step.</p>",
         "diagram": "  right=0 A  count[A]=1 -> max_freq 1\n  right=1 A  count[A]=2 -> max_freq 2\n  right=2 B  count[B]=1 -> max_freq 2\n  right=3 C  count[C]=1 -> max_freq 2"},
        {"code": "            while (right - left + 1) - max_freq > k:\n                count[s[left]] -= 1\n                left += 1",
         "explain": "<p>The number of characters we would have to change is the window size minus the majority count. If that exceeds <code>k</code>, drop characters from the left until it fits. Because the window grew by one and <code>max_freq</code> never drops, this loop runs at most once per step, so the window effectively slides rather than shrinking.</p>",
         "diagram": "  right=3 C  window \"AABC\" len 4, max_freq 2, 4-2=2 <= 2  ok\n  right=4 C  window \"AABCC\" len 5, max_freq 2, 5-2=3 > 2\n             drop s[0]=A -> count[A]=1, left=1\n             window \"ABCC\" len 4, 4-2=2 ok\n  right=5 B  window \"ABCCB\" len 5, max_freq 2, 5-2=3 > 2\n             drop s[1]=A -> count[A]=0, left=2\n             window \"BCCB\" len 4, 4-2=2 ok\n  right=6 B  count[B]=3 -> max_freq 3\n             window \"BCCBB\" len 5, 5-3=2 ok"},
        {"code": "            best = max(best, right - left + 1)",
         "explain": "<p>The window is now valid (fixable within <code>k</code> changes), so its length is a candidate answer.</p>",
         "diagram": "  right: 0  1  2  3  4  5  6\n  len:   1  2  3  4  4  4  5\n  best:  1  2  3  4  4  4  5"},
        {"code": "        return best",
         "explain": "<p>The longest window we ever held is the answer. For <code>\"ABC\"</code> with <code>k = 0</code> every window of length 2 needs one change, so the window keeps sliding at size 1 and <code>best</code> is 1.</p>",
         "diagram": "  \"AABCCBB\", k=2 -> 5   (\"BCCBB\" -> \"BBBBB\")"},
    ],
    "complexity": "Time O(n): each index enters and leaves the window at most once. Space O(1), the count dict has at most 26 keys.",
}

TESTS = """
s = Solution()
assert s.characterReplacement("AABCCBB", 2) == 5
assert s.characterReplacement("ABC", 0) == 1
assert s.characterReplacement("A", 0) == 1
assert s.characterReplacement("AAAA", 2) == 4
assert s.characterReplacement("ABAB", 2) == 4
assert s.characterReplacement("AABABBA", 1) == 4
assert s.characterReplacement("ABCDE", 5) == 5
assert s.characterReplacement("BAAAB", 0) == 3
"""
