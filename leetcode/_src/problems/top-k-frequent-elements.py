PROBLEM = {
    "slug": "top-k-frequent-elements", "number": 347, "title": "Top K Frequent Elements", "category": "Heap", "difficulty": "Medium",
    "url": "https://leetcode.com/problems/top-k-frequent-elements/", "premium": False,
    "statement_html": """<p>Given a list of integers and a number <code>k</code>, return the <code>k</code> values that occur most often. The answer may be in any order. You may assume the answer is unique, meaning there is no tie at the boundary that would make two different sets of <code>k</code> elements valid.</p>
<pre>
Input:  nums = [4, 4, 4, 7, 7, 2, 9, 9, 9, 9], k = 2
Output: [9, 4]        9 appears 4 times, 4 appears 3 times

Input:  nums = [5], k = 1
Output: [5]
</pre>
<ul>
  <li>1 &le; len(nums) &le; 10<sup>5</sup>, 1 &le; k &le; number of distinct values</li>
  <li>Follow-up: better than O(n log n)</li>
</ul>""",
    "intro_html": """<p><strong>Count, then keep a min-heap of size k.</strong> A <code>Counter</code> gives each value's frequency in one pass. We then push <code>(frequency, value)</code> pairs into a heap and pop the smallest whenever the heap grows past <code>k</code>, so the heap always holds the <code>k</code> most frequent seen so far. Each push and pop costs O(log k), giving O(n log k) overall, which beats sorting all the counts when <code>k</code> is small. (<code>heapq.nlargest(k, counts, key=counts.get)</code> is the one-line equivalent.)</p>""",
    "blocks": [
        {"code": "from collections import Counter\nimport heapq\nfrom typing import List\n\nclass Solution:\n    def topKFrequent(self, nums: List[int], k: int) -> List[int]:",
         "explain": "<p><code>Counter</code> is a dict subclass that tallies occurrences. <code>heapq</code> implements a binary min-heap on top of a plain list: <code>heappush</code> and <code>heappop</code> keep the smallest item at index 0 in O(log size) each.</p>",
         "diagram": None},
        {"code": "        counts = Counter(nums)",
         "explain": "<p>One linear pass to map each distinct value to how many times it appears. From here on we work with the distinct values only, of which there may be far fewer than <code>len(nums)</code>.</p>",
         "diagram": "  nums = [4, 4, 4, 7, 7, 2, 9, 9, 9, 9]\n  counts = {4: 3, 7: 2, 2: 1, 9: 4}"},
        {"code": "        heap: List[tuple] = []",
         "explain": "<p>The heap is just a list that <code>heapq</code> keeps in heap order: every parent is <code>&le;</code> its children, so the minimum is always at <code>heap[0]</code>. It will hold at most <code>k</code> entries of the form <code>(frequency, value)</code>. Tuples compare element by element, so the frequency decides the ordering.</p>",
         "diagram": "  heap = []      will hold (freq, value) pairs, min at index 0"},
        {"code": "        for num, freq in counts.items():\n            heapq.heappush(heap, (freq, num))",
         "explain": "<p>Push every distinct value with its frequency first. <code>heappush</code> appends to the end of the list and then \"sifts up\", swapping with its parent until the heap property holds again. That is O(log k) because the heap never exceeds <code>k + 1</code> items.</p>",
         "diagram": "  k = 2\n  push (3, 4):   heap = [(3,4)]\n  push (2, 7):   heap = [(2,7), (3,4)]        min at index 0\n  push (1, 2):   heap = [(1,2), (3,4), (2,7)]  size 3 > k"},
        {"code": "            if len(heap) > k:\n                heapq.heappop(heap)",
         "explain": "<p>If the heap now has <code>k + 1</code> entries, evict the least frequent, which is the root. <code>heappop</code> removes <code>heap[0]</code>, moves the last item to the root, and \"sifts down\" to restore order. After this the heap holds exactly the <code>k</code> most frequent values seen so far; anything popped can never return, which is correct since a later item only pushes smaller counts out, never larger ones.</p>",
         "diagram": "  heap = [(1,2), (3,4), (2,7)]   pop -> (1,2) leaves\n  heap = [(2,7), (3,4)]\n\n  push (4, 9):   heap = [(2,7), (3,4), (4,9)]  size 3 > k\n  pop  -> (2,7) leaves\n  heap = [(3,4), (4,9)]"},
        {"code": "        return [num for freq, num in heap]",
         "explain": "<p>Whatever survived in the heap is the answer. Strip the frequencies and return the values. The list is in heap order, not sorted by frequency, which is fine because the problem accepts any order.</p>",
         "diagram": "  heap = [(3,4), (4,9)]   ->   [4, 9]"},
    ],
    "complexity": "Time O(n log k): O(n) to count, then one O(log k) heap operation per distinct value. Space O(n) for the counts plus O(k) for the heap.",
}

TESTS = """
s = Solution()
assert sorted(s.topKFrequent([4, 4, 4, 7, 7, 2, 9, 9, 9, 9], 2)) == [4, 9]
assert s.topKFrequent([5], 1) == [5]
assert sorted(s.topKFrequent([1, 1, 1, 2, 2, 3], 2)) == [1, 2]
assert sorted(s.topKFrequent([1, 2, 3], 3)) == [1, 2, 3]
assert sorted(s.topKFrequent([-1, -1, 0], 1)) == [-1]
assert sorted(s.topKFrequent([3, 3, 3, 1, 1, 2], 1)) == [3]
"""
