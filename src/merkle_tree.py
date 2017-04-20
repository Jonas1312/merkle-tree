#!/usr/bin/env python
# coding:utf-8
"""
  Purpose:  Merkle tree implementation.
  Created:  19/04/2017
"""

import hashlib


class MerkleTree:
    """MerkleTree class.

    Attributes:
        leaves (list): Leaves of the tree.
        tree (): Merkle tree.
        
    """

    def __init__(self):
        """Constructor for MerkleTree."""
        self.leaves = list()
        self.tree = None

    def add_leaf(self, data, hashed=False):
        """Add a leaf or a list of leafs.
        
        Note:
            If 'hashed' is False then 'data' will be hashed.

        """
        if type(data) is not list:
            data = [data]
        if not hashed:
            self.leaves += [bytearray.fromhex(self.hash(leaf)) for leaf in data]
        else:
            self.leaves += [bytearray.fromhex(leaf) for leaf in data]

    def generate_tree(self):
        pass

    @staticmethod
    def hash(data):
        """Calculate sha256 hash of 'data'.
        
        Returns:
            (str): String of the hash.

        """
        if type(data) is not bytes:
            data = data.encode('utf-8')
        return hashlib.sha256(data).hexdigest()


def main():
    tree = MerkleTree()

    tree.add_leaf("test")
    tree.add_leaf("9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08", hashed=True)
    tree.add_leaf(["test", "retest", "reretest"])
    with open('9a30a503b2862c51c3c5acd7fbce2f1f784cf4658ccf8e87d5023a90c21c0714.txt', 'rb') as file:
        buf = file.read()
        tree.add_leaf(buf)

    for leaf in tree.leaves:
        print(leaf.hex())


if __name__ == "__main__":
    main()
