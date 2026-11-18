PROBLEM = {
    "slug": "alien-dictionary", "number": 269, "title": "Alien Dictionary", "category": "Graph", "difficulty": "Hard",
    "url": "https://leetcode.com/problems/alien-dictionary/", "premium": True,
    "statement_html": """<p>An alien language uses the lowercase English letters but puts them in an unknown order. You are given a list of words that is <strong>already sorted</strong> according to that alien alphabet. Recover the alphabet: return a string containing every letter that appears in the words, exactly once, in a valid alien order. If several orders are consistent with the words, any one is accepted. If no order is consistent (the words imply a contradiction, or a word is followed by its own proper prefix, which can never be sorted), return the empty string.</p>
<pre>
Input:  words = ["ba", "bc", "ac", "cab"]
Output: "bac"        ba &lt; bc tells us a &lt; c; bc &lt; ac tells us b &lt; a

Input:  words = ["abc", "ab"]
Output: ""           a word cannot come after its own prefix

Input:  words = ["x", "y", "x"]
Output: ""           x &lt; y and y &lt; x is a contradiction
</pre>
<ul>
  <li>1 &le; len(words) &le; 100, 1 &le; len(words[i]) &le; 100</li>
  <li>Words contain only lowercase English letters</li>
  <li>Letters that never appear in the input must not appear in the output</li>
</ul>""",
    "intro_html": """<p><strong>Build a graph from adjacent words, then topologically sort it.</strong> Two neighbouring words in a sorted list tell us one fact: at the first position where they differ, the letter in the earlier word comes before the letter in the later word. Each such fact is a directed edge. Letters with no incoming edges can go first; peeling them off one by one (Kahn's algorithm) produces the alphabet. If a cycle prevents us from peeling every letter, the words were inconsistent and we return <code>\"\"</code>.</p>""",
    "blocks": [
        {"code": "from collections import deque\nfrom typing import List\n\nclass Solution:\n    def alienOrder(self, words: List[str]) -> str:",
         "explain": "<p>LeetCode's template names the method <code>alienOrder</code> and passes the sorted word list; the result is a string of letters. <code>deque</code> gives the queue for the BFS style topological sort.</p>",
         "diagram": None},
        {"code": "        adj = {ch: set() for word in words for ch in word}\n        indegree = {ch: 0 for ch in adj}",
         "explain": "<p>Register every letter that occurs anywhere, even letters that never take part in a comparison, because they must still appear in the output. <code>adj[a]</code> is the set of letters known to come <em>after</em> <code>a</code>; <code>indegree[b]</code> counts how many letters are known to come before <code>b</code>. A set (not a list) for the neighbours means a repeated fact is stored once and the in-degree is not double counted.</p>",
         "diagram": "  words = [\"ba\", \"bc\", \"ac\", \"cab\"]\n  adj      = {b: {}, a: {}, c: {}}\n  indegree = {b: 0, a: 0, c: 0}"},
        {"code": "        for first, second in zip(words, words[1:]):\n            if len(first) > len(second) and first.startswith(second):\n                return \"\"",
         "explain": "<p>Only <em>adjacent</em> pairs carry information; comparing non-adjacent words adds nothing new because the order is transitive. Before extracting a fact, catch the one invalid shape: a longer word followed by its own prefix (like <code>\"abc\"</code> then <code>\"ab\"</code>). No alphabet can sort these this way, so the answer is immediately the empty string.</p>",
         "diagram": "  pairs: (ba, bc)  (bc, ac)  (ac, cab)\n  [\"abc\", \"ab\"]: len 3 > len 2 and \"abc\".startswith(\"ab\") -> \"\""},
        {"code": "            for a, b in zip(first, second):\n                if a != b:\n                    if b not in adj[a]:\n                        adj[a].add(b)\n                        indegree[b] += 1\n                    break",
         "explain": "<p>Walk the two words in lockstep until the letters differ. That first mismatch is the only thing sorting tells us: <code>a</code> comes before <code>b</code>. Record the edge once, bump <code>b</code>'s in-degree, and <code>break</code>, because letters after the first difference carry no ordering information at all.</p>",
         "diagram": "  (ba, bc):  b=b same, a!=c -> edge a -> c    indegree c = 1\n  (bc, ac):  b!=a         -> edge b -> a    indegree a = 1\n  (ac, cab): a!=c         -> a -> c again, already stored\n\n  graph:  b -> a -> c      adj = {b: {a}, a: {c}, c: {}}\n                           indegree = {b: 0, a: 1, c: 1}"},
        {"code": "        queue = deque(ch for ch in adj if indegree[ch] == 0)\n        order = []",
         "explain": "<p>Start Kahn's algorithm with every letter that nothing precedes. These can safely be the first letters of the alphabet. <code>order</code> will collect letters as they are peeled off.</p>",
         "diagram": "  indegree = {b: 0, a: 1, c: 1}  ->  queue = [b], order = []"},
        {"code": "        while queue:\n            ch = queue.popleft()\n            order.append(ch)",
         "explain": "<p>Pop a letter whose predecessors are all already placed and append it to the alphabet. Because a letter only enters the queue when its in-degree is zero, everything before it in <code>order</code> is legitimately earlier in the alien order.</p>",
         "diagram": "  pop b -> order = [b]"},
        {"code": "            for nxt in adj[ch]:\n                indegree[nxt] -= 1\n                if indegree[nxt] == 0:\n                    queue.append(nxt)",
         "explain": "<p>Placing <code>ch</code> satisfies one constraint for each letter it points to. A letter whose last constraint just disappeared is ready and joins the queue. When several letters are ready at once, the order we pop them is arbitrary, which is exactly why multiple valid answers exist.</p>",
         "diagram": "  pop b: a's indegree 1 -> 0, queue = [a]       order = [b]\n  pop a: c's indegree 1 -> 0, queue = [c]       order = [b, a]\n  pop c: no outgoing edges,   queue = []        order = [b, a, c]"},
        {"code": "        return \"\".join(order) if len(order) == len(adj) else \"\"",
         "explain": "<p>If every letter was placed, join them into the answer. If some letters are missing they sit on a cycle (each is waiting for another), which means the input words contradict themselves, so return <code>\"\"</code>. For <code>[\"x\", \"y\", \"x\"]</code> the edges are <code>x -&gt; y</code> and <code>y -&gt; x</code>, both in-degrees are 1, the queue starts empty and <code>order</code> stays empty.</p>",
         "diagram": "  order = [b, a, c], len 3 == 3 letters -> \"bac\"\n  [\"x\", \"y\", \"x\"]: indegree = {x: 1, y: 1}, order = [] -> \"\""},
    ],
    "complexity": "Time O(C) where C is the total number of characters in all words: building edges touches each character once and the sort is linear in letters plus edges (at most 26 letters and 26 * 25 edges). Space O(1) beyond the input, since the graph has at most 26 nodes.",
}

TESTS = """
s = Solution()

def valid(words, result):
    letters = {ch for w in words for ch in w}
    if len(result) != len(letters) or set(result) != letters:
        return False
    pos = {ch: i for i, ch in enumerate(result)}
    for a, b in zip(words, words[1:]):
        if len(a) > len(b) and a.startswith(b):
            return False
        for x, y in zip(a, b):
            if x != y:
                if pos[x] >= pos[y]:
                    return False
                break
    return True

w = ["ba", "bc", "ac", "cab"]
assert s.alienOrder(w) == "bac" and valid(w, "bac")
assert s.alienOrder(["abc", "ab"]) == ""
assert s.alienOrder(["x", "y", "x"]) == ""
w = ["wrt", "wrf", "er", "ett", "rftt"]
assert valid(w, s.alienOrder(w))
w = ["z", "x"]
assert s.alienOrder(w) == "zx"
w = ["abc"]
assert valid(w, s.alienOrder(w))
w = ["ab", "ab"]
assert valid(w, s.alienOrder(w))
w = ["ac", "ab", "zc", "zb"]
assert valid(w, s.alienOrder(w))
assert s.alienOrder(["a", "b", "c", "a"]) == ""
"""
