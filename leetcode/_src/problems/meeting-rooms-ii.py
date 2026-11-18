PROBLEM = {
    "slug": "meeting-rooms-ii", "number": 253, "title": "Meeting Rooms II", "category": "Interval", "difficulty": "Medium",
    "url": "https://leetcode.com/problems/meeting-rooms-ii/", "premium": True,
    "statement_html": """<p>You are given a list of meetings, each as a pair <code>[start, end]</code> occupying the half-open span from <code>start</code> up to but not including <code>end</code>. Every meeting needs a room for its whole duration, and a room can host only one meeting at a time, though a new meeting may begin in a room at the exact moment the previous one ends. Return the minimum number of rooms needed so that every meeting can be held.</p>
<pre>
Input:  intervals = [[1,4], [2,5], [4,6], [5,7]]
Output: 2          [1,4] and [2,5] overlap; [4,6] reuses the first room,
                   [5,7] reuses the second

Input:  intervals = [[8,9], [9,10]]
Output: 1
</pre>
<ul>
  <li>1 &le; len(intervals) &le; 10<sup>4</sup>, 0 &le; start &lt; end &le; 10<sup>6</sup></li>
  <li>Meetings are not given in any particular order</li>
</ul>""",
    "intro_html": """<p><strong>Sort by start and keep a min-heap of the end times of meetings in progress.</strong> Processing meetings in start order, the heap top is the room that frees up soonest. If that room is free by the time the next meeting starts, reuse it (pop); otherwise a new room is needed. Either way the new meeting's end time is pushed. The heap never shrinks below the peak number of simultaneous meetings, so its final size is the answer.</p>""",
    "blocks": [
        {"code": "import heapq\nfrom typing import List\n\nclass Solution:\n    def minMeetingRooms(self, intervals: List[List[int]]) -> int:",
         "explain": "<p>LeetCode calls <code>minMeetingRooms</code> with the list of <code>[start, end]</code> pairs and expects an integer. <code>heapq</code> provides a binary min-heap over a plain list.</p>",
         "diagram": None},
        {"code": "        intervals.sort(key=lambda x: x[0])",
         "explain": "<p>Handle meetings in the order they begin. This mirrors how rooms are actually assigned over time: when a meeting starts, the only question is whether some room has already been vacated.</p>",
         "diagram": "  sorted: [[1,4], [2,5], [4,6], [5,7]]\n\n  1---4\n    2---5\n        4---6\n          5---7"},
        {"code": "        ends = []",
         "explain": "<p>The heap. Each entry is the end time of a meeting currently occupying a room, so <code>len(ends)</code> is the number of rooms in use and <code>ends[0]</code> is the earliest any of them becomes free.</p>",
         "diagram": "  ends = []        (no rooms in use)"},
        {"code": "        for start, end in intervals:",
         "explain": "<p>Sweep through the meetings by start time. For each one we decide whether to reuse a room or open a new one.</p>",
         "diagram": None},
        {"code": "            if ends and ends[0] <= start:\n                heapq.heappop(ends)",
         "explain": "<p>Look at the room that frees up first. If it is free by <code>start</code>, this meeting can take it over: pop that finished meeting. Checking only the earliest end is enough, because if even that room is still busy, every other room is busier. The <code>&lt;=</code> lets a meeting start exactly when another ends.</p>",
         "diagram": "  [1,4]: ends=[]      nothing to free\n  [2,5]: ends=[4]     4 <= 2 ? no    (room still busy)\n  [4,6]: ends=[4,5]   4 <= 4 ? yes  -> pop 4, ends=[5]\n  [5,7]: ends=[5,6]   5 <= 5 ? yes  -> pop 5, ends=[6]"},
        {"code": "            heapq.heappush(ends, end)",
         "explain": "<p>Whether we reused a room or not, this meeting now occupies one until <code>end</code>, so push its end time. If we popped above, the heap size is unchanged (same room, new meeting); if not, it grows by one (a new room).</p>",
         "diagram": "  meeting   pop?   push   ends after   rooms\n  [1,4]     no      4     [4]           1\n  [2,5]     no      5     [4,5]         2\n  [4,6]     yes     6     [5,6]         2\n  [5,7]     yes     7     [6,7]         2"},
        {"code": "        return len(ends)",
         "explain": "<p>Rooms are only ever added, never removed (a pop is always followed by a push), so the heap size at the end equals the maximum number of rooms that were ever simultaneously occupied, which is the minimum number of rooms required.</p>",
         "diagram": "  [[8,9],[9,10]]:  push 9 -> [9];  9 <= 9 pop, push 10 -> [10]\n  len(ends) = 1"},
    ],
    "complexity": "Time O(n log n): sorting, plus one O(log n) heap push (and at most one pop) per meeting. Space O(n) for the heap in the worst case.",
}

TESTS = """
s = Solution()
assert s.minMeetingRooms([[1,4],[2,5],[4,6],[5,7]]) == 2
assert s.minMeetingRooms([[8,9],[9,10]]) == 1
assert s.minMeetingRooms([[3,6]]) == 1
assert s.minMeetingRooms([[0,30],[5,10],[15,20]]) == 2
assert s.minMeetingRooms([[1,5],[1,5],[1,5]]) == 3
assert s.minMeetingRooms([[1,10],[2,3],[4,5],[6,7]]) == 2
assert s.minMeetingRooms([[13,15],[1,13],[6,9]]) == 2
"""
