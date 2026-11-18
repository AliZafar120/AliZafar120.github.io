PROBLEM = {
    "slug": "sum-of-two-integers", "number": 371, "title": "Sum of Two Integers", "category": "Binary", "difficulty": "Medium",
    "url": "https://leetcode.com/problems/sum-of-two-integers/", "premium": False,
    "statement_html": """<p>Return the sum of two integers <code>a</code> and <code>b</code> without using the <code>+</code> or <code>-</code> operators anywhere in your code. Both inputs and the result fit in a signed 32-bit integer, so negative numbers must be handled correctly.</p>
<pre>
Input:  a = 5, b = 3
Output: 8

Input:  a = -2, b = 1
Output: -1
</pre>
<ul>
  <li>-1000 &le; a, b &le; 1000</li>
  <li>The operators <code>+</code> and <code>-</code> are forbidden; bit operators are allowed</li>
</ul>""",
    "intro_html": """<p><strong>Bitwise addition: XOR for the digit sums, AND shifted left for the carries.</strong> Adding two bits gives <code>a ^ b</code> as the result bit and <code>a &amp; b</code> as the carry into the next column, so we repeatedly replace <code>(a, b)</code> with <code>(a ^ b, (a &amp; b) &lt;&lt; 1)</code> until there is no carry left. Python integers have unlimited width, so a negative number's sign bits would stretch forever and the carry would never die out; we therefore mask everything to 32 bits and convert back to a signed value at the end.</p>""",
    "blocks": [
        {"code": "class Solution:\n    def getSum(self, a: int, b: int) -> int:",
         "explain": "<p>LeetCode calls <code>getSum</code> with the two integers and expects their sum. No <code>+</code> or <code>-</code> appears below.</p>",
         "diagram": None},
        {"code": "        MASK = 0xFFFFFFFF",
         "explain": "<p>Thirty-two one bits. ANDing with it throws away everything above bit 31, which simulates the fixed-width registers of C or Java. In Python <code>-2</code> is conceptually an infinite string of ones ending in <code>...1110</code>; after the mask it becomes the 32-bit pattern <code>0xFFFFFFFE</code>, a plain positive number we can safely loop on.</p>",
         "diagram": "  MASK     = 1111 1111 1111 1111 1111 1111 1111 1111  (32 ones)\n  -2       = ...1111 1111 1110                        (infinite ones)\n  -2 & MASK= 1111 1111 1111 1111 1111 1111 1111 1110  = 0xFFFFFFFE"},
        {"code": "        MAX_INT = 0x7FFFFFFF",
         "explain": "<p>The largest positive 32-bit signed value, <code>2^31 - 1</code>. Any masked result above it has bit 31 set, which in two's complement means the true answer is negative. We will use this to decide whether to convert back.</p>",
         "diagram": "  MAX_INT  = 0111 1111 1111 1111 1111 1111 1111 1111\n  bit 31 clear -> non-negative, bit 31 set -> negative"},
        {"code": "        while b != 0:",
         "explain": "<p>Keep going while there is still a carry to add in. Because <code>b</code> is masked to 32 bits and shifts left by one each round, the loop ends after at most 32 iterations.</p>",
         "diagram": None},
        {"code": "            carry = ((a & b) << 1) & MASK",
         "explain": "<p>A column produces a carry exactly when both bits are 1, which is <code>a &amp; b</code>. The carry belongs to the next column up, hence the shift left. Masking drops a carry out of bit 31, exactly as 32-bit hardware would overflow silently.</p>",
         "diagram": "  a = 5 = 0101\n  b = 3 = 0011\n  a & b  = 0001  -> << 1 -> carry = 0010"},
        {"code": "            a = (a ^ b) & MASK",
         "explain": "<p>XOR is addition without carry: 1+0 and 0+1 give 1, while 0+0 and 1+1 give 0 (the 1+1 carry was captured separately). This is the partial sum; the mask keeps it inside 32 bits.</p>",
         "diagram": "  a = 0101\n  b = 0011\n  a ^ b = 0110  -> a = 6   (5 + 3 with the carry still pending)"},
        {"code": "            b = carry",
         "explain": "<p>The pending carry becomes the new second operand, and the next iteration adds it into the partial sum in the same way. The process is finished when no carry remains.</p>",
         "diagram": "  round   a        b        a^b      (a&b)<<1\n    1     0101     0011     0110     0010\n    2     0110     0010     0100     0100\n    3     0100     0100     0000     1000\n    4     0000     1000     1000     0000  -> b = 0, stop\n  a = 1000 = 8"},
        {"code": "        return a if a <= MAX_INT else ~(a ^ MASK)",
         "explain": "<p>If bit 31 is clear, <code>a</code> is already the answer. Otherwise the 32-bit pattern represents a negative number. <code>a ^ MASK</code> flips the low 32 bits (giving the pattern's complement as a small positive number) and <code>~</code> then flips all bits of the Python integer, yielding exactly the negative value the pattern encodes, with no <code>-</code> operator involved.</p>",
         "diagram": "  a = -2, b = 1:\n  round 1: a&b = ...1110 & 0001 = 0 -> carry 0\n           a = (-2 ^ 1) & MASK = 0xFFFFFFFF, b = 0\n  0xFFFFFFFF > MAX_INT -> negative\n  a ^ MASK = 0x00000000 = 0,  ~0 = -1   -> answer -1"},
    ],
    "complexity": "Time O(1): at most 32 iterations regardless of input. Space O(1).",
}

TESTS = """
s = Solution()
assert s.getSum(5, 3) == 8
assert s.getSum(-2, 1) == -1
assert s.getSum(0, 0) == 0
assert s.getSum(-1, -1) == -2
assert s.getSum(1000, -1000) == 0
assert s.getSum(-7, -9) == -16
assert s.getSum(123, 877) == 1000
import random
for _ in range(200):
    x, y = random.randint(-1000, 1000), random.randint(-1000, 1000)
    assert s.getSum(x, y) == x + y
"""
