PROBLEM = {
    "slug": "add-and-search-word-data-structure-design", "number": 211, "title": "Design Add and Search Words Data Structure", "category": "Tree", "difficulty": "Medium",
    "url": "https://leetcode.com/problems/add-and-search-word-data-structure-design/", "premium": False,
    "statement_html": """<p>Implement a class <code>WordDictionary</code> with two operations. <code>addWord(word)</code> stores a lowercase word. <code>search(pattern)</code> reports whether any stored word matches the pattern, where the pattern consists of lowercase letters and the wildcard <code>.</code>, which stands for exactly one arbitrary letter. The match must cover the whole word, so lengths have to agree.</p>
<pre>
d = WordDictionary()
d.addWord("dog")
d.addWord("dig")
d.search("dog")   -> true
d.search("d.g")   -> true      matches both "dog" and "dig"
d.search(".i.")   -> true      matches "dig"
d.search("d..")   -> true
d.search("do")    -> false     a prefix is not a match
d.search("...a")  -> false     nothing has length 4
</pre>
<ul>
  <li>1 &le; len(word) &le; 25, lowercase letters; patterns additionally may contain <code>.</code></li>
  <li>At most 10<sup>4</sup> calls; a search pattern has at most 2 dots</li>
</ul>""",
    "intro_html": """<p><strong>A trie plus a depth-first search for wildcards.</strong> Words are stored in a trie of nested dicts, exactly as in a plain prefix tree. Searching a literal character follows one child; searching a <code>.</code> must try <em>every</em> child, so the search becomes a recursive DFS that branches at each dot. The end-of-word marker ensures the pattern consumes the whole word and not just a prefix.</p>""",
    "blocks": [
        {"code": "class WordDictionary:\n    def __init__(self):\n        self.root = {}",
         "explain": "<p>A design problem, so the class name is <code>WordDictionary</code>. The storage is one nested dict rooted at <code>self.root</code>; each node maps a character to its child node.</p>",
         "diagram": "  root = {}"},
        {"code": "    def addWord(self, word: str) -> None:\n        node = self.root\n        for ch in word:\n            node = node.setdefault(ch, {})\n        node[\"$\"] = True",
         "explain": "<p>Standard trie insertion. Walk down one level per character, creating missing children with <code>setdefault</code>, then plant the end marker <code>\"$\"</code> on the last node so that <code>\"do\"</code> is not mistaken for a stored word just because <code>\"dog\"</code> passes through it.</p>",
         "diagram": "  addWord(\"dog\"), addWord(\"dig\"):\n  root\n   d\n   |-- o -- g $\n   |-- i -- g $\n  {\"d\": {\"o\": {\"g\": {\"$\": True}}, \"i\": {\"g\": {\"$\": True}}}}"},
        {"code": "    def search(self, word: str) -> bool:\n        def dfs(node: dict, i: int) -> bool:",
         "explain": "<p><code>dfs(node, i)</code> asks: starting at trie node <code>node</code>, can the rest of the pattern from index <code>i</code> be matched? Making it a closure gives it access to <code>word</code> without passing it along at every level.</p>",
         "diagram": "  search(\"d.g\")  ->  dfs(root, 0)"},
        {"code": "            if i == len(word):\n                return \"$\" in node",
         "explain": "<p>The pattern is used up. Success means a stored word <em>ends</em> exactly here, which is what the marker records. Without this check <code>search(\"do\")</code> would wrongly succeed by reaching the <code>\"o\"</code> node.</p>",
         "diagram": "  search(\"do\"): after \"d\",\"o\" we sit at {\"g\": {...}}\n  i == 2 == len(\"do\") -> \"$\" in node? no -> False"},
        {"code": "            ch = word[i]\n            if ch == \".\":\n                return any(dfs(child, i + 1) for key, child in node.items() if key != \"$\")",
         "explain": "<p>A wildcard may stand for any letter, so try every child of the current node and succeed if any branch matches the remainder. The end marker <code>\"$\"</code> is a key too but not a child node, so it is skipped. <code>any</code> with a generator stops at the first success.</p>",
         "diagram": "  search(\"d.g\"): at node after \"d\" = {\"o\": ..., \"i\": ...}, i=1\n    try \"o\": dfs({\"g\": {\"$\"}}, 2) -> \"g\" matches, i=3 -> \"$\" -> True\n  any(...) -> True (the \"i\" branch is never tried)\n\n  search(\".i.\"): at root, i=0, try \"d\":\n    \"i\" literal -> node {\"g\": {\"$\"}}\n    \".\" at i=2: try \"g\" -> i=3 -> \"$\" -> True"},
        {"code": "            return ch in node and dfs(node[ch], i + 1)",
         "explain": "<p>A literal character has only one possible continuation: the matching child, if it exists. If the child is missing the pattern cannot match along this path and we return <code>False</code> without recursing.</p>",
         "diagram": "  search(\"dog\"): d -> o -> g, then i=3 -> \"$\" -> True\n  search(\"dot\"): d -> o, \"t\" not in {\"g\": ...} -> False"},
        {"code": "        return dfs(self.root, 0)",
         "explain": "<p>Start the search from the root with the whole pattern still to match. A pattern longer than every stored word simply runs out of children and returns false.</p>",
         "diagram": "  search(\"...a\"): three dots reach the \"$\" nodes under g,\n  then \"a\" not in {\"$\": True} -> False"},
    ],
    "complexity": "Time O(L) for addWord and for a search without dots; a search with dots can branch to O(26^d * L) in the worst case for d dots. Space O(total characters added).",
}

TESTS = """
d = WordDictionary()
d.addWord("dog")
d.addWord("dig")
assert d.search("dog") is True
assert d.search("d.g") is True
assert d.search(".i.") is True
assert d.search("d..") is True
assert d.search("do") is False
assert d.search("...a") is False
assert d.search("dot") is False
assert d.search("....") is False
assert d.search("...") is True
e = WordDictionary()
assert e.search("a") is False
assert e.search(".") is False
e.addWord("a")
assert e.search(".") is True
assert e.search("a") is True
assert e.search("..") is False
"""
