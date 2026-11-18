PROBLEM = {
    "slug": "counting-bits", "number": 338, "title": "Counting Bits", "category": "Binary", "difficulty": "Easy",
    "url": "https://leetcode.com/problems/counting-bits/", "premium": False,
    "statement_html": """<p>Given a non-negative integer <code>n</code>, return a list of length <code>n + 1</code> where entry <code>i</code> is the number of 1 bits in the binary form of <code>i</code>, for every <code>i</code> from 0 to <code>n</code>. The whole list should be built in O(n) time, i.e. without counting the bits of each number from scratch.</p>
<pre>
Input:  n = 6
Output: [0, 1, 1, 2, 1, 2, 2]
        0=0  1=1  2=10  3=11  4=100  5=101  6=110

Input:  n = 1
Output: [0, 1]
</pre>
<ul>
  <li>0 &le; n &le; 10<sup>5</sup></li>
  <li>Linear time is expected; a built-in popcount per number is not the intended solution</li>
</ul>""",
    "intro_html": """<p><strong>Dynamic programming on the bit pattern.</strong> Dropping the last bit of <code>i</code> (that is, <code>i &gt;&gt; 1</code>) gives a smaller number whose answer is already in the table, and the dropped bit <code>i &amp; 1</code> is either 0 or 1. So <code>bits[i] = bits[i &gt;&gt; 1] + (i &amp; 1)</code>: one table lookup and one addition per number.</p>""",
    "blocks": [
        {"code": "from typing import List\n\nclass Solution:\n    def countBits(self, n: int) -> List[int]:",
         "explain": "<p>LeetCode calls <code>countBits</code> with <code>n</code> and expects the list of <code>n + 1</code> counts.</p>",
         "diagram": None},
        {"code": "        bits = [0] * (n + 1)",
         "explain": "<p>The table of answers, one slot per number from 0 to <code>n</code>. Slot 0 is already correct: zero has no 1 bits. Every other slot will be filled from a smaller slot, which is why we fill in increasing order.</p>",
         "diagram": "  n = 6\n  i:     0  1  2  3  4  5  6\n  bits: [0, 0, 0, 0, 0, 0, 0]"},
        {"code": "        for i in range(1, n + 1):",
         "explain": "<p>Fill the slots from 1 upwards. When we reach <code>i</code>, every smaller index is already final, and in particular <code>i &gt;&gt; 1</code> is, since it is strictly less than <code>i</code>.</p>",
         "diagram": None},
        {"code": "            bits[i] = bits[i >> 1] + (i & 1)",
         "explain": "<p>Write <code>i</code> in binary. Shifting right by one chops off the last bit, leaving a number we have already counted. The chopped bit, <code>i &amp; 1</code>, is 1 for odd numbers and 0 for even ones. The count of <code>i</code> is the count of the shorter number plus that final bit.</p>",
         "diagram": "  i   binary   i>>1   bits[i>>1]   i&1   bits[i]\n  1      1      0        0          1       1\n  2     10      1        1          0       1\n  3     11      1        1          1       2\n  4    100      2        1          0       1\n  5    101      2        1          1       2\n  6    110      3        2          0       2"},
        {"code": "        return bits",
         "explain": "<p>The table now holds the popcount of every number up to <code>n</code>. Each entry cost O(1), giving O(n) overall.</p>",
         "diagram": "  bits = [0, 1, 1, 2, 1, 2, 2]"},
    ],
    "complexity": "Time O(n), one constant-time step per number. Space O(n) for the output list.",
}

TESTS = """
s = Solution()
assert s.countBits(6) == [0, 1, 1, 2, 1, 2, 2]
assert s.countBits(1) == [0, 1]
assert s.countBits(0) == [0]
assert s.countBits(2) == [0, 1, 1]
assert s.countBits(8) == [0, 1, 1, 2, 1, 2, 2, 3, 1]
assert s.countBits(100) == [bin(i).count("1") for i in range(101)]
"""
