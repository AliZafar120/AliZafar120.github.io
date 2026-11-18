PROBLEM = {
    "slug": "number-of-1-bits", "number": 191, "title": "Number of 1 Bits", "category": "Binary", "difficulty": "Easy",
    "url": "https://leetcode.com/problems/number-of-1-bits/", "premium": False,
    "statement_html": """<p>Given a non-negative integer <code>n</code>, return how many bits are set to 1 in its binary representation. This count is also called the Hamming weight or population count.</p>
<pre>
Input:  n = 44         binary 101100
Output: 3

Input:  n = 255        binary 11111111
Output: 8
</pre>
<ul>
  <li>0 &le; n &lt; 2<sup>31</sup></li>
  <li>Only the set bits are counted; leading zeros do not matter</li>
</ul>""",
    "intro_html": """<p><strong>Brian Kernighan's trick: clear the lowest set bit until nothing is left.</strong> The expression <code>n &amp; (n - 1)</code> removes exactly one 1 bit from <code>n</code>, the rightmost one. Each loop iteration therefore handles one set bit, so the loop runs once per 1 bit rather than once per bit position. For sparse numbers this is far fewer than 32 steps.</p>""",
    "blocks": [
        {"code": "class Solution:\n    def hammingWeight(self, n: int) -> int:",
         "explain": "<p>LeetCode calls <code>hammingWeight</code> with the integer and expects the count of 1 bits.</p>",
         "diagram": None},
        {"code": "        count = 0",
         "explain": "<p>The number of 1 bits removed so far. Each iteration of the loop below removes exactly one, so this will end up as the answer.</p>",
         "diagram": "  n = 44 = 101100     count = 0"},
        {"code": "        while n:",
         "explain": "<p>Loop while any bit is still set. An integer is truthy exactly when it is non-zero, so the loop stops the moment the last 1 bit has been cleared.</p>",
         "diagram": None},
        {"code": "            n &= n - 1",
         "explain": "<p>The heart of the method. Subtracting 1 flips the lowest set bit to 0 and turns every bit below it into 1 (that is how borrowing works). ANDing with the original leaves every higher bit unchanged, clears that lowest set bit, and the bits below it were already 0 in <code>n</code>. Net effect: exactly one 1 bit disappears.</p>",
         "diagram": "  n     = 101100\n  n - 1 = 101011     lowest 1 became 0, zeros below it became 1\n  n & (n-1) = 101000 only the lowest set bit is gone"},
        {"code": "            count += 1",
         "explain": "<p>One bit has been cleared, so count it. The loop repeats until <code>n</code> is zero, which takes exactly as many rounds as there were 1 bits.</p>",
         "diagram": "  round   n before   n - 1    n after   count\n    1     101100     101011   101000      1\n    2     101000     100111   100000      2\n    3     100000     011111   000000      3   -> stop"},
        {"code": "        return count",
         "explain": "<p>Three rounds for <code>101100</code>, so the answer is 3. For <code>n = 0</code> the loop never runs and we correctly return 0.</p>",
         "diagram": "  n = 255 = 11111111 -> 8 rounds -> 8\n  n = 0              -> 0 rounds -> 0"},
    ],
    "complexity": "Time O(k) where k is the number of set bits, at most 32. Space O(1).",
}

TESTS = """
s = Solution()
assert s.hammingWeight(44) == 3
assert s.hammingWeight(255) == 8
assert s.hammingWeight(0) == 0
assert s.hammingWeight(1) == 1
assert s.hammingWeight(2**31 - 1) == 31
assert s.hammingWeight(2**30) == 1
assert s.hammingWeight(0b1011) == 3
"""
