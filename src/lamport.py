#!/usr/bin/env python
# coding:utf-8
"""
  Purpose:  Lamport One-Time Signature Scheme (LOTSS) implementation.
  Created:  20/04/2017
"""

from bitstring import BitArray
import hashlib
from os import urandom


class LamportSignature:
    """Lamport signature class.
    
    Attributes:
        private_key (list): Private key.
        public_key (list): Public key.
        
    """

    def __init__(self):
        """Constructor for LamportSignature."""
        self.private_key = self.generate_private_key()
        self.public_key = self.generate_public_key()

    @staticmethod
    def generate_private_key():
        """Generate a private key.
        
        Returns:
            (list): Private key, 2×256×256 bits = 16 KiB.

        """
        return [(urandom(32), urandom(32)) for i in range(256)]

    def generate_public_key(self):
        """Generate a public key.
        
        Returns:
            (list): Public key, 2×256×256 bits = 16 KiB.
        
        """
        return [(self.hash(a), self.hash(b)) for (a, b) in self.private_key]

    def sign(self, msg):
        """Sign a message with the Lamport signature.
        
        Args:
            msg (str): Message to sign.
        
        Returns:
            (list): Signature of the message, sequence of 256 random numbers, 256×256 bits.
        
        """
        msg_hash = self.hash(msg)
        signature = []
        for (a, b), bit in zip(self.private_key, BitArray(bytes=msg_hash).bin):
            if bit == "0":
                signature.append(a)
            elif bit == "1":
                signature.append(b)
        return signature

    @classmethod
    def verify(cls, msg, signature, public_key):
        """Verify signature of the message.
        
        Args:
            msg (str): Message to check.
            signature (list): Signature of the message, sequence of 256 random numbers, 256×256 bits.
            public_key (list): Public key, 2×256×256 bits.
        
        Returns:
            (boolean): True if signature of the message is right otherwise False.
        
        """
        msg_hash = cls.hash(msg)
        signature_hash = [cls.hash(i) for i in signature]
        for sig_hash, (a, b), bit in zip(signature_hash, public_key, BitArray(bytes=msg_hash).bin):
            if (bit == "0" and sig_hash != a) or (bit == "1" and sig_hash != b):
                return False
        return True

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
    for msg_sent, msg_to_check in (("abc", "abc"), ("abc", "aaa"), ("abc", "abc")):
        lamport = LamportSignature()
        signature = lamport.sign(msg_sent)
        print(msg_sent, msg_to_check, lamport.verify(msg_to_check, signature, lamport.public_key))


if __name__ == "__main__":
    main()
