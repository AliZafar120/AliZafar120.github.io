# LeetCode walkthrough sources

The pages in `leetcode/<slug>/` are generated. Edit the source files here, not the HTML.

- `problems/<slug>.py`: one file per problem (`PROBLEM` dict + `TESTS`), format in `SPEC.md`.
- `python3 run_tests.py [slug ...]`: validates every file and executes its solution against its tests.
- `python3 build.py`: regenerates `../<slug>/index.html` for all problems and `../index.html`.
- `helpers.py`: ListNode/TreeNode/Node and builders used by tests.

Jekyll does not publish folders that start with an underscore, so this directory is not on the live site.
