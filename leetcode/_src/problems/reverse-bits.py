PROBLEM = {
    "slug": "reverse-bits", "number": 190, "title": "Reverse Bits", "category": "Binary", "difficulty": "Easy",
    "url": "https://leetcode.com/problems/reverse-bits/", "premium": False,
    "statement_html": """<p>Given a non-negative integer <code>n</code> that represents a 32-bit unsigned value, reverse the order of its 32 bits and return the resulting integer. Bit 0 (the least significant) moves to bit 31, bit 1 moves to bit 30, and so on. Leading zeros count: they become trailing zeros.</p>
<pre>
Input:  n = 6          00000000000000000000000000000110
Output: 1610612736     01100000000000000000000000000000

Input:  n = 1
Output: 2147483648     a single 1 moves from bit 0 to bit 31
</pre>
<ul>
  <li>0 &le; n &lt; 2<sup>32</sup>; the input is treated as exactly 32 bits</li>
  <li>The result is also an unsigned 32-bit value</li>
</ul>""",
    "intro_html": """<p><strong>Peel bits off the right of the input and push them onto the right of the output, 32 times.</strong> Each round takes the lowest bit of <code>n</code>, shifts the partial result left to make room, and drops that bit in. After 32 rounds the first bit we took has been pushed all the way to position 31, which is exactly a reversal. Fixing the count at 32 is what makes leading zeros travel to the far end.</p>""",
    "blocks": [
        {"code": "class Solution:\n    def reverseBits(self, n: int) -> int:",
         "explain": "<p>LeetCode calls <code>reverseBits</code> with the 32-bit value and expects the reversed value as an integer.</p>",
         "diagram": None},
        {"code": "        result = 0",
         "explain": "<p>The reversed number, built up one bit at a time from the left end. It starts empty.</p>",
         "diagram": "  n = 6 = ...0110        result = 0\n  (shown with 8 bits below for readability; real code uses 32)"},
        {"code": "        for _ in range(32):",
         "explain": "<p>Exactly 32 iterations, no more and no fewer, regardless of how big <code>n</code> is. If we stopped when <code>n</code> became zero, the leading zeros of small inputs would never be moved to the low end and the answer would be wrong.</p>",
         "diagram": None},
        {"code": "            result = (result << 1) | (n & 1)",
         "explain": "<p>Shift the partial result left by one to open a new slot at bit 0, then fill that slot with the current lowest bit of <code>n</code>. Bits placed earlier move one step further left every round, which is how the first bit taken ends up at position 31.</p>",
         "diagram": "  8-bit toy, n = 00000110\n  round  n&1   result (after shift and OR)\n    1     0    00000000\n    2     1    00000001\n    3     1    00000011\n    4     0    00000110\n    ...   0    (four more zeros pushed in)\n    8     0    01100000"},
        {"code": "            n >>= 1",
         "explain": "<p>Discard the bit we just copied so the next round sees the next one. After 32 shifts <code>n</code> is zero, having given up every bit in order from lowest to highest.</p>",
         "diagram": "  n: 0110 -> 0011 -> 0001 -> 0000 -> 0000 ..."},
        {"code": "        return result",
         "explain": "<p>For the real 32-bit case, the two set bits of 6 (positions 1 and 2) land at positions 30 and 29, so the answer is <code>2^30 + 2^29 = 1610612736</code>.</p>",
         "diagram": "  n      = 0000 0000 0000 0000 0000 0000 0000 0110\n  result = 0110 0000 0000 0000 0000 0000 0000 0000 = 1610612736"},
    ],
    "complexity": "Time O(1): a fixed 32 iterations. Space O(1).",
}

TESTS = """
s = Solution()
assert s.reverseBits(6) == 1610612736
assert s.reverseBits(1) == 2147483648
assert s.reverseBits(0) == 0
assert s.reverseBits(0xFFFFFFFF) == 0xFFFFFFFF
assert s.reverseBits(0b00000010100101000001111010011100) == 0b00111001011110000010100101000000
assert s.reverseBits(2147483648) == 1
assert s.reverseBits(s.reverseBits(123456789)) == 123456789
"""
