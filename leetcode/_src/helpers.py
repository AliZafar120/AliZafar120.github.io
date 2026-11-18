"""Shared helpers available to every solution's TESTS block (and to solutions that need the node classes)."""
from typing import Optional, List

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val; self.next = next

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val; self.left = left; self.right = right

class Node:  # for Clone Graph
    def __init__(self, val=0, neighbors=None):
        self.val = val; self.neighbors = neighbors if neighbors is not None else []

def build_list(values):
    head = cur = None
    for v in values:
        n = ListNode(v)
        if head is None: head = cur = n
        else: cur.next = n; cur = n
    return head

def to_list(head):
    out = []
    while head: out.append(head.val); head = head.next
    return out

def build_tree(values):
    """LeetCode level-order encoding, e.g. [3,9,20,None,None,15,7]."""
    if not values or values[0] is None: return None
    root = TreeNode(values[0]); q = [root]; i = 1
    while q and i < len(values):
        node = q.pop(0)
        if i < len(values) and values[i] is not None:
            node.left = TreeNode(values[i]); q.append(node.left)
        i += 1
        if i < len(values) and values[i] is not None:
            node.right = TreeNode(values[i]); q.append(node.right)
        i += 1
    return root

def to_level_order(root):
    out, q = [], [root]
    while q:
        n = q.pop(0)
        if n is None: out.append(None); continue
        out.append(n.val); q.append(n.left); q.append(n.right)
    while out and out[-1] is None: out.pop()
    return out

def build_graph(adj):
    """adj: LeetCode adjacency list, 1-indexed, e.g. [[2,4],[1,3],[2,4],[1,3]]. Returns node 1 or None."""
    if not adj: return None
    nodes = [Node(i + 1) for i in range(len(adj))]
    for i, nb in enumerate(adj): nodes[i].neighbors = [nodes[j - 1] for j in nb]
    return nodes[0]

def graph_to_adj(node):
    if node is None: return []
    seen = {}; order = []
    stack = [node]
    while stack:
        n = stack.pop()
        if n.val in seen: continue
        seen[n.val] = n; order.append(n)
        stack.extend(n.neighbors)
    size = max(seen)
    return [[nb.val for nb in seen[i].neighbors] if i in seen else [] for i in range(1, size + 1)]
