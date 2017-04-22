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
        n_levels (int): Number of levels in the tree.
        n_leaves (int): Number of leaves in the tree (at level 0).
        
    """

    def __init__(self, n_leaves):
        """MerkleTree object constructor.
        
        Args:
            n_leaves (int): Number of leaves in the tree.
            
        """
        if floor(log2(n_leaves)) != log2(n_leaves):
            raise ValueError("Wrong number of leaves.")
        self.tree = {}
        self.n_levels = None
        self.n_leaves = n_leaves

    def add_node(self, data, position, hashed=False):
        """Add a node to the tree.
        
        Args:
            data (str/None): Node value.
            position (tuple): Position in the tree (level, index).
            hashed (boolean): 'data' already hashed or not.
            
        Note:
            If 'hashed' is True then 'data' will not be hashed.

        """
        if data is None:
            self.tree[position] = None
        elif hashed:
            self.tree[position] = bytearray.fromhex(data)
        else:
            self.tree[position] = self.hash(data)

    def generate_tree(self):
        """Generate tree.
        
        Note:
            Unknow node value is None.
            
        """
        self.n_levels = int(log2(self.n_leaves)) + 1

        for level in range(1, self.n_levels):
            for pos in range(int(self.n_leaves / 2 ** level)):
                left_child = self.tree[(level - 1, 2 * pos)]
                right_child = self.tree[(level - 1, 2 * pos + 1)]
                if left_child is not None and right_child is not None:
                    self.tree[(level, pos)] = self.hash(left_child + right_child)
                else:
                    self.tree[(level, pos)] = None

    def get_root(self):
        """Get root of the tree.
        
        Returns:
            (bytes): Root hash.
        
        """
        return self.tree[(self.n_levels - 1, 0)]

    def get_brother(self, position):
        """Get the brother node of the node at 'position'.
        
        Returns:
            (None/bytearray): Node hash.
        
        """
        level = position[0]
        index = position[1] + 1 if position[1] % 2 == 0 else position[1] - 1
        try:
            return self.tree[(level, index)]
        except:
            raise ValueError("No brother exists.")

    @staticmethod
    def hash(data):
        """Calculate sha256 hash of 'data'.
        
        Args:
            (str/bytearray): Data to hash

        Returns:
            (bytearray): bytes of the hash.

        """
        if type(data) is not bytearray:
            data = data.encode('utf-8')
        return bytearray(hashlib.sha256(data).digest())


def main():
    mk = MerkleTree(n_leaves=4)
    mk.add_node("test", (0, 0))
    mk.add_node("retest", (0, 1))
    mk.add_node(None, (0, 2))
    mk.add_node("bitcoin", (0, 3))
    mk.generate_tree()

    for key, value in mk.tree.items():
        print(key, value)

    print(mk.get_brother((1, 0)))


if __name__ == "__main__":
    main()
