PROBLEM = {
    "slug": "group-anagrams", "number": 49, "title": "Group Anagrams", "category": "String", "difficulty": "Medium",
    "url": "https://leetcode.com/problems/group-anagrams/", "premium": False,
    "statement_html": """<p>Given a list of lowercase words, gather the anagrams together: words made of exactly the same letters with the same multiplicities belong in the same group. Return the groups as a list of lists. The order of the groups, and of words within a group, does not matter.</p>
<pre>
Input:  strs = ["cat", "act", "dog", "god", "odg", "bird"]
Output: [["cat", "act"], ["dog", "god", "odg"], ["bird"]]

Input:  strs = [""]
Output: [[""]]
</pre>
<ul>
  <li>1 &le; len(strs) &le; 10<sup>4</sup>, 0 &le; len(strs[i]) &le; 100</li>
  <li>Words contain only lowercase English letters</li>
</ul>""",
    "intro_html": """<p><strong>Hash map keyed by a 26-letter count signature.</strong> Two words are anagrams exactly when they have the same letter histogram, so the histogram itself is a perfect group key. For each word we build a 26-element count, convert it to a tuple (lists are not hashable), and append the word to that key's bucket. Compared with sorting each word as the key, counting is O(L) rather than O(L log L) per word.</p>""",
    "blocks": [
        {"code": "from collections import defaultdict\nfrom typing import List\n\nclass Solution:\n    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:",
         "explain": "<p>LeetCode calls <code>groupAnagrams</code> with the list of words and expects a list of groups. <code>defaultdict(list)</code> creates an empty bucket the first time a key is touched, so we never have to check for a missing key.</p>",
         "diagram": None},
        {"code": "        groups = defaultdict(list)",
         "explain": "<p>The map from <strong>signature</strong> to <strong>list of words</strong> with that signature. Every bucket will end up being one group in the answer.</p>",
         "diagram": "  groups = {}        signature tuple -> [words]"},
        {"code": "        for word in strs:",
         "explain": "<p>Each word is handled independently and exactly once; the work per word depends only on its length.</p>",
         "diagram": "  strs = [\"cat\", \"act\", \"dog\", \"god\", \"odg\", \"bird\"]"},
        {"code": "            count = [0] * 26\n            for ch in word:\n                count[ord(ch) - ord(\"a\")] += 1",
         "explain": "<p>Build the letter histogram for this word: slot 0 is <code>a</code>, slot 25 is <code>z</code>. Anagrams produce identical histograms no matter how their letters are ordered, which is the whole reason this works as a key.</p>",
         "diagram": "  \"cat\": a=1 c=1 t=1  -> [1,0,1,0,...,1(t),...,0]\n  \"act\": a=1 c=1 t=1  -> same histogram\n  \"dog\": d=1 g=1 o=1  -> different histogram"},
        {"code": "            groups[tuple(count)].append(word)",
         "explain": "<p>A list cannot be a dict key because it is mutable, so we freeze it into a tuple. Then append the word to its bucket. Because <code>groups</code> is a <code>defaultdict</code>, a brand new signature silently gets a fresh empty list before the append.</p>",
         "diagram": "  after \"cat\":  {(a1,c1,t1): [\"cat\"]}\n  after \"act\":  {(a1,c1,t1): [\"cat\",\"act\"]}\n  after \"dog\":  {..., (d1,g1,o1): [\"dog\"]}\n  after \"god\":  {..., (d1,g1,o1): [\"dog\",\"god\"]}\n  after \"odg\":  {..., (d1,g1,o1): [\"dog\",\"god\",\"odg\"]}\n  after \"bird\": {..., (b1,d1,i1,r1): [\"bird\"]}"},
        {"code": "        return list(groups.values())",
         "explain": "<p>The keys were only a means of grouping; the answer is just the buckets. Since any order is accepted we return the values as they come. The empty string hashes to the all-zero tuple and forms its own group, as required.</p>",
         "diagram": "  [[\"cat\",\"act\"], [\"dog\",\"god\",\"odg\"], [\"bird\"]]"},
    ],
    "complexity": "Time O(N * L) where N is the number of words and L the maximum word length: each word is counted once and each tuple key has fixed size 26. Space O(N * L) to hold the words in their groups plus O(N) keys.",
}

TESTS = """
s = Solution()

def norm(groups):
    return sorted(sorted(g) for g in groups)

assert norm(s.groupAnagrams(["cat", "act", "dog", "god", "odg", "bird"])) == [["act", "cat"], ["bird"], ["dog", "god", "odg"]]
assert s.groupAnagrams([""]) == [[""]]
assert s.groupAnagrams(["a"]) == [["a"]]
assert norm(s.groupAnagrams(["ab", "ba", "ab"])) == [["ab", "ab", "ba"]]
assert norm(s.groupAnagrams(["x", "y", "z"])) == [["x"], ["y"], ["z"]]
assert norm(s.groupAnagrams(["eat", "tea", "tan", "ate", "nat", "bat"])) == [["ate", "eat", "tea"], ["bat"], ["nat", "tan"]]
assert norm(s.groupAnagrams(["", "", "a"])) == [["", ""], ["a"]]
"""
