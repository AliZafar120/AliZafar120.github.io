PROBLEM = {
    "slug": "meeting-rooms", "number": 252, "title": "Meeting Rooms", "category": "Interval", "difficulty": "Easy",
    "url": "https://leetcode.com/problems/meeting-rooms/", "premium": True,
    "statement_html": """<p>You are given a list of meetings, each as a pair <code>[start, end]</code> meaning the meeting occupies the half-open time span from <code>start</code> up to but not including <code>end</code>. One person has to attend every meeting. Return <code>True</code> if that is possible, meaning no two meetings overlap in time, and <code>False</code> otherwise. A meeting that ends at time <code>t</code> and another that starts at <code>t</code> do not conflict.</p>
<pre>
Input:  intervals = [[9,10], [13,15], [10,12]]
Output: True         sorted: 9-10, 10-12, 13-15, no clashes

Input:  intervals = [[1,5], [3,7]]
Output: False        3 falls inside [1,5)
</pre>
<ul>
  <li>0 &le; len(intervals) &le; 10<sup>4</sup>, 0 &le; start &lt; end &le; 10<sup>6</sup></li>
  <li>Meetings are not given in any particular order</li>
</ul>""",
    "intro_html": """<p><strong>Sort by start, then compare each meeting with the one before it.</strong> Once meetings are in start order, the only meeting that can clash with meeting <code>i</code> without also clashing with an earlier pair is meeting <code>i - 1</code>. So a single linear scan checking that every meeting starts no earlier than its predecessor ends is enough, after an O(n log n) sort.</p>""",
    "blocks": [
        {"code": "from typing import List\n\nclass Solution:\n    def canAttendMeetings(self, intervals: List[List[int]]) -> bool:",
         "explain": "<p>LeetCode calls <code>canAttendMeetings</code> with the list of <code>[start, end]</code> pairs and expects a boolean.</p>",
         "diagram": None},
        {"code": "        intervals.sort(key=lambda x: x[0])",
         "explain": "<p>Order the meetings by start time. In this order, if any two meetings overlap, then some <em>adjacent</em> pair overlaps too: the earlier of the two ends after the later one starts, and every meeting between them starts even earlier than the later one. That reduces the check to neighbours only.</p>",
         "diagram": "  before: [[9,10], [13,15], [10,12]]\n  after:  [[9,10], [10,12], [13,15]]\n\n  9-10\n     10--12\n           13--15"},
        {"code": "        for i in range(1, len(intervals)):",
         "explain": "<p>Visit each meeting from the second onwards, so that <code>i - 1</code> is always a valid predecessor. An empty or single-meeting list skips the loop entirely.</p>",
         "diagram": None},
        {"code": "            if intervals[i][0] < intervals[i - 1][1]:\n                return False",
         "explain": "<p>If this meeting starts before the previous one has ended, the person would need to be in two places at once. Strict <code>&lt;</code> allows back-to-back meetings, since spans are half-open. Returning immediately saves scanning the rest.</p>",
         "diagram": "  i=1: [10,12] vs [9,10]:  10 < 10 ? no   (back to back is fine)\n  i=2: [13,15] vs [10,12]: 13 < 12 ? no\n\n  [[1,5],[3,7]]:  i=1:  3 < 5 ? yes -> return False\n  1-----5\n    3-----7"},
        {"code": "        return True",
         "explain": "<p>No adjacent pair clashed, and by the sorting argument that means no pair at all clashes.</p>",
         "diagram": "  [[9,10], [10,12], [13,15]] -> True"},
    ],
    "complexity": "Time O(n log n) for the sort, then O(n) for the scan. Space O(1) extra beyond the in-place sort.",
}

TESTS = """
s = Solution()
assert s.canAttendMeetings([[9,10],[13,15],[10,12]]) is True
assert s.canAttendMeetings([[1,5],[3,7]]) is False
assert s.canAttendMeetings([]) is True
assert s.canAttendMeetings([[4,8]]) is True
assert s.canAttendMeetings([[0,30],[5,10],[15,20]]) is False
assert s.canAttendMeetings([[7,10],[2,4]]) is True
assert s.canAttendMeetings([[1,3],[1,3]]) is False
"""
