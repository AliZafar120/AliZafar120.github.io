PROBLEM = {
    "slug": "longest-consecutive-sequence", "number": 128, "title": "Longest Consecutive Sequence", "category": "Graph", "difficulty": "Medium",
    "url": "https://leetcode.com/problems/longest-consecutive-sequence/", "premium": False,
    "statement_html": """<p>Given an unsorted list of integers, find the length of the longest run of consecutive values that all appear somewhere in the list. The values do not have to be adjacent in the input, and duplicates do not make a run longer. Your algorithm must run in O(n) time, so sorting is off the table.</p>
<pre>
Input:  nums = [50, 3, 2, 100, 4, 1]
Output: 4            the run 1, 2, 3, 4

Input:  nums = [7, 7, 7]
Output: 1
</pre>
<ul>
  <li>0 &le; len(nums) &le; 10<sup>5</sup></li>
  <li>-10<sup>9</sup> &le; nums[i] &le; 10<sup>9</sup></li>
</ul>""",
    "intro_html": """<p><strong>Hash set, and only start counting at the head of a run.</strong> Put every number in a set so membership is O(1). Then, for each number, ask whether <code>num - 1</code> is also present: if it is, this number sits in the middle of a run and somebody else will count that run from its true start. Only from a run's head do we walk forward <code>num + 1, num + 2, ...</code> until the set runs out. Every element is walked at most once in total, which keeps the whole thing linear.</p>""",
    "blocks": [
        {"code": "from typing import List\n\nclass Solution:\n    def longestConsecutive(self, nums: List[int]) -> int:",
         "explain": "<p>LeetCode calls <code>longestConsecutive</code> with the integer list and expects the length of the longest run as an int.</p>",
         "diagram": None},
        {"code": "        num_set = set(nums)",
         "explain": "<p>Convert the list to a set. This removes duplicates for free and, more importantly, turns \"is <code>x</code> in the input\" into an O(1) question. Everything below relies on that.</p>",
         "diagram": "  nums    = [50, 3, 2, 100, 4, 1]\n  num_set = {1, 2, 3, 4, 50, 100}"},
        {"code": "        best = 0",
         "explain": "<p>The longest run found so far. Starting at 0 also handles the empty input, where the loop never runs.</p>",
         "diagram": None},
        {"code": "        for num in num_set:\n            if num - 1 in num_set:\n                continue",
         "explain": "<p>Iterate over the set rather than the list so duplicates are visited once. The key trick: if <code>num - 1</code> exists, <code>num</code> is <em>not</em> the start of its run, so skip it. The run will be counted exactly once, from its smallest member. Without this check we would re-walk the same run from every member and the algorithm would become O(n&sup2;) on a long sorted input.</p>",
         "diagram": "  num = 2    1 in set   -> skip (2 is mid-run)\n  num = 3    2 in set   -> skip\n  num = 4    3 in set   -> skip\n  num = 1    0 not in set -> HEAD, count from here\n  num = 50   49 not in set -> HEAD\n  num = 100  99 not in set -> HEAD"},
        {"code": "            length = 1\n            while num + length in num_set:\n                length += 1",
         "explain": "<p>From a head, walk forward one step at a time while the next value exists. <code>length</code> is both the loop counter and the answer for this run. Each set member is reached by exactly one of these walks (the one starting at its head), so the total work of all walks together is O(n).</p>",
         "diagram": "  head 1:   2 in set, 3 in set, 4 in set, 5 not  -> length = 4\n  head 50:  51 not in set                        -> length = 1\n  head 100: 101 not in set                       -> length = 1"},
        {"code": "            best = max(best, length)",
         "explain": "<p>Keep the longest run seen so far.</p>",
         "diagram": "  best: 0 -> 4 (run from 1) -> 4 -> 4"},
        {"code": "        return best",
         "explain": "<p>All heads have been expanded, so <code>best</code> holds the length of the longest consecutive sequence. For <code>[7, 7, 7]</code> the set is <code>{7}</code>, 7 is a head, and the walk stops immediately with length 1.</p>",
         "diagram": None},
    ],
    "complexity": "Time O(n): building the set is linear and every element is walked forward at most once. Space O(n) for the set.",
}

TESTS = """
s = Solution()
assert s.longestConsecutive([50, 3, 2, 100, 4, 1]) == 4
assert s.longestConsecutive([7, 7, 7]) == 1
assert s.longestConsecutive([]) == 0
assert s.longestConsecutive([5]) == 1
assert s.longestConsecutive([0, -1, 1, 2, -2, 10]) == 5
assert s.longestConsecutive([1, 3, 5, 7]) == 1
assert s.longestConsecutive([9, 1, 4, 7, 3, -1, 0, 5, 8, -1, 6]) == 7
"""
