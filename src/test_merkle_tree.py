#!/usr/bin/env python
# coding:utf-8
"""
  Purpose:  Tests for Merkle signature class
  Created:  24/04/2017
"""

from merkle_tree import MerkleTree
import unittest
import hashlib

class merkle_tree_test(unittest.TestCase):

    """Tests the merkle_tree functions"""

    def setUp(self):
        """Initialization"""
        self.merkle_tree1 = MerkleTree(8)

    def test_add_node(self):
        """Tests add_node"""

        data1 = None
        data2 = 'A6'
        data3 = bytearray.fromhex('A6')
        data4 = "test"

        position1 = 0,0
        position2 = 1,2
        position3 = 2,1
        position4 = 0,3

        self.merkle_tree1.add_node(data1, position1)
        self.merkle_tree1.add_node(data2, position2, True)
        self.merkle_tree1.add_node(data3, position3, True)
        self.merkle_tree1.add_node(data4, position4)

        self.assertIsNone(self.merkle_tree1.tree[position1])
        self.assertIs(bytearray.fromhex(data2),self.merkle_tree1.tree[position2])
        self.assertIs(data3,self.merkle_tree1.tree[position3])
        self.assertIs(bytearray(hashlib.sha256(data4.encode('utf-8')).digest()),self.merkle_tree1.tree[position4])


