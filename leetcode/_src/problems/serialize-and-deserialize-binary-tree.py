PROBLEM = {
    "slug": "serialize-and-deserialize-binary-tree", "number": 297, "title": "Serialize and Deserialize Binary Tree", "category": "Tree", "difficulty": "Hard",
    "url": "https://leetcode.com/problems/serialize-and-deserialize-binary-tree/", "premium": False,
    "statement_html": """<p>Design a class <code>Codec</code> that turns a binary tree into a string and back. <code>serialize(root)</code> must produce a string from which <code>deserialize(s)</code> rebuilds a tree with exactly the same shape and values. The string format is entirely up to you; the only requirement is that the round trip is lossless. Node values may be negative and have several digits.</p>
<pre>
Input:  root = [1, 2, 3, null, null, 4, 5]
          1
         / \\
        2   3
           / \\
          4   5
serialize   -> "1,2,#,#,3,4,#,#,5,#,#"   (one possible encoding)
deserialize -> the same tree, level order [1, 2, 3, null, null, 4, 5]

Input:  root = []
serialize   -> "#"
deserialize -> empty tree
</pre>
<ul>
  <li>0 &le; number of nodes &le; 10<sup>4</sup></li>
  <li>-1000 &le; Node.val &le; 1000</li>
</ul>""",
    "intro_html": """<p><strong>Preorder with explicit null markers.</strong> A preorder walk that writes <code>#</code> for every missing child describes the tree unambiguously: the first token is the root, and the tokens that follow are the left subtree in full, then the right subtree. To decode, we read the tokens in order through an iterator and build recursively; because the iterator advances as a side effect, the left-subtree call consumes exactly its own tokens and leaves the right subtree's tokens for the next call. No indices or lengths need to be tracked.</p>""",
    "blocks": [
        {"code": "from typing import Optional\n\nclass Codec:",
         "explain": "<p>A design problem, so the class is <code>Codec</code>. LeetCode runs <code>deserialize(serialize(root))</code> and checks the result against the original tree.</p>",
         "diagram": None},
        {"code": "    def serialize(self, root: Optional[TreeNode]) -> str:\n        parts = []",
         "explain": "<p>Collect tokens in a list and join once at the end; one token per node and one per missing child. Building the string piece by piece with <code>+=</code> would be quadratic.</p>",
         "diagram": "          1\n         / \\\\\n        2   3\n           / \\\\\n          4   5\n  parts = []"},
        {"code": "        def walk(node: Optional[TreeNode]) -> None:\n            if node is None:\n                parts.append(\"#\")\n                return",
         "explain": "<p>The recursive writer. A missing child is written as the marker <code>#</code>. This is what makes the format decodable: without the markers, <code>[1, 2]</code> and <code>[1, null, 2]</code> would both serialise to <code>\"1,2\"</code>.</p>",
         "diagram": "  walk(None) -> parts gets \"#\"\n\n  [1, 2]        -> 1,2,#,#,#\n  [1, null, 2]  -> 1,#,2,#,#     (different, as required)"},
        {"code": "            parts.append(str(node.val))\n            walk(node.left)\n            walk(node.right)",
         "explain": "<p>Preorder: the node first, then the entire left subtree, then the entire right subtree. Writing the node before its children is what lets the decoder know, at every step, which node it is about to build.</p>",
         "diagram": "  walk(1): \"1\"\n    walk(2): \"2\"  walk(None): \"#\"  walk(None): \"#\"\n    walk(3): \"3\"\n      walk(4): \"4\"  \"#\"  \"#\"\n      walk(5): \"5\"  \"#\"  \"#\"\n  parts = [1, 2, #, #, 3, 4, #, #, 5, #, #]"},
        {"code": "        walk(root)\n        return \",\".join(parts)",
         "explain": "<p>Run the walk from the root and join with commas. The comma separator is safe because values are integers; a negative sign or multiple digits never contain a comma. An empty tree produces just <code>\"#\"</code>.</p>",
         "diagram": "  \"1,2,#,#,3,4,#,#,5,#,#\"\n  empty tree -> \"#\""},
        {"code": "    def deserialize(self, data: str) -> Optional[TreeNode]:\n        tokens = iter(data.split(\",\"))",
         "explain": "<p>Split back into tokens and wrap them in an iterator. The iterator is the whole trick: every call to <code>next</code> consumes one token permanently, so recursive calls automatically continue from where the previous one stopped without passing an index around.</p>",
         "diagram": "  tokens -> 1  2  #  #  3  4  #  #  5  #  #\n            ^ next() returns this and moves on"},
        {"code": "        def build() -> Optional[TreeNode]:\n            val = next(tokens)\n            if val == \"#\":\n                return None",
         "explain": "<p>Take the next token. A marker means this position holds no node; return <code>None</code> and let the caller attach it as a missing child. Note that <code>build</code> takes no arguments: the iterator's position is the only state.</p>",
         "diagram": "  build(): next() = \"1\"  -> make node 1\n    build(): next() = \"2\"  -> make node 2\n      build(): next() = \"#\" -> None  (2.left)\n      build(): next() = \"#\" -> None  (2.right)"},
        {"code": "            node = TreeNode(int(val))\n            node.left = build()\n            node.right = build()\n            return node",
         "explain": "<p>Mirror of the writer. Create the node, then build the left subtree, which consumes exactly the tokens the writer emitted for the left subtree, then build the right. The order of these two calls must match <code>serialize</code> exactly.</p>",
         "diagram": "  remaining after node 2 is done: 3  4  #  #  5  #  #\n    build(): \"3\" -> node 3\n      build(): \"4\" -> node 4, left \"#\", right \"#\"\n      build(): \"5\" -> node 5, left \"#\", right \"#\"\n  node 1: left = node 2, right = node 3\n          1\n         / \\\\\n        2   3\n           / \\\\\n          4   5"},
        {"code": "        return build()",
         "explain": "<p>Build from the first token, which is the root. For <code>\"#\"</code> the first call returns <code>None</code> immediately, reconstructing the empty tree.</p>",
         "diagram": None},
    ],
    "complexity": "Time O(n) for each direction, every node and null marker is touched once. Space O(n) for the token list plus O(h) recursion depth.",
}

TESTS = """
c = Codec()
t = build_tree([1, 2, 3, None, None, 4, 5])
assert c.serialize(t) == "1,2,#,#,3,4,#,#,5,#,#"
assert to_level_order(c.deserialize(c.serialize(t))) == [1, 2, 3, None, None, 4, 5]
assert c.serialize(None) == "#"
assert c.deserialize(c.serialize(None)) is None
assert to_level_order(c.deserialize(c.serialize(build_tree([1, 2])))) == [1, 2]
assert to_level_order(c.deserialize(c.serialize(build_tree([1, None, 2])))) == [1, None, 2]
assert to_level_order(c.deserialize(c.serialize(build_tree([-5, 100, None, -12])))) == [-5, 100, None, -12]
assert to_level_order(c.deserialize(c.serialize(build_tree([7])))) == [7]
"""
