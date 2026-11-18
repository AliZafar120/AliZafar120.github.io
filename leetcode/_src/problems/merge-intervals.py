PROBLEM = {
    "slug": "merge-intervals", "number": 56, "title": "Merge Intervals", "category": "Interval", "difficulty": "Medium",
    "url": "https://leetcode.com/problems/merge-intervals/", "premium": False,
    "statement_html": """<p>You are given a list of closed intervals <code>[start, end]</code> in no particular order. Merge every group of overlapping intervals into a single interval that covers them all, and return the merged list. Intervals that only touch at an endpoint, such as [1,4] and [4,6], count as overlapping.</p>
<pre>
Input:  intervals = [[6,8], [1,3], [2,5], [9,9]]
Output: [[1,5], [6,8], [9,9]]       [1,3] and [2,5] overlap

Input:  intervals = [[1,4], [4,6]]
Output: [[1,6]]
</pre>
<ul>
  <li>1 &le; len(intervals) &le; 10<sup>4</sup>, 0 &le; start &le; end &le; 10<sup>4</sup></li>
  <li>The output may be in any order, but sorted by start is natural</li>
</ul>""",
    "intro_html": """<p><strong>Sort by start, then sweep once merging into the last emitted interval.</strong> After sorting, any interval that overlaps the current group must begin before the group's current end, so a single comparison against the last merged interval decides whether to extend it or to start a new one. Sorting costs O(n log n); the sweep itself is linear.</p>""",
    "blocks": [
        {"code": "from typing import List\n\nclass Solution:\n    def merge(self, intervals: List[List[int]]) -> List[List[int]]:",
         "explain": "<p>LeetCode calls <code>merge</code> with the unsorted list and expects the merged list.</p>",
         "diagram": None},
        {"code": "        intervals.sort(key=lambda x: x[0])",
         "explain": "<p>Order by start time. This is the step that makes the one-pass sweep correct: once sorted, all intervals that could overlap a given group arrive consecutively, so we never need to look back further than the last merged interval.</p>",
         "diagram": "  before: [[6,8], [1,3], [2,5], [9,9]]\n  after:  [[1,3], [2,5], [6,8], [9,9]]"},
        {"code": "        merged = []",
         "explain": "<p>The output. Its last element is the group currently being built; everything before it is final.</p>",
         "diagram": None},
        {"code": "        for start, end in intervals:",
         "explain": "<p>Sweep the sorted intervals left to right, unpacking each one. Because of the sort, <code>start</code> is never smaller than the start of the last merged interval.</p>",
         "diagram": "  1---3\n    2-----5\n            6---8\n                 9"},
        {"code": "            if merged and merged[-1][1] >= start:\n                merged[-1][1] = max(merged[-1][1], end)",
         "explain": "<p>If the current interval begins no later than the last group ends, they overlap (or touch), so extend the group. The <code>max</code> matters: the new interval might be entirely inside the group, in which case the group's end must not shrink.</p>",
         "diagram": "  merged = [[1,3]]   next [2,5]:  3 >= 2 -> overlap\n  merged[-1][1] = max(3, 5) = 5    -> merged = [[1,5]]\n\n  (if next were [2,2]: max(3,2)=3, group stays [1,3])"},
        {"code": "            else:\n                merged.append([start, end])",
         "explain": "<p>Otherwise there is a gap between the last group and this interval, and since later intervals start even further right, nothing can ever bridge that gap. Close the group and start a new one. A fresh list is appended so we never alias the input.</p>",
         "diagram": "  merged = [[1,5]]        next [6,8]: 5 >= 6 ? no -> append\n  merged = [[1,5],[6,8]]  next [9,9]: 8 >= 9 ? no -> append\n  merged = [[1,5],[6,8],[9,9]]"},
        {"code": "        return merged",
         "explain": "<p>Every input interval has been folded into exactly one output interval. Touching intervals merge because the test uses <code>&gt;=</code>.</p>",
         "diagram": "  [[1,4],[4,6]]: 4 >= 4 -> merge -> [[1,6]]"},
    ],
    "complexity": "Time O(n log n) for the sort, then O(n) for the sweep. Space O(n) for the output (O(log n) to O(n) for the sort, depending on the implementation).",
}

TESTS = """
s = Solution()
assert s.merge([[6,8],[1,3],[2,5],[9,9]]) == [[1,5],[6,8],[9,9]]
assert s.merge([[1,4],[4,6]]) == [[1,6]]
assert s.merge([[3,3]]) == [[3,3]]
assert s.merge([[1,4],[2,3]]) == [[1,4]]
assert s.merge([[1,3],[2,6],[8,10],[15,18]]) == [[1,6],[8,10],[15,18]]
assert s.merge([[5,7],[1,2]]) == [[1,2],[5,7]]
assert s.merge([[1,10],[2,3],[4,5],[9,12]]) == [[1,12]]
"""
