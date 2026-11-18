PROBLEM = {
    "slug": "search-in-rotated-sorted-array", "number": 33, "title": "Search in Rotated Sorted Array",
    "category": "Array", "difficulty": "Medium",
    "url": "https://leetcode.com/problems/search-in-rotated-sorted-array/", "premium": False,
    "statement_html": """<p>A list of <em>distinct</em> integers was sorted in increasing order and then rotated at some unknown position, so for example <code>[1, 3, 5, 6, 8, 10]</code> may have become <code>[6, 8, 10, 1, 3, 5]</code>. Given the rotated list and a <code>target</code>, return the index of <code>target</code>, or -1 if it is not present. The solution must run in O(log n).</p>
<pre>
Input:  nums = [6, 8, 10, 1, 3, 5], target = 3
Output: 4

Input:  nums = [9, 1, 3, 5, 7], target = 4
Output: -1
</pre>
<ul>
  <li>1 &le; len(nums) &le; 5000, all values distinct</li>
  <li>The list was sorted ascending before rotation; O(log n) is required</li>
</ul>""",
    "intro_html": """<p><strong>Modified binary search.</strong> Whichever way the list is rotated, at least one of the two halves around the midpoint is properly sorted, and we can tell which by comparing <code>nums[lo]</code> with <code>nums[mid]</code>. Inside a sorted half a simple range check tells us whether the target can be there. So at every step we decide which half to discard and keep halving, just like an ordinary binary search.</p>""",
    "blocks": [
        {"code": "from typing import List\n\nclass Solution:\n    def search(self, nums: List[int], target: int) -> int:",
         "explain": "<p>LeetCode calls <code>search</code> with the rotated list and the target and expects an index or -1.</p>",
         "diagram": None},
        {"code": "        lo, hi = 0, len(nums) - 1",
         "explain": "<p>The inclusive search window. The target, if present, is always inside <code>nums[lo..hi]</code>.</p>",
         "diagram": "  nums = [6, 8, 10, 1, 3, 5]   target = 3\n  index   0  1   2  3  4  5\n          lo              hi"},
        {"code": "        while lo <= hi:",
         "explain": "<p>Standard binary search loop. We use <code>&lt;=</code> because a window of one element still has to be checked against the target.</p>",
         "diagram": None},
        {"code": "            mid = (lo + hi) // 2",
         "explain": "<p>The middle index. We will compare the target against <code>nums[mid]</code> and against the ends of whichever half is sorted.</p>",
         "diagram": "  lo=0, hi=5 -> mid=2   nums[mid]=10"},
        {"code": "            if nums[mid] == target:\n                return mid",
         "explain": "<p>Found it. Values are distinct, so this is the only valid index and we can return at once.</p>",
         "diagram": None},
        {"code": "            if nums[lo] <= nums[mid]:",
         "explain": "<p>Decide which half is sorted. If the leftmost value is not larger than the middle one, there is no rotation drop between them, so <code>nums[lo..mid]</code> is in increasing order. (If the drop were in that range, <code>nums[lo]</code> would be bigger than <code>nums[mid]</code>.)</p>",
         "diagram": "  [6, 8, 10, 1, 3, 5]    nums[lo]=6 <= nums[mid]=10\n   lo     mid       hi   -> left half [6, 8, 10] is sorted"},
        {"code": "                if nums[lo] <= target < nums[mid]:\n                    hi = mid - 1\n                else:\n                    lo = mid + 1",
         "explain": "<p>With the left half sorted, the target is in it exactly when it falls between <code>nums[lo]</code> and <code>nums[mid]</code>. If so, discard the right half; otherwise the target must be in the (possibly unsorted) right half, so discard the left.</p>",
         "diagram": "  target=3:  6 <= 3 < 10 ?  no  -> lo = mid+1 = 3\n  [6, 8, 10, 1, 3, 5]\n              lo    hi\n  lo=3, hi=5 -> mid=4   nums[4]=3 == target -> return 4"},
        {"code": "            else:",
         "explain": "<p>Otherwise <code>nums[lo] &gt; nums[mid]</code>, meaning the rotation drop is in the left half, and therefore the right half <code>nums[mid..hi]</code> is the sorted one.</p>",
         "diagram": "  nums = [9, 1, 3, 5, 7]  target = 7\n  lo=0, hi=4, mid=2:  nums[lo]=9 > nums[mid]=3\n  -> right half [3, 5, 7] is sorted"},
        {"code": "                if nums[mid] < target <= nums[hi]:\n                    lo = mid + 1\n                else:\n                    hi = mid - 1",
         "explain": "<p>Mirror image of the previous step: the target is in the sorted right half exactly when it lies between <code>nums[mid]</code> and <code>nums[hi]</code>. Keep that half if so, otherwise keep the left.</p>",
         "diagram": "  target=7:  3 < 7 <= 7 ?  yes -> lo = mid+1 = 3\n  lo=3, hi=4, mid=3: nums[3]=5 != 7, 5 <= 5 so left sorted,\n             5 <= 7 < 5 ? no -> lo = 4\n  lo=4, hi=4, mid=4: nums[4]=7 == target -> return 4"},
        {"code": "        return -1",
         "explain": "<p>The window became empty without a match, so the target is not in the list.</p>",
         "diagram": "  nums = [9, 1, 3, 5, 7]  target = 4\n  mid=2 (3): right sorted, 3 < 4 <= 7 -> lo=3\n  mid=3 (5): left sorted,  5 <= 4 < 5 ? no -> lo=4\n  mid=4 (7): left sorted,  7 <= 4 < 7 ? no -> lo=5 > hi -> -1"},
    ],
    "complexity": "Time O(log n), the window halves each step. Space O(1).",
}

TESTS = """
s = Solution()
assert s.search([6, 8, 10, 1, 3, 5], 3) == 4
assert s.search([9, 1, 3, 5, 7], 4) == -1
assert s.search([9, 1, 3, 5, 7], 7) == 4
assert s.search([9, 1, 3, 5, 7], 9) == 0
assert s.search([1], 1) == 0
assert s.search([1], 2) == -1
assert s.search([4, 5, 6, 7, 0, 1, 2], 0) == 4
assert s.search([4, 5, 6, 7, 0, 1, 2], 3) == -1
assert s.search([1, 3], 3) == 1
"""
