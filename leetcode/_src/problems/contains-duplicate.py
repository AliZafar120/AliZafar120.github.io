PROBLEM = {
    "slug": "contains-duplicate", "number": 217, "title": "Contains Duplicate", "category": "Array", "difficulty": "Easy",
    "url": "https://leetcode.com/problems/contains-duplicate/", "premium": False,
    "statement_html": """<p>Given a list of integers <code>nums</code>, decide whether any value occurs more than once. Return <code>True</code> if some value appears at least twice and <code>False</code> if every value is distinct.</p>
<pre>
Input:  nums = [4, 1, 7, 1]
Output: True       1 appears at positions 1 and 3

Input:  nums = [4, 1, 7]
Output: False
</pre>
<ul>
  <li>1 &le; len(nums) &le; 10<sup>5</sup></li>
  <li>Values fit in a signed 32-bit integer</li>
</ul>""",
    "intro_html": """<p><strong>One pass with a hash set.</strong> We walk the list and keep every value we have met in a set. Membership checks on a set are O(1) on average, so the moment we meet a value that is already there we can stop and answer <code>True</code>. Sorting first and comparing neighbours also works but costs O(n log n); the set gives linear time.</p>""",
    "blocks": [
        {"code": "from typing import List\n\nclass Solution:\n    def containsDuplicate(self, nums: List[int]) -> bool:",
         "explain": "<p>LeetCode calls <code>containsDuplicate</code> with the list and expects a boolean.</p>",
         "diagram": None},
        {"code": "        seen = set()",
         "explain": "<p>The set of values met so far. A set is the right container because we only need to ask &quot;have I seen this before?&quot;, never where or how many times, and that question is O(1).</p>",
         "diagram": "  seen = {}          values met so far"},
        {"code": "        for num in nums:",
         "explain": "<p>Visit each value once, in order. Indices are not needed here, so a plain <code>for</code> over the values is enough.</p>",
         "diagram": "  nums = [4, 1, 7, 1]\n  num=4   num=1   num=7   num=1"},
        {"code": "            if num in seen:\n                return True",
         "explain": "<p>If the value is already in the set, some earlier position held the same number: that is a duplicate and we can return immediately without looking at the rest of the list. Early exit is a real saving when the duplicate comes early in a long list.</p>",
         "diagram": "  num=4  seen={}         miss -> add 4\n  num=1  seen={4}        miss -> add 1\n  num=7  seen={4,1}      miss -> add 7\n  num=1  seen={4,1,7}    HIT  -> return True"},
        {"code": "            seen.add(num)",
         "explain": "<p>Not seen before, so remember it for the values still to come. Adding <em>after</em> the check means a value never matches itself.</p>",
         "diagram": "  nums = [4, 1, 7]\n  seen grows: {} -> {4} -> {4,1} -> {4,1,7}, no hit"},
        {"code": "        return False",
         "explain": "<p>The loop finished without a hit, so every value was added exactly once and no duplicates exist.</p>",
         "diagram": None},
    ],
    "complexity": "Time O(n), one pass with O(1) set operations. Space O(n) for the set in the worst case.",
}

TESTS = """
s = Solution()
assert s.containsDuplicate([4, 1, 7, 1]) is True
assert s.containsDuplicate([4, 1, 7]) is False
assert s.containsDuplicate([5]) is False
assert s.containsDuplicate([2, 2, 2]) is True
assert s.containsDuplicate([-1, 0, 1, -1]) is True
assert s.containsDuplicate(list(range(1000))) is False
"""
