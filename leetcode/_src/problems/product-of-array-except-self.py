PROBLEM = {
    "slug": "product-of-array-except-self", "number": 238, "title": "Product of Array Except Self",
    "category": "Array", "difficulty": "Medium",
    "url": "https://leetcode.com/problems/product-of-array-except-self/", "premium": False,
    "statement_html": """<p>Given a list of integers <code>nums</code>, build a new list <code>answer</code> of the same length where <code>answer[i]</code> is the product of every element of <code>nums</code> except <code>nums[i]</code>. You must do it in O(n) time and you may not use division.</p>
<pre>
Input:  nums = [2, 3, 4, 5]
Output: [60, 40, 30, 24]     e.g. answer[1] = 2 * 4 * 5 = 40

Input:  nums = [3, 0, 2]
Output: [0, 6, 0]
</pre>
<ul>
  <li>2 &le; len(nums) &le; 10<sup>5</sup>, -30 &le; nums[i] &le; 30</li>
  <li>Every product fits in a 32-bit integer; division is not allowed</li>
</ul>""",
    "intro_html": """<p><strong>Prefix products from the left, suffix products from the right.</strong> The product of everything except position <code>i</code> is (product of all elements left of <code>i</code>) times (product of all elements right of <code>i</code>). One left-to-right pass writes the left products into the answer array; a second right-to-left pass multiplies in the right products on the fly with a single running variable. No division, O(n) time, and only the output array for storage.</p>""",
    "blocks": [
        {"code": "from typing import List\n\nclass Solution:\n    def productExceptSelf(self, nums: List[int]) -> List[int]:",
         "explain": "<p>LeetCode calls <code>productExceptSelf</code> with the list and expects a new list of the same length.</p>",
         "diagram": None},
        {"code": "        n = len(nums)\n        answer = [1] * n",
         "explain": "<p>The output array, pre-filled with the multiplicative identity 1. It doubles as our scratch space, which is why the solution counts as O(1) extra memory (the output does not count).</p>",
         "diagram": "  nums   = [2, 3, 4, 5]\n  answer = [1, 1, 1, 1]"},
        {"code": "        prefix = 1",
         "explain": "<p>The running product of all elements strictly to the <em>left</em> of the current position. Before index 0 there is nothing on the left, so the product is 1.</p>",
         "diagram": "  prefix = 1      (product of nothing)"},
        {"code": "        for i in range(n):\n            answer[i] = prefix\n            prefix *= nums[i]",
         "explain": "<p>First pass, left to right. At each index we <em>first</em> store the left product (which does not include <code>nums[i]</code>), <em>then</em> fold <code>nums[i]</code> into <code>prefix</code> for the positions that follow. The order of these two lines is what keeps the element itself out of its own answer.</p>",
         "diagram": "  i   prefix before   answer[i]   prefix after\n  0        1             1           1*2 = 2\n  1        2             2           2*3 = 6\n  2        6             6           6*4 = 24\n  3       24            24          24*5 = 120\n  answer = [1, 2, 6, 24]     (left products)"},
        {"code": "        suffix = 1",
         "explain": "<p>Same idea mirrored: the running product of everything strictly to the <em>right</em> of the current position. To the right of the last index there is nothing, so start at 1.</p>",
         "diagram": "  suffix = 1      (nothing to the right of index 3)"},
        {"code": "        for i in range(n - 1, -1, -1):\n            answer[i] *= suffix\n            suffix *= nums[i]",
         "explain": "<p>Second pass, right to left. <code>answer[i]</code> already holds the left product, so multiplying by <code>suffix</code> completes it. Then fold <code>nums[i]</code> into <code>suffix</code> for the positions further left. We never store the suffix products in a second array: the single variable is enough.</p>",
         "diagram": "  i   suffix before   answer[i] = left*suffix   suffix after\n  3        1             24 * 1   = 24             1*5 = 5\n  2        5              6 * 5   = 30             5*4 = 20\n  1       20              2 * 20  = 40            20*3 = 60\n  0       60              1 * 60  = 60            60*2 = 120\n  answer = [60, 40, 30, 24]"},
        {"code": "        return answer",
         "explain": "<p>Each position now holds left product times right product, which is exactly the product of all other elements. Zeros need no special handling: a zero on the left makes every prefix after it 0, and the same happens on the right.</p>",
         "diagram": "  nums = [3, 0, 2]\n  left  products: [1, 3, 0]\n  right products: [0, 2, 1]\n  answer:         [0, 6, 0]"},
    ],
    "complexity": "Time O(n), two passes. Space O(1) extra beyond the output array.",
}

TESTS = """
s = Solution()
assert s.productExceptSelf([2, 3, 4, 5]) == [60, 40, 30, 24]
assert s.productExceptSelf([3, 0, 2]) == [0, 6, 0]
assert s.productExceptSelf([1, 1]) == [1, 1]
assert s.productExceptSelf([0, 0, 4]) == [0, 0, 0]
assert s.productExceptSelf([-1, 2, -3, 4]) == [-24, 12, -8, 6]
assert s.productExceptSelf([5, 7]) == [7, 5]
"""
