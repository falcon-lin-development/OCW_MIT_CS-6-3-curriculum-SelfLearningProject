class RangeIndex(object):
    """Array-based range index implementation.
      Implement AVL version
  """

    def __init__(self):
        """Initially empty range index."""
        self.data = []
        self.root = None

    def add(self, key):
        """Inserts a key in the range index."""
        if key is None:
            raise ValueError('Cannot insert nil in the index')

        if self.root is None:
            self.root = _BST_node(key)
            return 0

        comparison_node = self.root
        while True:
            if comparison_node is None:
                break
            if key <= comparison_node.key:
                if comparison_node.left is None:
                    new_node = _BST_node(key, comparison_node)
                    comparison_node.left = new_node
                    break
                comparison_node = comparison_node.left
            else:
                if comparison_node.right is None:
                    new_node = _BST_node(key, comparison_node)
                    comparison_node.right = new_node
                    break
                comparison_node = comparison_node.right
        self._fix_RI(new_node)

    def remove(self, key):
        """Removes a key node from the range index. if it exists"""
        node = self._search(key)
        if node is None:
            raise Exception("{0} doesn\'t in rangeIndex".format(key))
        # print node, node.is_leaf()
        if node.is_leaf():  # simple remove
            if node.parent.left == node:
                node.parent.left = None
                node.parent = None
                self._fix_RI(node.parent)
                del node
            elif node.parent.right == node:
                node.parent.right = None
                node.parent = None
                self._fix_RI(node.parent)
                del node
            else:  # no parent == root
                self.root = None
                del node
        elif bool(node.left) != bool(node.right):  # logical xor // only one branch
            if node.parent.left == node:  # node == parent.left
                if bool(node.left):
                    node.parent.left = node.left
                    node.left.parent = node.parent
                    self._fix_RI(node.parent)
                    del node
                else:
                    node.parent.left = node.right
                    node.right.parent = node.parent
                    self._fix_RI(node.parent)
                    del node
            else:  # node == parent.right
                if bool(node.left):
                    node.parent.right = node.left
                    node.left.parent = node.parent
                    self._fix_RI(node.parent)
                    del node
                else:
                    node.parent.right = node.right
                    node.right.parent = node.parent
                    self._fix_RI(node.parent)
                    del node
        else:  # complex remove
            successor = self._successor(node.key)
            node.key = successor.key
            self.remove(successor.key)

    def list(self, first_key, last_key):
        """List of values for the keys that fall within [first_key, last_key]."""

        def node_list(node, l, h, result):
            if node is None:
                return
            if l <= node.key <= h:
                result.append(node.key)
            if node.key >= l:
                node_list(node.left, l, h, result)
            if node.key <= h:
                node_list(node.right, l, h, result)

        def LCA(tree_root, l, h):
            node = tree_root
            while True:
                if node is None or (l <= node.key <= h):
                    break
                if l < node.key:
                    node = node.left
                else:
                    node = node.right
            return node

        lca = LCA(self.root, first_key, last_key)
        result = []
        node_list(lca, first_key, last_key, result)
        return result

    def count(self, first_key, last_key):
        """Number of keys that fall within [first_key, last_key]."""
        return len(self.list(first_key, last_key))

    def _fix_RI(self, node):
        """after updates, fix RI(AVL) will maintain representative Invariant; potentially change tree structure"""
        if node is None:
            return
        # check AVL
        # print node.is_AVL()
        # print node
        if node.is_AVL():
            node.fix_height()
            node.fix_size()
            if node.parent is None:
                self.root = node
            self._fix_RI(node.parent)
            return
        else:
            lh, rh = node.get_lh(), node.get_rh()
            # print lh, rh
            if lh > rh:
                if node.left.get_rh() > node.left.get_lh():  # if zigzag
                    self._lr(node.left)
                self._rr(node)
            else:
                if node.right.get_lh() > node.right.get_rh():  # if zigzag
                    self._rr(node.right)
                self._lr(node)

    def _lr(self, node):
        """left rotate"""
        x = node
        y = node.right
        assert y is not None, "no rotation can operate on leaf"
        A = x.left
        B = y.left
        C = y.right
        # print x
        # print y
        # print A
        # print B
        # print C
        # swap 1
        y.parent = x.parent
        if x.parent is not None:
            if x.parent.left == x:
                x.parent.left = y
            else:
                x.parent.right = y
        # swap 2
        y.left = x
        x.parent = y
        # swap 3
        x.right = B
        if B is not None:
            B.parent = x

        self._fix_RI(x)

    def _rr(self, node):
        """right rotate"""
        y = node
        x = node.left
        assert x is not None, "no rotation can operate on leaf"
        A = x.left
        B = x.right
        C = y.right

        # swap 1
        x.parent = y.parent
        if y.parent is not None:
            if y.parent.left == y:
                y.parent.left = x
            else:
                y.parent.right = x
        # swap 2
        x.right = y
        y.parent = x
        # swap 3
        y.left = B
        if B is not None:
            B.parent = y

        self._fix_RI(y)

    def _find_min(self, key):
        """return the minimum node of the pruned subtree rooted at key node; if the key node exist"""
        node = self._search(key)
        if node is None:
            raise Exception('{0} doesn\'t in rangeIndex'.format(key))

        if node.left is not None:
            return self._find_min(node.left.key)
        else:
            return node

    def _successor(self, key):
        """return the node of successor if there's a node for the key"""
        node = self._search(key)
        if node is None:
            raise Exception('{0} doesn\'t in rangeIndex'.format(key))

        if node.right is not None: # simple case
            return self._find_min(node.right.key)
        elif node.parent is not None: # complex case
            while node.parent is not None and node.parent.right is node:
                node = node.parent
            if node.parent is None:
                return None
            else:
                return node.parent
        else:
            return None

    def _search(self, key):
        """using a key to search for a node or there isn't one"""
        comparison_node = self.root
        while comparison_node is not None:
            if key == comparison_node.key:
                return comparison_node
            elif key <= comparison_node.key:
                comparison_node = comparison_node.left
            else:
                comparison_node = comparison_node.right
        return None



class _BST_node(object):
    def __init__(self, key, parent=None, left=None, right=None):
        self.key = key
        self.parent = parent
        self.left = left
        self.right = right
        self.size = self._calc_size()
        self.height = self._calc_height()

    def is_leaf(self):
        return not bool(self.left) and not bool(self.right)

    def is_AVL(self):
        if self.left is not None:
            lh = self.left.height
        else:
            lh = -1
        if self.right is not None:
            rh = self.right.height
        else:
            rh = -1
        return abs(lh - rh) <= 1

    def get_lh(self):
        if self.left is None:
            return -1
        return self.left.height

    def get_rh(self):
        if self.right is None:
            return -1
        return self.right.height

    def fix_size(self):
        self.size = self._calc_size()

    def fix_height(self):
        self.height = self._calc_height()

    def _calc_size(self):
        if self.left is not None:
            ls = self.left.size
        else:
            ls = 0
        if self.right is not None:
            rs = self.right.size
        else:
            rs = 0
        return ls + rs + 1

    def _calc_height(self):
        if self.left is not None:
            lh = self.left.height
        else:
            lh = -1
        if self.right is not None:
            rh = self.right.height
        else:
            rh = -1
        return max(lh, rh) + 1

    def __lt__(self, other):
        # :nodoc: Delegate comparison to keys.
        return self.key < other.key

    def __le__(self, other):
        return self.key <= other.key

    def __gt__(self, other):
        # :nodoc: Delegate comparison to keys.
        return self.key > other.key

    def __ge__(self, other):
        # :nodoc: Delegate comparison to keys.
        return self.key >= other.key

    def __eq__(self, other):
        # :nodoc: Delegate comparison to keys.
        return self.key == other.key

    def __ne__(self, other):
        # :nodoc: Delegate comparison to keys.
        return self.key != other.key
    def __str__(self):
        out = "key:{0}, parent:{1}, left:{2}, right:{3}, size:{4}, height:{5}".format(self.key, \
                        bool(self.parent), bool(self.left), bool(self.right), self.size, self.height)
        return out


a = RangeIndex()
a.add(1)
a.add(2)
a.add(3)
a.add(4)
a.add(5)
a.remove(5)
print a._search(2)
# print a._successor(3)
# print a.count(-1000, 1000)
# print a.list(-1000, 1000)
# print a.root
# print a.root.left
# print a.root.right

