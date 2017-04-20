#!/usr/bin/env python
# coding:utf-8
"""
  Purpose:  Merkle tree class
  Created:  19/04/2017
"""

import hashlib


class MerkleTree:
    """MerkleTree class

    Attributes:
        leaves (list): leaves of the tree.
        tree (): Merkle tree
        hash_function (builtin_function_or_method): hash function used.
        
    """

    def __init__(self, hash_type='sha256'):
        """Constructor for MerkleTree
        
        Args:
            hash_type (str): Hash type, 'sha256' or 'md5'
            
        """
        self.leaves = list()
        self.tree = None
        hash_type = hash_type.lower()
        if hash_type == 'sha256':
            self.hash_function = hashlib.sha256
        elif hash_type == 'md5':
            self.hash_function = hashlib.md5
        else:
            raise Exception("Invalid hash type")

    def add_leaf(self, data, hashed=False):
        """Add a leaf or a list of leafs.
        
        Note:
            If 'hashed' is False then 'data' will be hashed.

        """
        if type(data) is not list:
            data = [data]
        if not hashed:
            self.leaves += [bytearray.fromhex(self.generate_hash(leaf)) for leaf in data]
        else:
            self.leaves += [bytearray.fromhex(leaf) for leaf in data]

    def generate_tree(self):
        pass

    def generate_hash(self, data):
        if type(data) is not bytes:
            data = data.encode('utf-8')
        hash_object = self.hash_function(data)
        hex_dig = hash_object.hexdigest()
        return hex_dig

    @staticmethod
    def to_hex(byte_array):
        return byte_array.hex()


def main():
    tree = MerkleTree()

    tree.add_leaf("test")
    tree.add_leaf("9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08", hashed=True)
    tree.add_leaf(["test", "retest", "reretest"])
    with open('9a30a503b2862c51c3c5acd7fbce2f1f784cf4658ccf8e87d5023a90c21c0714.txt', 'rb') as file:
        buf = file.read()
        tree.add_leaf(buf)

    for leaf in tree.leaves:
        print(tree.to_hex(leaf))


if __name__ == "__main__":
    main()
