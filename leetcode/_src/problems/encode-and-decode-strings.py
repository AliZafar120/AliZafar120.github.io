PROBLEM = {
    "slug": "encode-and-decode-strings", "number": 271, "title": "Encode and Decode Strings", "category": "String", "difficulty": "Medium",
    "url": "https://leetcode.com/problems/encode-and-decode-strings/", "premium": True,
    "statement_html": """<p>Design a class <code>Codec</code> with two methods. <code>encode(strs)</code> takes a list of strings and packs it into one single string that can be sent over a network. <code>decode(s)</code> takes that single string and must return exactly the original list. The strings may contain <em>any</em> character, including whatever separator you choose, and may be empty, so a plain <code>join</code>/<code>split</code> on a delimiter is not enough. You may not rely on any shared state between encoding and decoding other than the encoded string itself.</p>
<pre>
Input:  strs = ["cat", "", "a#b"]
encode -> "3#cat0#3#a#b"
decode -> ["cat", "", "a#b"]        (identical to the input)

Input:  strs = []
encode -> ""
decode -> []
</pre>
<ul>
  <li>0 &le; len(strs) &le; 200, each string has length 0 to 200</li>
  <li>Strings contain any of the 256 ASCII characters</li>
  <li>Do not use serialisation libraries or eval; the format must be your own</li>
</ul>""",
    "intro_html": """<p><strong>Length-prefix each string.</strong> Write every string as its length in decimal, a <code>#</code> marker, then the raw characters. The decoder reads digits up to the first <code>#</code>, learns exactly how many characters to take, and jumps past them. Because the length tells it where each string ends, the string contents can contain <code>#</code> or anything else without confusion. This is the classic solution to the delimiter problem used by many real wire formats.</p>""",
    "blocks": [
        {"code": "from typing import List\n\nclass Codec:",
         "explain": "<p>This is a design problem, so the class is called <code>Codec</code> rather than <code>Solution</code>. LeetCode creates one instance and calls <code>decode(encode(strs))</code>, comparing the result to the original list.</p>",
         "diagram": None},
        {"code": "    def encode(self, strs: List[str]) -> str:\n        out = []",
         "explain": "<p>Build the encoded pieces in a list and join once at the end. Repeated string concatenation in a loop is quadratic in the worst case; collecting parts and joining is linear.</p>",
         "diagram": "  strs = [\"cat\", \"\", \"a#b\"]\n  out = []"},
        {"code": "        for s in strs:\n            out.append(f\"{len(s)}#{s}\")",
         "explain": "<p>Each string becomes <code>&lt;length&gt;#&lt;content&gt;</code>. The length is written in decimal and may have several digits; the <code>#</code> marks where the digits end. Since lengths are always digits and never contain <code>#</code>, the decoder can always find the marker. The content after it is copied verbatim, including any <code>#</code> it contains.</p>",
         "diagram": "  \"cat\" -> \"3#cat\"\n  \"\"    -> \"0#\"\n  \"a#b\" -> \"3#a#b\"\n  out = [\"3#cat\", \"0#\", \"3#a#b\"]"},
        {"code": "        return \"\".join(out)",
         "explain": "<p>Concatenate the pieces with no separator between them; none is needed because each piece announces its own length. An empty list encodes to the empty string.</p>",
         "diagram": "  \"3#cat\" + \"0#\" + \"3#a#b\"  ->  \"3#cat0#3#a#b\""},
        {"code": "    def decode(self, s: str) -> List[str]:\n        res = []\n        i = 0",
         "explain": "<p>The decoder walks the encoded string with a cursor <code>i</code> that always sits at the start of a length field. <code>res</code> collects the recovered strings in order.</p>",
         "diagram": "  s = \"3#cat0#3#a#b\"\n       i=0"},
        {"code": "        while i < len(s):\n            j = s.index(\"#\", i)\n            length = int(s[i:j])",
         "explain": "<p>While there is data left, find the <code>#</code> that ends the current length field. <code>s.index(\"#\", i)</code> searches only from the cursor onwards, so a <code>#</code> inside an earlier string's content is never mistaken for a marker. The digits between <code>i</code> and <code>j</code> give the length.</p>",
         "diagram": "  s = \"3#cat0#3#a#b\"\n  i=0  j=1  s[0:1]=\"3\"  -> length 3\n  i=5  j=6  s[5:6]=\"0\"  -> length 0\n  i=7  j=8  s[7:8]=\"3\"  -> length 3"},
        {"code": "            res.append(s[j + 1:j + 1 + length])\n            i = j + 1 + length",
         "explain": "<p>The content starts right after the marker and runs for exactly <code>length</code> characters. Slice it out, then move the cursor past it to the next length field. Because the jump is by a known count, a <code>#</code> inside the content (as in <code>\"a#b\"</code>) is skipped over, never interpreted.</p>",
         "diagram": "  s = \"3#cat0#3#a#b\"\n  j=1  take s[2:5]  = \"cat\"   i -> 5\n  j=6  take s[7:7]  = \"\"      i -> 7\n  j=8  take s[9:12] = \"a#b\"   i -> 12  (== len(s), loop ends)\n  res = [\"cat\", \"\", \"a#b\"]"},
        {"code": "        return res",
         "explain": "<p>The cursor has reached the end, so every encoded string has been recovered. An empty encoded string skips the loop entirely and returns <code>[]</code>, which correctly distinguishes <code>[]</code> from <code>[\"\"]</code> (the latter encodes to <code>\"0#\"</code>).</p>",
         "diagram": "  encode([])   = \"\"    -> decode -> []\n  encode([\"\"]) = \"0#\"  -> decode -> [\"\"]"},
    ],
    "complexity": "Time O(total characters) for both encode and decode. Space O(total characters) for the encoded string and the decoded list.",
}

TESTS = """
c = Codec()
assert c.decode(c.encode(["cat", "", "a#b"])) == ["cat", "", "a#b"]
assert c.encode(["cat", "", "a#b"]) == "3#cat0#3#a#b"
assert c.decode(c.encode([])) == []
assert c.decode(c.encode([""])) == [""]
assert c.decode(c.encode(["", ""])) == ["", ""]
assert c.decode(c.encode(["#", "##", "12#34"])) == ["#", "##", "12#34"]
long = "x" * 150
assert c.decode(c.encode([long, "y"])) == [long, "y"]
assert c.decode(c.encode(["hello world", "a,b;c", "\\n\\t"])) == ["hello world", "a,b;c", "\\n\\t"]
"""
