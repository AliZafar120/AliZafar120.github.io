PROBLEM = {
    "slug": "non-overlapping-intervals", "number": 435, "title": "Non-overlapping Intervals", "category": "Interval", "difficulty": "Medium",
    "url": "https://leetcode.com/problems/non-overlapping-intervals/", "premium": False,
    "statement_html": """<p>You are given a list of intervals <code>[start, end]</code>. Return the smallest number of intervals you must remove so that the ones left do not overlap. Two intervals that only touch, such as [1,3] and [3,5], are <em>not</em> considered overlapping here.</p>
<pre>
Input:  intervals = [[1,4], [2,3], [3,5], [6,7]]
Output: 1          remove [1,4]; [2,3], [3,5], [6,7] are then disjoint

Input:  intervals = [[1,2], [2,3], [3,4]]
Output: 0          touching is fine
</pre>
<ul>
  <li>1 &le; len(intervals) &le; 10<sup>5</sup>, -5 * 10<sup>4</sup> &le; start &lt; end &le; 5 * 10<sup>4</sup></li>
  <li>Return the count removed, not the remaining intervals</li>
</ul>""",
    "intro_html": """<p><strong>Greedy by earliest end time.</strong> Removing the fewest intervals is the same as keeping the most, and the classic way to keep the most non-overlapping intervals is to sort by end and always keep the one that finishes first: it leaves the most room for whatever comes next. Sweep the sorted list, keep an interval when it starts after the last kept one ends, and count every interval that does not.</p>""",
    "blocks": [
        {"code": "from typing import List\n\nclass Solution:\n    def eraseOverlapIntervals(self, intervals: List[List[int]]) -> int:",
         "explain": "<p>LeetCode calls <code>eraseOverlapIntervals</code> with the list and expects the minimum number of removals.</p>",
         "diagram": None},
        {"code": "        intervals.sort(key=lambda x: x[1])",
         "explain": "<p>Sort by <em>end</em>, not start. The interval that ends earliest is always safe to keep: any optimal solution that keeps a different first interval can swap it for this one without creating a conflict, because this one ends no later.</p>",
         "diagram": "  before: [[1,4], [2,3], [3,5], [6,7]]\n  after:  [[2,3], [1,4], [3,5], [6,7]]   (by end: 3, 4, 5, 7)"},
        {"code": "        removed = 0",
         "explain": "<p>The number of intervals discarded so far. This is the quantity the problem asks for, so we count removals directly rather than counting the kept ones and subtracting.</p>",
         "diagram": None},
        {"code": "        prev_end = intervals[0][1]",
         "explain": "<p>The end of the most recently kept interval. The first interval in end order is always kept, so its end is the starting point. The constraints guarantee at least one interval, so indexing is safe.</p>",
         "diagram": "  keep [2,3]  -> prev_end = 3\n\n     2-3\n   1-----4\n       3---5\n              6-7"},
        {"code": "        for start, end in intervals[1:]:",
         "explain": "<p>Consider the remaining intervals in order of their end. Each one is either kept or removed, decided by a single comparison with <code>prev_end</code>.</p>",
         "diagram": None},
        {"code": "            if start < prev_end:\n                removed += 1",
         "explain": "<p>If this interval begins before the last kept one finishes, the two overlap. Remove this one rather than the kept one: the kept one ends no later (we sorted by end), so it is the better interval to hold on to. Touching intervals (<code>start == prev_end</code>) are not overlaps, hence the strict <code>&lt;</code>.</p>",
         "diagram": "  [1,4]: start 1 < prev_end 3 -> overlap, removed = 1\n  (prev_end stays 3)"},
        {"code": "            else:\n                prev_end = end",
         "explain": "<p>No overlap, so keep this interval and it becomes the new reference. From now on, later intervals must start at or after its end.</p>",
         "diagram": "  interval  start < prev_end ?  action        prev_end  removed\n  [2,3]     (first)             keep             3         0\n  [1,4]     1 < 3  yes          remove           3         1\n  [3,5]     3 < 3  no           keep             5         1\n  [6,7]     6 < 5  no           keep             7         1"},
        {"code": "        return removed",
         "explain": "<p>Every interval that conflicted with the greedy choice has been counted. For a list where every interval starts exactly where the previous ends, nothing is removed.</p>",
         "diagram": "  [[1,2],[2,3],[3,4]]: 2 < 2 no, 3 < 3 no -> removed = 0"},
    ],
    "complexity": "Time O(n log n) for the sort, then O(n) for the sweep. Space O(1) extra beyond the in-place sort.",
}

TESTS = """
s = Solution()
assert s.eraseOverlapIntervals([[1,4],[2,3],[3,5],[6,7]]) == 1
assert s.eraseOverlapIntervals([[1,2],[2,3],[3,4]]) == 0
assert s.eraseOverlapIntervals([[1,2]]) == 0
assert s.eraseOverlapIntervals([[1,2],[1,2],[1,2]]) == 2
assert s.eraseOverlapIntervals([[1,2],[2,3],[3,4],[1,3]]) == 1
assert s.eraseOverlapIntervals([[1,100],[11,22],[1,11],[2,12]]) == 2
assert s.eraseOverlapIntervals([[-5,0],[-3,2],[1,4]]) == 1
"""
