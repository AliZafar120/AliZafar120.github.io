PROBLEM = {
    "slug": "find-median-from-data-stream", "number": 295, "title": "Find Median from Data Stream", "category": "Heap", "difficulty": "Hard",
    "url": "https://leetcode.com/problems/find-median-from-data-stream/", "premium": False,
    "statement_html": """<p>Design a class <code>MedianFinder</code> that receives integers one at a time and can report the median of everything received so far at any moment. The median of an odd-sized collection is its middle value when sorted; for an even-sized collection it is the mean of the two middle values. Both operations will be called many times, so each should be fast.</p>
<pre>
MedianFinder()
addNum(5)      ->  findMedian() = 5.0
addNum(2)      ->  findMedian() = 3.5      sorted: 2 5
addNum(8)      ->  findMedian() = 5.0      sorted: 2 5 8
addNum(1)      ->  findMedian() = 3.5      sorted: 1 2 5 8
</pre>
<ul>
  <li>-10<sup>5</sup> &le; num &le; 10<sup>5</sup></li>
  <li>findMedian is only called after at least one addNum</li>
  <li>Up to 5 * 10<sup>4</sup> calls in total</li>
</ul>""",
    "intro_html": """<p><strong>Two heaps that split the data in half.</strong> A max-heap <code>low</code> holds the smaller half and a min-heap <code>high</code> holds the larger half, so the median is always at the top of one or both. Each new number first goes through <code>low</code>, then the largest of <code>low</code> is moved to <code>high</code>, and if <code>high</code> ends up bigger we move one back. That keeps every element of <code>low</code> at most every element of <code>high</code>, with sizes equal or <code>low</code> one larger. Insertion is O(log n) and the median is read in O(1).</p>""",
    "blocks": [
        {"code": "import heapq\n\nclass MedianFinder:",
         "explain": "<p>LeetCode instantiates <code>MedianFinder</code> directly and calls its methods, so the class name must match. Python's <code>heapq</code> only provides a min-heap, which is why the max-heap below stores negated values.</p>",
         "diagram": None},
        {"code": "    def __init__(self):\n        self.low: list[int] = []\n        self.high: list[int] = []",
         "explain": "<p>Two heaps, both empty to start. <code>low</code> is a max-heap of the smaller half, stored as negatives so that <code>heapq</code>'s min-heap pops the largest original value. <code>high</code> is an ordinary min-heap of the larger half. The invariants we maintain: every value in <code>low</code> is <code>&le;</code> every value in <code>high</code>, and <code>len(low)</code> is <code>len(high)</code> or <code>len(high) + 1</code>.</p>",
         "diagram": "  low  (max-heap, negated):  []     smaller half, biggest on top\n  high (min-heap):           []     larger half, smallest on top\n\n  sorted data:  [ ... low ... ] [ ... high ... ]\n                          ^top   ^top"},
        {"code": "    def addNum(self, num: int) -> None:\n        heapq.heappush(self.low, -num)",
         "explain": "<p>Step one of an insert: push the number into <code>low</code>, negated. We do not yet know which half it belongs in, and pushing into <code>low</code> unconditionally is fine because the next step immediately filters it.</p>",
         "diagram": "  state before: low = {2}        high = {5}\n  addNum(8):    low = {2, 8}     high = {5}     (stored as -2, -8)"},
        {"code": "        heapq.heappush(self.high, -heapq.heappop(self.low))",
         "explain": "<p>Step two: pop the largest value of <code>low</code> (its root, un-negated) and push it into <code>high</code>. If the new number was large it is the one that moves, landing in the correct half. If it was small, it stays and the previous maximum of <code>low</code> moves up instead. Either way the ordering invariant <code>max(low) &le; min(high)</code> holds after this step.</p>",
         "diagram": "  low = {2, 8}  high = {5}\n  pop max of low -> 8,  push into high\n  low = {2}     high = {5, 8}     every low <= every high"},
        {"code": "        if len(self.high) > len(self.low):\n            heapq.heappush(self.low, -heapq.heappop(self.high))",
         "explain": "<p>Step three: fix the sizes. Step two always grows <code>high</code> by one, so after it <code>high</code> may be larger than <code>low</code>. If so, move the smallest of <code>high</code> back to <code>low</code>. Now <code>low</code> is equal in size or one bigger, so the median is either the top of <code>low</code> alone (odd count) or the average of the two tops (even count).</p>",
         "diagram": "  low = {2}     high = {5, 8}     sizes 1 vs 2 -> rebalance\n  pop min of high -> 5, push into low\n  low = {2, 5}  high = {8}        sizes 2 vs 1   top of low = 5\n\n  full trace of the example:\n  add 5: low={5} high={}           median 5\n  add 2: low={2} high={5}          median (2+5)/2 = 3.5\n  add 8: low={2,5} high={8}        median 5\n  add 1: low={1,2} high={5,8}      median (2+5)/2 = 3.5"},
        {"code": "    def findMedian(self) -> float:\n        if len(self.low) > len(self.high):\n            return float(-self.low[0])",
         "explain": "<p>With an odd number of elements, <code>low</code> holds one more than <code>high</code>, and its root is the exact middle value. Un-negate it and return it as a float, since the problem expects a floating-point result.</p>",
         "diagram": "  low = {2, 5}  high = {8}      3 elements, odd\n  low[0] = -5  ->  median = 5.0"},
        {"code": "        return (-self.low[0] + self.high[0]) / 2",
         "explain": "<p>With an even count the two halves are the same size, and the two middle values are the top of each heap: the largest of the small half and the smallest of the large half. Their mean is the median. Division by 2 in Python 3 produces a float even for whole-number results.</p>",
         "diagram": "  low = {1, 2}  high = {5, 8}   4 elements, even\n  -low[0] = 2,  high[0] = 5  ->  median = (2 + 5) / 2 = 3.5"},
    ],
    "complexity": "addNum is O(log n) for at most three heap operations; findMedian is O(1). Space O(n) to hold every number across the two heaps.",
}

TESTS = """
mf = MedianFinder()
mf.addNum(5); assert mf.findMedian() == 5.0
mf.addNum(2); assert mf.findMedian() == 3.5
mf.addNum(8); assert mf.findMedian() == 5.0
mf.addNum(1); assert mf.findMedian() == 3.5
mf2 = MedianFinder()
mf2.addNum(1); mf2.addNum(2); assert mf2.findMedian() == 1.5
mf2.addNum(3); assert mf2.findMedian() == 2.0
mf3 = MedianFinder()
for v in [7, 7, 7, 7]: mf3.addNum(v)
assert mf3.findMedian() == 7.0
mf4 = MedianFinder()
for v in [-3, -1, -2, 10, 4]: mf4.addNum(v)
assert mf4.findMedian() == -1.0
mf4.addNum(100); assert mf4.findMedian() == 1.5
"""
