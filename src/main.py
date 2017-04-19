#!/usr/bin/env python
# coding:utf-8
"""
  Purpose:  Main file
  Created:  19/04/2017
"""

from merkle_tree import MerkleTree


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
