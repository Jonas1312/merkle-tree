#!/usr/bin/env python
# coding:utf-8
"""
  Purpose:  Tests for Merkle signature class
  Created:  24/04/2017
"""

import merkle_tree
import unittest
import hashlib

class merkle_tree_test(unittest.TestCase):

    """Tests the merkle_tree functions"""

    def setUp(self):
        """Initialization"""
        self.mk = merkle_tree.MerkleTree(n_leaves=8)
        self.mk.add_node("test", (0, 0))
        self.mk.add_node("retest", (0, 1))
        self.mk.add_node("test", (0, 2))
        self.mk.add_node("world", (0, 3))
        self.mk.add_node("test", (0, 4))
        self.mk.add_node("again", (0, 5))
        self.mk.add_node("test", (0, 6))
        self.mk.add_node("andagain", (0, 7))
        self.mk.generate_tree()

    def test_add_node(self):
        """Tests add_node"""

        data1 = None
        data2 = 'a6'
        data3 = bytearray.fromhex('a6')
        data4 = "test"

        position1 = 0,0
        position2 = 1,1
        position3 = 2,0
        position4 = 0,3

        self.mk.add_node(data1, position1)
        self.mk.add_node(data2, position2, True)
        self.mk.add_node(data3, position3, True)
        self.mk.add_node(data4, position4)

        self.assertIsNone(self.mk.tree[position1])
        self.assertEqual(bytearray.fromhex(data2),self.mk.tree[position2])
        self.assertEqual(data3,self.mk.tree[position3])
        self.assertEqual(bytearray(hashlib.sha256(data4.encode('utf-8')).digest()),self.mk.tree[position4])

    def test_generate_tree(self):
        """Tests generate_tree"""
        node_0_0 = bytearray(hashlib.sha256("test".encode('utf-8')).digest())
        node_0_1 = bytearray(hashlib.sha256("retest".encode('utf-8')).digest())
        node_0_2 = bytearray(hashlib.sha256("test".encode('utf-8')).digest())
        node_0_3 = bytearray(hashlib.sha256("world".encode('utf-8')).digest())
        node_0_4 = bytearray(hashlib.sha256("test".encode('utf-8')).digest())
        node_0_5 = bytearray(hashlib.sha256("again".encode('utf-8')).digest())
        node_0_6 = bytearray(hashlib.sha256("test".encode('utf-8')).digest())
        node_0_7 = bytearray(hashlib.sha256("andagain".encode('utf-8')).digest())
        node_1_0 = bytearray(hashlib.sha256(node_0_0 + node_0_1).digest())
        node_1_1 = bytearray(hashlib.sha256(node_0_2 + node_0_3).digest())
        node_1_2 = bytearray(hashlib.sha256(node_0_4 + node_0_5).digest())
        node_1_3 = bytearray(hashlib.sha256(node_0_6 + node_0_7).digest())
        node_2_0 = bytearray(hashlib.sha256(node_1_0 + node_1_1).digest())
        node_2_1 = bytearray(hashlib.sha256(node_1_2 + node_1_3).digest())
        node_3_0 = bytearray(hashlib.sha256(node_2_0 + node_2_1).digest())

        self.assertEqual(node_1_0, self.mk.tree[1, 0])
        self.assertEqual(node_1_1, self.mk.tree[1, 1])
        self.assertEqual(node_1_2, self.mk.tree[1, 2])
        self.assertEqual(node_1_3, self.mk.tree[1, 3])
        self.assertEqual(node_2_0, self.mk.tree[2, 0])
        self.assertEqual(node_2_1, self.mk.tree[2, 1])
        self.assertEqual(node_3_0, self.mk.tree[3, 0])

