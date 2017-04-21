#!/usr/bin/env python
# coding:utf-8
"""
  Purpose:  Merkle tree implementation.
  Created:  19/04/2017
"""

import hashlib
from math import log2, floor


class MerkleTree:
    """MerkleTree class.

    Attributes:
        tree (dict): Merkle tree.
        n_levels (int): Number of levels in the tree
        n_leaves (int): Number of leaves in the tree (at level 0)
        
    """

    def __init__(self):
        """Constructor for MerkleTree."""
        self.tree = {}
        self.n_levels = None
        self.n_leaves = 0

    def add_leaf(self, data, position=None, hashed=False):
        """Add a leaf to the tree.
        
        Note:
            If 'hashed' is False then 'data' will be hashed.

        """
        if position is None:
            position = self.n_leaves
        if not hashed:
            self.tree[(0, position)] = self.hash(data)
        else:
            self.tree[(0, position)] = data
        self.n_leaves += 1

    def generate_tree(self):
        """Generate tree."""
        while floor(log2(self.n_leaves)) != log2(self.n_leaves):
            self.add_leaf("Null", len(self.tree))

        self.n_levels = int(log2(self.n_leaves)) + 1
        for level in range(1, self.n_levels):
            for pos in range(int(self.n_leaves / 2 ** level)):
                self.tree[(level, pos)] = self.hash(
                    self.tree[(level - 1, 2 * pos)] + self.tree[(level - 1, 2 * pos + 1)])

    def get_root(self):
        """Get root of the tree.
        
        Returns:
            (bytes): root hash.
        
        """
        return self.tree[(self.n_levels - 1, 0)]

    @staticmethod
    def hash(data):
        """Calculate sha256 hash of 'data'.

        Returns:
            (bytes): bytes of the hash.

        """
        if type(data) is not bytes:
            data = data.encode('utf-8')
        return hashlib.sha256(data).digest()


def main():
    tree = MerkleTree()
    tree.add_leaf("test")
    tree.add_leaf("retest")
    tree.add_leaf("retest")
    tree.add_leaf("retest")
    tree.add_leaf("retest")
    tree.generate_tree()
    for (key, value) in tree.tree.items():
        print(key, value.hex())
    print(tree.get_root().hex())


if __name__ == "__main__":
    main()
