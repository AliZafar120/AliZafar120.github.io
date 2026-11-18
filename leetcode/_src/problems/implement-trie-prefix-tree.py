PROBLEM = {
    "slug": "implement-trie-prefix-tree", "number": 208, "title": "Implement Trie (Prefix Tree)", "category": "Tree", "difficulty": "Medium",
    "url": "https://leetcode.com/problems/implement-trie-prefix-tree/", "premium": False,
    "statement_html": """<p>Implement a class <code>Trie</code> that stores lowercase words and supports three operations: <code>insert(word)</code> adds a word, <code>search(word)</code> reports whether that exact word was inserted, and <code>startsWith(prefix)</code> reports whether any inserted word begins with the given prefix. A prefix that was never inserted as a whole word must make <code>search</code> return false but <code>startsWith</code> return true.</p>
<pre>
trie = Trie()
trie.insert("cart")
trie.search("cart")     -> true
trie.search("car")      -> false     "car" is only a prefix
trie.startsWith("car")  -> true
trie.startsWith("cat")  -> false
trie.insert("car")
trie.search("car")      -> true
</pre>
<ul>
  <li>1 &le; len(word), len(prefix) &le; 2000, lowercase English letters only</li>
  <li>At most 3 &middot; 10<sup>4</sup> calls in total</li>
</ul>""",
    "intro_html": """<p><strong>Nested dictionaries, one level per character.</strong> Each node of the trie is a dict mapping a character to the child node for that character. Walking a word means following one dict lookup per letter. A special key marks the nodes where an inserted word ends, which is what separates \"this is a real word\" from \"this is merely a prefix\". Every operation costs time proportional to the word length, independent of how many words are stored.</p>""",
    "blocks": [
        {"code": "from typing import Optional\n\nclass Trie:\n    def __init__(self):\n        self.root = {}",
         "explain": "<p>A design problem, so the class is <code>Trie</code>. The whole structure is a single nested dict starting from an empty root; children are created lazily as words are inserted.</p>",
         "diagram": "  root = {}"},
        {"code": "    def insert(self, word: str) -> None:\n        node = self.root\n        for ch in word:\n            node = node.setdefault(ch, {})",
         "explain": "<p>Walk down one level per character, creating the child if it does not exist. <code>dict.setdefault(ch, {})</code> returns the existing child or inserts and returns a new empty one, so the lookup and the creation are a single expression.</p>",
         "diagram": "  insert(\"cart\"):\n  root -> {c} -> {a} -> {r} -> {t}\n  root = {\"c\": {\"a\": {\"r\": {\"t\": {}}}}}"},
        {"code": "        node[\"$\"] = True",
         "explain": "<p>Mark the final node as the end of a word. Any key that cannot be a letter works; <code>\"$\"</code> is a common choice. Without this marker the trie could not tell <code>\"car\"</code> apart from the path towards <code>\"cart\"</code>.</p>",
         "diagram": "  after insert(\"cart\"):\n  {\"c\": {\"a\": {\"r\": {\"t\": {\"$\": True}}}}}\n\n  after insert(\"car\") too:\n  {\"c\": {\"a\": {\"r\": {\"$\": True, \"t\": {\"$\": True}}}}}"},
        {"code": "    def _find(self, prefix: str) -> Optional[dict]:\n        node = self.root\n        for ch in prefix:\n            if ch not in node:\n                return None\n            node = node[ch]\n        return node",
         "explain": "<p>A shared helper: follow the characters and return the node where the prefix ends, or <code>None</code> if the path breaks off. Both <code>search</code> and <code>startsWith</code> need exactly this walk and differ only in what they do with the node at the end.</p>",
         "diagram": "  _find(\"car\") -> {\"$\": True, \"t\": {...}}   (a node)\n  _find(\"cat\") -> at \"a\", \"t\" not in node -> None"},
        {"code": "    def search(self, word: str) -> bool:\n        node = self._find(word)\n        return node is not None and \"$\" in node",
         "explain": "<p>An exact word exists only if the path exists <em>and</em> the end marker is set at its last node. Before <code>\"car\"</code> is inserted, <code>_find(\"car\")</code> returns the node <code>{\"t\": ...}</code>, which has no <code>\"$\"</code>, so <code>search</code> correctly says false.</p>",
         "diagram": "  only \"cart\" inserted:\n  search(\"cart\") -> node {\"$\": True}        -> True\n  search(\"car\")  -> node {\"t\": {...}}, no \"$\" -> False\n  search(\"cab\")  -> None                     -> False"},
        {"code": "    def startsWith(self, prefix: str) -> bool:\n        return self._find(prefix) is not None",
         "explain": "<p>For a prefix we only care that the path exists; whether a word ends there is irrelevant. Reaching any node at all means some inserted word continues through it.</p>",
         "diagram": "  startsWith(\"car\") -> node exists -> True\n  startsWith(\"cat\") -> None        -> False\n  startsWith(\"\")    -> root        -> True"},
    ],
    "complexity": "Time O(L) per operation, where L is the length of the word or prefix. Space O(total characters inserted) for the nested dicts.",
}

TESTS = """
t = Trie()
t.insert("cart")
assert t.search("cart") is True
assert t.search("car") is False
assert t.startsWith("car") is True
assert t.startsWith("cat") is False
t.insert("car")
assert t.search("car") is True
assert t.search("ca") is False
assert t.search("carts") is False
assert t.startsWith("c") is True
assert t.startsWith("d") is False
e = Trie()
assert e.search("a") is False
assert e.startsWith("a") is False
e.insert("a")
assert e.search("a") is True
assert e.startsWith("a") is True
"""
