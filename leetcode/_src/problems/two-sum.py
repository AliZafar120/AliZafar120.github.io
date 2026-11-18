PROBLEM = {
    "slug": "two-sum", "number": 1, "title": "Two Sum", "category": "Array", "difficulty": "Easy",
    "url": "https://leetcode.com/problems/two-sum/", "premium": False,
    "statement_html": """<p>You are given a list of integers <code>nums</code> and a target integer. Exactly one pair of positions holds two numbers that add up to the target. Return those two indices, in any order. The same position may not be used twice.</p>
<pre>
Input:  nums = [3, 8, 11, 2], target = 10
Output: [1, 3]        because nums[1] + nums[3] = 8 + 2 = 10

Input:  nums = [5, 5], target = 10
Output: [0, 1]
</pre>
<ul>
  <li>2 &le; len(nums) &le; 10<sup>4</sup>, values and target fit in a 32-bit integer</li>
  <li>Exactly one valid answer exists</li>
</ul>""",
    "intro_html": """<p><strong>One pass with a hash map.</strong> As we walk the list we remember every number we have seen together with its index. For each new number we ask the map whether its partner, <code>target - num</code>, has already appeared. Checking a dict is O(1), so the whole thing is a single linear pass instead of the O(n&sup2;) pair-by-pair search.</p>""",
    "blocks": [
        {"code": "from typing import List\n\nclass Solution:\n    def twoSum(self, nums: List[int], target: int) -> List[int]:",
         "explain": "<p>LeetCode calls the method <code>twoSum</code> on an instance of <code>Solution</code>. It receives the list and the target and must return a list of two indices.</p>",
         "diagram": None},
        {"code": "        seen = {}",
         "explain": "<p>The memory of the walk: a dictionary from <strong>value</strong> to the <strong>index where it appeared</strong>. It starts empty and grows by one entry per element. Looking up a key is O(1) on average, which is the whole point.</p>",
         "diagram": "  seen = {}          value -> index"},
        {"code": "        for i, num in enumerate(nums):",
         "explain": "<p>Visit every element once, with its position. <code>enumerate</code> hands us both at the same time, which we need because the answer is made of indices, not values.</p>",
         "diagram": "  nums = [3, 8, 11, 2], target = 10\n  i=0 num=3   i=1 num=8   i=2 num=11   i=3 num=2"},
        {"code": "            need = target - num",
         "explain": "<p>The <strong>partner</strong> this number would need. If <code>num + x = target</code> then <code>x = target - num</code>. Computing it lets us ask one direct question instead of scanning the list for a match.</p>",
         "diagram": "  num = 8, target = 10  ->  need = 2"},
        {"code": "            if need in seen:\n                return [seen[need], i]",
         "explain": "<p>Has the partner already been seen? If so, we are done: the earlier index comes from the map and the current index is <code>i</code>. Because we only look <em>backwards</em>, the two indices are always different, which rules out using the same element twice.</p>",
         "diagram": "  i=0 num=3  need=7  seen={}            miss -> store 3\n  i=1 num=8  need=2  seen={3:0}         miss -> store 8\n  i=2 num=11 need=-1 seen={3:0,8:1}     miss -> store 11\n  i=3 num=2  need=8  seen={3:0,8:1,11:2} HIT  -> [seen[8], 3] = [1, 3]"},
        {"code": "            seen[num] = i",
         "explain": "<p>Not found yet, so remember this number for the elements still to come. Storing <em>after</em> the check is what makes <code>[5, 5]</code> work: the second 5 finds the first, but a number never pairs with itself.</p>",
         "diagram": "  nums = [5, 5], target = 10\n  i=0 num=5 need=5 seen={}     miss -> seen={5:0}\n  i=1 num=5 need=5 seen={5:0}  HIT  -> [0, 1]"},
        {"code": "        return []",
         "explain": "<p>Never reached when the input is valid, since one answer is guaranteed. It keeps the function total and the type checker quiet.</p>",
         "diagram": None},
    ],
    "complexity": "Time O(n), one pass. Space O(n) for the map in the worst case.",
}

TESTS = """
s = Solution()
assert sorted(s.twoSum([3, 8, 11, 2], 10)) == [1, 3]
assert sorted(s.twoSum([5, 5], 10)) == [0, 1]
assert sorted(s.twoSum([2, 7, 11, 15], 9)) == [0, 1]
assert sorted(s.twoSum([-1, 4, 3], 2)) == [0, 2]
r = s.twoSum([1, 2, 3, 4, 5, 6], 11); assert len(r) == 2 and r[0] != r[1] and [1,2,3,4,5,6][r[0]] + [1,2,3,4,5,6][r[1]] == 11
"""
