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
        """Initialisation"""
        MerkleTree1 = MerkleTree.__init__(self,8)

    def test_add_node(self):
        """Tests add_node"""

        data1 = None
        data2 = hex(25)
        data3 = bytearray.fromhex(data2())
        data4 = "test"

        position1 = [0,0]
        position2 = [1,2]
        position3 = [2,1]
        position4 = [0,3]

        add_node(merkle_tree_test,data1,position1)
        add_node(merkle_tree_test, data2, position2,True)
        add_node(merkle_tree_test, data3, position3,True)
        add_node(merkle_tree_test, data4, position4)

        assertIsNone(merkle_tree_test[position1])
        assertIs(bytearray.fromhex(data2),merkle_tree_test[position2])
        assertIs(data3,merkle_tree_test[position3])
        assertIs(bytearray(hashlib.sha256(data4.encode('utf-8')).digest()),merkle_tree_test[position4])


