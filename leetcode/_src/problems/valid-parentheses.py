PROBLEM = {
    "slug": "valid-parentheses", "number": 20, "title": "Valid Parentheses", "category": "String", "difficulty": "Easy",
    "url": "https://leetcode.com/problems/valid-parentheses/", "premium": False,
    "statement_html": """<p>You are given a string <code>s</code> made only of the six bracket characters <code>( ) [ ] { }</code>. Decide whether the brackets are properly balanced: every opening bracket must be closed by the same kind of bracket, and brackets must close in the reverse order they were opened, so no pair may cross another pair.</p>
<pre>
Input:  s = "{[()]}"
Output: true          every bracket closes the most recent open one

Input:  s = "([)]"
Output: false         the ")" arrives while "[" is still open

Input:  s = "(("
Output: false         two brackets never get closed
</pre>
<ul>
  <li>1 &le; len(s) &le; 10<sup>4</sup></li>
  <li><code>s</code> contains only the characters <code>()[]{}</code></li>
</ul>""",
    "intro_html": """<p><strong>A stack of open brackets.</strong> Scan left to right. Every opening bracket is pushed; every closing bracket must match the bracket on top of the stack, which is the most recently opened and still unclosed one. If it matches we pop, otherwise the string is invalid. At the end the stack must be empty. The stack is exactly the right structure because brackets close in last-opened, first-closed order.</p>""",
    "blocks": [
        {"code": "class Solution:\n    def isValid(self, s: str) -> bool:",
         "explain": "<p>LeetCode calls <code>isValid</code> with the bracket string and expects a boolean. There is no need for imports; a plain list serves as the stack.</p>",
         "diagram": None},
        {"code": "        pairs = {\")\": \"(\", \"]\": \"[\", \"}\": \"{\"}",
         "explain": "<p>A lookup from each <strong>closing</strong> bracket to the <strong>opening</strong> bracket it must match. Keying on the closer is deliberate: when we meet a closer we need to know what should be on top of the stack, and this dict answers in O(1). It also doubles as the test for \"is this character a closer\".</p>",
         "diagram": "  pairs:   \")\" -> \"(\"     \"]\" -> \"[\"     \"}\" -> \"{\""},
        {"code": "        stack = []",
         "explain": "<p>The stack of brackets that have been opened but not yet closed. Python lists give <code>append</code> and <code>pop</code> at the end in O(1), which is all a stack needs.</p>",
         "diagram": "  stack = []        (top is the right end)"},
        {"code": "        for ch in s:",
         "explain": "<p>One pass over the characters. Each character is handled once and the decision about it is made immediately, so we never need to look ahead or backtrack.</p>",
         "diagram": "  s = \"{[()]}\"\n  ch:  {    [    (    )    ]    }"},
        {"code": "            if ch in pairs:",
         "explain": "<p>Is this a closing bracket? Only closers are keys of <code>pairs</code>, so membership in the dict is the test. Openers fall through to the <code>else</code> branch below.</p>",
         "diagram": None},
        {"code": "                if not stack or stack[-1] != pairs[ch]:\n                    return False",
         "explain": "<p>Two ways a closer can be wrong. If the stack is empty there is nothing to close, as in <code>\")(\"</code>. If the top of the stack is a different kind of opener, the pairs cross, as in <code>\"([)]\"</code>. Either way we can stop immediately: no later character can repair this.</p>",
         "diagram": "  s = \"([)]\"\n  ch=\"(\"  push          stack = [\"(\"]\n  ch=\"[\"  push          stack = [\"(\", \"[\"]\n  ch=\")\"  needs \"(\" but top is \"[\"  -> return False"},
        {"code": "                stack.pop()",
         "explain": "<p>The closer matched the top opener, so that pair is complete. Popping removes the opener and exposes whatever was opened before it, which is exactly the bracket the next closer must match.</p>",
         "diagram": "  s = \"{[()]}\"\n  ch=\"{\"  push   stack = [\"{\"]\n  ch=\"[\"  push   stack = [\"{\", \"[\"]\n  ch=\"(\"  push   stack = [\"{\", \"[\", \"(\"]\n  ch=\")\"  pop    stack = [\"{\", \"[\"]\n  ch=\"]\"  pop    stack = [\"{\"]\n  ch=\"}\"  pop    stack = []"},
        {"code": "            else:\n                stack.append(ch)",
         "explain": "<p>An opening bracket is always acceptable at this moment; whether it is valid depends on what comes later. We push it and let a future closer decide.</p>",
         "diagram": None},
        {"code": "        return not stack",
         "explain": "<p>After the scan every opener must have been popped by a matching closer. Anything left on the stack was never closed, as in <code>\"((\"</code>, so the string is valid only when the stack is empty.</p>",
         "diagram": "  s = \"((\"    after loop: stack = [\"(\", \"(\"]  -> False\n  s = \"{[()]}\" after loop: stack = []          -> True"},
    ],
    "complexity": "Time O(n), one pass with O(1) work per character. Space O(n) for the stack when the string is all openers.",
}

TESTS = """
s = Solution()
assert s.isValid("{[()]}") is True
assert s.isValid("([)]") is False
assert s.isValid("((") is False
assert s.isValid("()") is True
assert s.isValid("()[]{}") is True
assert s.isValid(")(") is False
assert s.isValid("]") is False
assert s.isValid("(") is False
assert s.isValid("{{}}[]") is True
"""
