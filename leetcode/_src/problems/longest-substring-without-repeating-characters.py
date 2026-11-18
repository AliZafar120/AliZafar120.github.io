PROBLEM = {
    "slug": "longest-substring-without-repeating-characters", "number": 3, "title": "Longest Substring Without Repeating Characters", "category": "String", "difficulty": "Medium",
    "url": "https://leetcode.com/problems/longest-substring-without-repeating-characters/", "premium": False,
    "statement_html": """<p>Given a string <code>s</code>, return the length of the longest contiguous substring in which no character appears more than once. Only the length is needed, not the substring itself.</p>
<pre>
Input:  s = "dvdfe"
Output: 4            "vdfe"

Input:  s = "abba"
Output: 2            "ab" or "ba"

Input:  s = ""
Output: 0
</pre>
<ul>
  <li>0 &le; len(s) &le; 5 * 10<sup>4</sup></li>
  <li><code>s</code> may contain letters, digits, symbols and spaces</li>
</ul>""",
    "intro_html": """<p><strong>Sliding window with a last-seen index map.</strong> Maintain a window <code>s[left..right]</code> that contains no repeats. As <code>right</code> advances, a dictionary tells us where the new character was last seen; if that position lies inside the window, we jump <code>left</code> to just past it, in one move rather than one step at a time. The window never shrinks below a valid state and each character is handled once.</p>""",
    "blocks": [
        {"code": "class Solution:\n    def lengthOfLongestSubstring(self, s: str) -> int:",
         "explain": "<p>LeetCode calls <code>lengthOfLongestSubstring</code> with the string and expects an integer length.</p>",
         "diagram": None},
        {"code": "        last_seen = {}",
         "explain": "<p>Maps each character to the <strong>index of its most recent occurrence</strong>. This is what lets us relocate the window's left edge in O(1) instead of scanning backwards to find the duplicate.</p>",
         "diagram": "  last_seen = {}        char -> most recent index"},
        {"code": "        left = 0\n        best = 0",
         "explain": "<p><code>left</code> is the start of the current duplicate-free window. <code>best</code> is the longest window length seen so far; starting at 0 covers the empty string.</p>",
         "diagram": "  s = \"dvdfe\"\n  left = 0, best = 0"},
        {"code": "        for right, ch in enumerate(s):",
         "explain": "<p>The right edge of the window sweeps across the string exactly once. Each new character <code>ch</code> is a candidate to extend the window.</p>",
         "diagram": "  right: 0    1    2    3    4\n  ch:    d    v    d    f    e"},
        {"code": "            if ch in last_seen and last_seen[ch] >= left:\n                left = last_seen[ch] + 1",
         "explain": "<p>Is <code>ch</code> already inside the window? It is in the dict if we have ever seen it, but that earlier copy only matters when its index is at or after <code>left</code>. The check <code>&gt;= left</code> is the subtle part: an occurrence to the left of the window was already excluded and must not drag <code>left</code> backwards. When there is a live duplicate, jump <code>left</code> to just past it.</p>",
         "diagram": "  s = \"abba\"\n  right=0 a: not seen                         left=0\n  right=1 b: not seen                         left=0\n  right=2 b: last_seen[b]=1 >= 0 -> left=2\n  right=3 a: last_seen[a]=0 < 2  -> stale, left stays 2\n  (without the >= check, left would wrongly jump to 1)"},
        {"code": "            last_seen[ch] = right",
         "explain": "<p>Record this occurrence as the newest one. Done after the duplicate check so we compare against the <em>previous</em> position, not the one we are adding now.</p>",
         "diagram": "  s = \"dvdfe\"\n  right=0 d: last_seen = {d:0}\n  right=1 v: last_seen = {d:0, v:1}\n  right=2 d: dup at 0 -> left=1,  last_seen = {d:2, v:1}\n  right=3 f: last_seen = {d:2, v:1, f:3}\n  right=4 e: last_seen = {d:2, v:1, f:3, e:4}"},
        {"code": "            best = max(best, right - left + 1)",
         "explain": "<p>The window <code>s[left..right]</code> is now guaranteed duplicate-free, so its length is a valid candidate. Taking the max after every step means we never need to track the best window's position, just its size.</p>",
         "diagram": "  right=0  window [0,0] \"d\"     len 1  best 1\n  right=1  window [0,1] \"dv\"    len 2  best 2\n  right=2  window [1,2] \"vd\"    len 2  best 2\n  right=3  window [1,3] \"vdf\"   len 3  best 3\n  right=4  window [1,4] \"vdfe\"  len 4  best 4"},
        {"code": "        return best",
         "explain": "<p>After the sweep, <code>best</code> holds the maximum window length. For the empty string the loop body never runs and 0 is returned.</p>",
         "diagram": None},
    ],
    "complexity": "Time O(n): right moves n times and left only jumps forward. Space O(min(n, alphabet)) for the dictionary.",
}

TESTS = """
s = Solution()
assert s.lengthOfLongestSubstring("dvdfe") == 4
assert s.lengthOfLongestSubstring("abba") == 2
assert s.lengthOfLongestSubstring("") == 0
assert s.lengthOfLongestSubstring("aaaa") == 1
assert s.lengthOfLongestSubstring("x") == 1
assert s.lengthOfLongestSubstring("tmmzuxt") == 5
assert s.lengthOfLongestSubstring("abcdef") == 6
assert s.lengthOfLongestSubstring("a b a") == 3
"""
