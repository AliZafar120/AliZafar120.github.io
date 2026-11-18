# LeetCode walkthrough problem files: specification

One Python file per problem in `problems/<slug>.py`, where `<slug>` is the LeetCode URL slug
(e.g. `two-sum`). The file defines exactly two module-level names: `PROBLEM` (a dict) and `TESTS` (a string).
Look at `problems/two-sum.py` for the exemplar and copy its shape exactly.

## PROBLEM dict

| key | type | notes |
|---|---|---|
| slug | str | must equal the file name without `.py` |
| number | int | the LeetCode problem number |
| title | str | LeetCode title |
| category | str | one of: Array, Binary, Dynamic Programming, Graph, Interval, Linked List, Matrix, String, Tree, Heap (as assigned) |
| difficulty | str | Easy / Medium / Hard (LeetCode's rating) |
| url | str | https://leetcode.com/problems/<slug>/ |
| premium | bool | True for problems marked "Leetcode Premium" in the list |
| statement_html | str | the problem **in your own words**: 2 to 4 sentences, then 1 or 2 small examples you make up yourself inside `<pre>`, then a short `<ul>` of the key constraints. Do NOT copy LeetCode's text or its examples. For premium problems state the task fully since readers cannot open the page. |
| intro_html | str | one `<p>`: the approach in 2 to 3 sentences, naming the core technique (two pointers, DP table, BFS...). |
| blocks | list | the solution, cut into 5 to 14 consecutive pieces. Each block: `{"code": str, "explain": str (HTML, 1 to 3 `<p>`), "diagram": str or None}`. The `code` strings joined with `"\n"` MUST be the complete, runnable solution: a `class Solution:` with the LeetCode method name and signature (type hints welcome), plus any imports at the top. Keep each block to 1 to 6 lines; cut at meaningful boundaries. Explain what the line does AND why, in the style of the exemplar. |
| complexity | str | e.g. "Time O(n), space O(n) for the hash map." |

### Explanations
Write for someone who knows Python but is new to the technique. Every block explains the idea, not just the syntax.
At least half the blocks carry an ASCII `diagram` that traces a concrete small example (state of pointers, table,
stack, queue...). Diagrams are plain text, monospace, under 14 lines and 70 columns. Use `&lt;` `&gt;` `&amp;` in
`explain` HTML, never in `diagram` (it is escaped automatically). Use `<code>` for identifiers.
No em dashes. British or American spelling, either, but consistent.

### Solutions
Idiomatic Python 3.10, the standard optimal approach for an interview (the one a strong candidate would write),
no external packages. `from typing import List, Optional` where needed. For linked list / tree / graph problems the
grader supplies `ListNode`, `TreeNode`, `Node` classes (see `helpers.py`); your code may reference them without
defining them, but if you define them, keep the same attribute names. For design problems (Trie, MedianFinder,
Codec...) the class name is the LeetCode one, not `Solution`.

## TESTS string
Python code executed after the solution with these names available: everything from `helpers.py`
(`ListNode, TreeNode, Node, build_list, to_list, build_tree, to_level_order, build_graph, graph_to_adj`), plus the
solution's classes. Use plain `assert` statements, at least 4 per problem, covering: a normal case, an edge case
(empty / single element / all equal), and the examples from your statement. For outputs where order does not matter,
sort before comparing. Print nothing.

## Checking your work
Run `python3 run_tests.py <slug> [<slug> ...]` from this directory. It execs the joined code, runs TESTS, and also
validates the dict (keys, block count, diagram share, slug, HTML sanity). Fix until every file you own prints PASS.
