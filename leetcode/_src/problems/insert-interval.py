PROBLEM = {
    "slug": "insert-interval", "number": 57, "title": "Insert Interval", "category": "Interval", "difficulty": "Medium",
    "url": "https://leetcode.com/problems/insert-interval/", "premium": False,
    "statement_html": """<p>You are given a list of closed intervals <code>[start, end]</code> that do not overlap and are sorted by start, plus one extra interval <code>newInterval</code>. Insert the new interval into the list so that the result is still sorted and still free of overlaps, merging it with any existing intervals it touches. Return the resulting list.</p>
<pre>
Input:  intervals = [[1,2], [4,6], [8,10], [12,15]], newInterval = [5,9]
Output: [[1,2], [4,10], [12,15]]      [5,9] swallows [4,6] and [8,10]

Input:  intervals = [[1,3]], newInterval = [5,7]
Output: [[1,3], [5,7]]
</pre>
<ul>
  <li>0 &le; len(intervals) &le; 10<sup>4</sup>, intervals are sorted by start and pairwise disjoint</li>
  <li>Intervals are closed: [1,3] and [3,5] overlap at 3 and should merge</li>
</ul>""",
    "intro_html": """<p><strong>Three linear phases over the sorted list.</strong> First copy every interval that ends before the new one starts; they are untouched. Then absorb every interval that overlaps the new one by widening its start and end. Finally copy the rest, which all begin after the merged interval ends. Because the input is sorted, each interval falls into exactly one of these phases and we visit it once.</p>""",
    "blocks": [
        {"code": "from typing import List\n\nclass Solution:\n    def insert(self, intervals: List[List[int]], newInterval: List[int]) -> List[List[int]]:",
         "explain": "<p>LeetCode calls <code>insert</code> with the sorted disjoint list and the new interval, and expects the merged list.</p>",
         "diagram": None},
        {"code": "        result = []\n        i = 0\n        n = len(intervals)",
         "explain": "<p>The output list, a cursor <code>i</code> into the input, and its length. The same cursor is carried through all three phases so every interval is examined exactly once.</p>",
         "diagram": "  intervals = [[1,2], [4,6], [8,10], [12,15]]   new = [5,9]\n  i = 0        ^\n  result = []"},
        {"code": "        start, end = newInterval",
         "explain": "<p>Unpack the new interval into two variables we can widen during the merge phase. Working on copies leaves the caller's list untouched.</p>",
         "diagram": "  start = 5, end = 9"},
        {"code": "        while i < n and intervals[i][1] < start:\n            result.append(intervals[i])\n            i += 1",
         "explain": "<p>Phase 1: intervals that finish strictly before the new one begins cannot overlap it. Copy them straight across. The strict <code>&lt;</code> is deliberate: an interval ending exactly at <code>start</code> touches the new one and must be merged, not copied.</p>",
         "diagram": "  [1,2]: 2 < 5  -> copy, i=1\n  [4,6]: 6 < 5 ? no -> stop phase 1\n  result = [[1,2]]"},
        {"code": "        while i < n and intervals[i][0] <= end:\n            start = min(start, intervals[i][0])\n            end = max(end, intervals[i][1])\n            i += 1",
         "explain": "<p>Phase 2: every interval that starts no later than the current <code>end</code> overlaps the new one (we already know it does not end before <code>start</code>). Absorb it by extending <code>start</code> downwards and <code>end</code> upwards. Each absorption can push <code>end</code> further right, so the condition is re-evaluated against the updated <code>end</code>.</p>",
         "diagram": "  [4,6]:   4 <= 9  -> start=min(5,4)=4,  end=max(9,6)=9,   i=2\n  [8,10]:  8 <= 9  -> start=4,           end=max(9,10)=10, i=3\n  [12,15]: 12 <= 10 ? no -> stop phase 2\n\n  new:        5-----9\n  absorbed:  4--6  8---10   ->  merged 4--------10"},
        {"code": "        result.append([start, end])",
         "explain": "<p>Emit the merged interval once. It belongs here in the order because everything already in <code>result</code> ends before it and everything still unvisited starts after it.</p>",
         "diagram": "  result = [[1,2], [4,10]]"},
        {"code": "        while i < n:\n            result.append(intervals[i])\n            i += 1",
         "explain": "<p>Phase 3: the remaining intervals all start after the merged interval ends, so they are copied unchanged.</p>",
         "diagram": "  [12,15] -> copy\n  result = [[1,2], [4,10], [12,15]]"},
        {"code": "        return result",
         "explain": "<p>Sorted and overlap-free. If the new interval lies entirely after the list, phase 1 copies everything, phase 2 absorbs nothing and the new interval is appended at the end.</p>",
         "diagram": "  intervals = [[1,3]], new = [5,7]\n  phase 1: 3 < 5 -> copy [1,3]\n  phase 2: nothing left\n  append [5,7]  -> [[1,3], [5,7]]"},
    ],
    "complexity": "Time O(n), each interval is visited once. Space O(n) for the output.",
}

TESTS = """
s = Solution()
assert s.insert([[1,2],[4,6],[8,10],[12,15]], [5,9]) == [[1,2],[4,10],[12,15]]
assert s.insert([[1,3]], [5,7]) == [[1,3],[5,7]]
assert s.insert([], [2,5]) == [[2,5]]
assert s.insert([[1,5]], [2,3]) == [[1,5]]
assert s.insert([[1,3],[6,9]], [2,5]) == [[1,5],[6,9]]
assert s.insert([[3,5],[8,9]], [1,2]) == [[1,2],[3,5],[8,9]]
assert s.insert([[1,3],[4,6]], [3,4]) == [[1,6]]
assert s.insert([[1,2],[3,5],[6,7],[8,10],[12,16]], [4,8]) == [[1,2],[3,10],[12,16]]
"""
