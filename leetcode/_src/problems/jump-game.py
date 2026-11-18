PROBLEM = {
    "slug": "jump-game", "number": 55, "title": "Jump Game", "category": "Dynamic Programming", "difficulty": "Medium",
    "url": "https://leetcode.com/problems/jump-game/", "premium": False,
    "statement_html": """<p>You stand on the first position of an array. Each value tells you the maximum number of positions you may jump forward from there (you can jump fewer). Decide whether it is possible to reach the last position.</p>
<pre>
Input:  nums = [2, 3, 1, 0, 4]
Output: True        0 -> 1 -> 4

Input:  nums = [3, 1, 0, 0, 2]
Output: False       index 3 is the farthest you can get, and it has 0 jump
</pre>
<ul>
  <li>1 &le; len(nums) &le; 10<sup>4</sup></li>
  <li>0 &le; nums[i] &le; 10<sup>5</sup></li>
</ul>""",
    "intro_html": """<p><strong>Greedy farthest reach.</strong> Walk left to right while tracking the farthest index reachable from any position visited so far. If the current index lies beyond that reach, we could never have landed here and the answer is False. Otherwise the current position may extend the reach. The full DP (is each index reachable?) collapses to this single number because reachability is contiguous: if you can reach index <code>k</code>, you can reach every index before it too.</p>""",
    "blocks": [
        {"code": "from typing import List\n\nclass Solution:\n    def canJump(self, nums: List[int]) -> bool:",
         "explain": "<p>LeetCode's signature: the array of maximum jump lengths in, a boolean out.</p>",
         "diagram": None},
        {"code": "        farthest = 0",
         "explain": "<p>The highest index we know we can land on. Before taking any jump we are standing at index 0, so that is the initial reach. This one integer replaces a whole boolean table of reachable positions.</p>",
         "diagram": "  nums = [2, 3, 1, 0, 4]\n  idx:    0  1  2  3  4\n          ^ farthest = 0"},
        {"code": "        for i, step in enumerate(nums):",
         "explain": "<p>Visit every index with its jump allowance. We need the index to test reachability and to compute how far a jump from here would land.</p>",
         "diagram": "  i=0 step=2   i=1 step=3   i=2 step=1   i=3 step=0   i=4 step=4"},
        {"code": "            if i > farthest:\n                return False",
         "explain": "<p>If the current index is beyond the farthest reach, no earlier position could jump here, and since we scan in order nothing later can help either. We are stuck before the end. This is the only way to fail.</p>",
         "diagram": "  nums = [3, 1, 0, 0, 2]\n  i=0  farthest=0  ok   -> farthest = max(0, 0+3) = 3\n  i=1  farthest=3  ok   -> farthest = max(3, 1+1) = 3\n  i=2  farthest=3  ok   -> farthest = max(3, 2+0) = 3\n  i=3  farthest=3  ok   -> farthest = max(3, 3+0) = 3\n  i=4  4 > 3   STUCK   -> return False"},
        {"code": "            farthest = max(farthest, i + step)",
         "explain": "<p>Since we can stand here, we can also jump from here, landing anywhere up to <code>i + step</code>. Extend the reach if that beats the current record. Taking the maximum rather than overwriting is essential: a short jump from a later position must not shrink a long reach established earlier.</p>",
         "diagram": "  nums = [2, 3, 1, 0, 4]\n  i=0 step=2  farthest = max(0, 2) = 2\n  i=1 step=3  farthest = max(2, 4) = 4\n  i=2 step=1  farthest = max(4, 3) = 4\n  i=3 step=0  farthest = max(4, 3) = 4\n  i=4 step=4  farthest = max(4, 8) = 8"},
        {"code": "        return True",
         "explain": "<p>If the loop finishes, every index including the last one passed the reachability test, so the end is reachable. A one-element array trivially returns True here because index 0 is where we start.</p>",
         "diagram": "  nums = [2, 3, 1, 0, 4]: loop completes -> True\n  nums = [0]:             i=0, 0 > 0 is False -> True"},
    ],
    "complexity": "Time O(n), one pass. Space O(1), a single integer.",
}

TESTS = """
s = Solution()
assert s.canJump([2, 3, 1, 0, 4]) is True
assert s.canJump([3, 1, 0, 0, 2]) is False
assert s.canJump([2, 3, 1, 1, 4]) is True
assert s.canJump([3, 2, 1, 0, 4]) is False
assert s.canJump([0]) is True
assert s.canJump([0, 1]) is False
assert s.canJump([1, 1, 1, 1]) is True
assert s.canJump([5, 0, 0, 0, 0, 0]) is True
"""
