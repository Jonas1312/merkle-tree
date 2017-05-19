#!/usr/bin/env python
# coding:utf-8
"""
  Purpose:  Tests for Lamport signature class
  Created:  24/04/2017
"""

import lamport
import unittest
import hashlib
from os import urandom

class lamport_signature_test(unittest.TestCase):

    """Tests the lamport signature methods"""

    def setUp(self):
        self.ls = lamport.LamportSignature()

    def test_generate_private_key(self):
        """Tests generate_private_key"""
        self.assertEqual(len(self.ls.private_key),256)   #On vérifie qu'il y a bien 256 paires de groupes de 265 bits
        self.assertEqual(type(self.ls.private_key[0][0]),bytearray)
        self.assertEqual(len(self.ls.private_key[127][1]),32)   #On vérifie qu'un élément pris au hasard fait bien 32 octets i.e. 256 bits

    def test_generate_public_key(self):
        """Test generate_public_key"""
        noDifference = True
        for i,tuple in enumerate(self.ls.private_key):
            noDifference = noDifference and ((self.ls.hash(tuple[0]),self.ls.hash(tuple[1])) == self.ls.public_key[i])
        self.assertTrue(noDifference)

    def test_concatenate_key(self):
        """Tests concatenate_key"""
        key = [(bytearray(urandom(32)), bytearray(urandom(32))) for i in range(256)]
        ret = bytearray(0)
        for a,b in key:
            ret += a + b
        self.assertEqual(ret,self.ls.concatenate_key(key))

    def test_decatenate_key(self):
        """Tests decatenate_key"""
        self.assertEqual(self.ls.decatenate_key(self.ls.concatenate_key(self.ls.private_key)),self.ls.private_key)
        self.assertEqual(self.ls.decatenate_key(self.ls.concatenate_key(self.ls.public_key)),self.ls.public_key)

    def test_get_key(self):
        """Tests get_key"""
        puK = self.ls.get_key('public',False)
        puKC = self.ls.get_key('public',True)
        prK = self.ls.get_key('private', False)
        prKC = self.ls.get_key('private', True)
        self.assertEqual(puK, self.ls.public_key)
        self.assertEqual(puKC, self.ls.concatenate_key(self.ls.public_key))
        self.assertEqual(prK, self.ls.private_key)
        self.assertEqual(prKC, self.ls.concatenate_key(self.ls.private_key))

    def test_verify(self):
        """Tests verify"""
        msg = 'Ceci est un message test'
        msg2 = 'Ceci est un autre message test'
        signature = self.ls.sign(msg)
        signature2 = self.ls.sign(msg2)
        self.assertTrue(self.ls.verify(msg,signature,self.ls.public_key))
        self.assertFalse(self.ls.verify(msg,signature2,self.ls.public_key))


















