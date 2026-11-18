PROBLEM = {
    "slug": "decode-ways", "number": 91, "title": "Decode Ways", "category": "Dynamic Programming", "difficulty": "Medium",
    "url": "https://leetcode.com/problems/decode-ways/", "premium": False,
    "statement_html": """<p>Letters are encoded as numbers: A is 1, B is 2, up to Z is 26, and the codes are written one after another with no separators. Given a string of digits, count how many different letter strings could have produced it. A piece such as "0" or "07" is not a valid code, and a string with no valid decoding has 0 ways.</p>
<pre>
Input:  s = "2611"
Output: 4        2|6|1|1, 26|1|1, 2|6|11, 26|11

Input:  s = "1201"
Output: 1        only 1|20|1, since "01" and a lone "0" are not codes
</pre>
<ul>
  <li>1 &le; len(s) &le; 100, digits only</li>
  <li>s may contain leading zeros (then the answer is 0)</li>
</ul>""",
    "intro_html": """<p><strong>Fibonacci-style DP over positions.</strong> The number of decodings of the first <code>i</code> digits is the number of decodings ending with a one-digit code (valid when the digit is not 0) plus the number ending with a two-digit code (valid when the pair is 10 to 26). Each count depends only on the two previous counts, so two rolling variables replace a full table.</p>""",
    "blocks": [
        {"code": "class Solution:\n    def numDecodings(self, s: str) -> int:",
         "explain": "<p>LeetCode's signature: a digit string in, a count out. Digits are compared as characters throughout, which is fine because single ASCII digits compare the same way as their values.</p>",
         "diagram": None},
        {"code": "        if s[0] == \"0\":\n            return 0",
         "explain": "<p>A leading zero cannot start any code (\"0\" alone is invalid and \"0x\" is not a two-digit code), so nothing can be decoded. Catching it here also lets the loop start from the second character with a known count of 1 for the first.</p>",
         "diagram": "  s = \"0\"     -> 0\n  s = \"012\"   -> 0   (no code starts with 0)"},
        {"code": "        prev, cur = 1, 1",
         "explain": "<p><code>cur</code> is the number of ways to decode the prefix processed so far, <code>prev</code> the number for the prefix one character shorter. After the first digit (which is nonzero) there is exactly one way, and the empty prefix also counts as one way, which is what lets a two-digit code at positions 0 and 1 contribute correctly.</p>",
         "diagram": "  s = \"2611\"\n  prefix:   \"\"    \"2\"\n  ways:      1     1\n            prev  cur"},
        {"code": "        for i in range(1, len(s)):\n            nxt = 0",
         "explain": "<p>Extend the prefix one digit at a time, starting from the second character. <code>nxt</code> accumulates the number of ways to decode the prefix ending at <code>i</code>; it is rebuilt from scratch each iteration from the two cases below.</p>",
         "diagram": "  s = \"2611\":  i = 1 ('6'),  i = 2 ('1'),  i = 3 ('1')"},
        {"code": "            if s[i] != \"0\":\n                nxt += cur",
         "explain": "<p>Case one: digit <code>i</code> is a code on its own. That works for 1 through 9 but not 0, and every decoding of the previous prefix extends to one here, so add <code>cur</code>.</p>",
         "diagram": "  i=1  s[1]='6'  single code \"6\" ok   nxt += cur (1)\n  i=2  s[2]='1'  single code \"1\" ok   nxt += cur (2)\n  (in \"1201\", i=2 s[2]='0' -> a lone 0 is not a code, skip)"},
        {"code": "            if s[i - 1] == \"1\" or (s[i - 1] == \"2\" and s[i] <= \"6\"):\n                nxt += prev",
         "explain": "<p>Case two: digits <code>i - 1</code> and <code>i</code> together form a code from 10 to 26. That happens when the first digit is 1 (10 to 19) or the first is 2 and the second is at most 6 (20 to 26). Then every decoding of the prefix two characters back extends to here, so add <code>prev</code>. Pairs like \"27\" or \"06\" fail this test and add nothing.</p>",
         "diagram": "  i=1  s[0:2]=\"26\"  pair ok (2 and 6<=6)   nxt += prev (1)\n  i=2  s[1:3]=\"61\"  pair not ok (61 > 26)  no change\n  i=3  s[2:4]=\"11\"  pair ok (starts with 1) nxt += prev (2)"},
        {"code": "            prev, cur = cur, nxt",
         "explain": "<p>Slide the window: the current count becomes the previous one, and the freshly computed <code>nxt</code> becomes the current. Only two numbers are kept at any time.</p>",
         "diagram": "  s = \"2611\"\n  start:          prev=1  cur=1\n  i=1 ('6'):  nxt = 1 + 1 = 2    prev=1  cur=2\n  i=2 ('1'):  nxt = 2 + 0 = 2    prev=2  cur=2\n  i=3 ('1'):  nxt = 2 + 2 = 4    prev=2  cur=4"},
        {"code": "        return cur",
         "explain": "<p>After the last digit, <code>cur</code> counts the decodings of the whole string. If an internal zero had no valid partner, <code>nxt</code> became 0 at that step and stays 0 to the end, correctly reporting no decodings.</p>",
         "diagram": "  s = \"1201\"\n  start:          prev=1  cur=1\n  i=1 ('2'):  single ok, \"12\" ok   nxt=1+1=2   prev=1  cur=2\n  i=2 ('0'):  single no, \"20\" ok   nxt=0+1=1   prev=2  cur=1\n  i=3 ('1'):  single ok, \"01\" no   nxt=1+0=1   prev=1  cur=1\n  -> return 1"},
    ],
    "complexity": "Time O(n), one pass over the digits. Space O(1), two rolling counters.",
}

TESTS = """
s = Solution()
assert s.numDecodings("2611") == 4
assert s.numDecodings("1201") == 1
assert s.numDecodings("12") == 2
assert s.numDecodings("226") == 3
assert s.numDecodings("06") == 0
assert s.numDecodings("0") == 0
assert s.numDecodings("10") == 1
assert s.numDecodings("100") == 0
assert s.numDecodings("27") == 1
assert s.numDecodings("1111111111") == 89
"""
