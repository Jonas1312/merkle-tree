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
        used (boolean): Keys already used to sign a message.
        
    """

    def __init__(self):
        """ LamportSignature object constructor"""
        self.private_key = self.generate_private_key()
        self.public_key = self.generate_public_key()
        self.used = False

    @staticmethod
    def generate_private_key():
        """Generate a private key.
        
        Returns:
            (list): Private key, 2×256×256 bits = 16 KiB.

        """
        return [(bytearray(urandom(32)), bytearray(urandom(32))) for i in range(256)]

    def generate_public_key(self):
        """Generate a public key.
        
        Returns:
            (list): Public key, 2×256×256 bits = 16 KiB.
        
        """
        return [(self.hash(a), self.hash(b)) for (a, b) in self.private_key]

    @staticmethod
    def concatenate_key(key_list):
        """Concatenate key.
        
        Args:
            key_list (list): Key to concatenate.
        
        Returns:
            (bytearray): Concatenated key.
        
        """
        ret = bytearray(0)
        if type(key_list[0]) is tuple:
            for a, b in key_list:
                ret += a + b
        else:
            for i in key_list:
                ret += i
        return ret

    @staticmethod
    def decatenate_key(key):
        """Decatenate key.
        
        Args:
            key (bytearray): Key to decatenate.
        
        Returns:
            (list): Decatenated key.
            
        """
        if len(key) == 8192:  # signature key size 256×256 bits
            return [key[i:i + 32] for i in range(0, 8192, 32)]
        elif len(key) == 16384:  # public/private key size 2x256×256 bits
            ret = []
            for i in range(0, 16384, 64):
                ret.append((key[i:i + 32], key[i + 32:i + 64]))
            return ret
        else:
            raise ValueError("Wrong key size.")

    def get_key(self, key_type, concatenate):
        """Getter for the public or private key.
        
        Args:
            key_type (str): 'public' or 'private'.
            concatenate (boolean): Concatenate key or not.
        
        Returns:
            (bytearray/list): Public key.
        
        """
        key = self.public_key if key_type == 'public' else self.private_key
        if not concatenate:
            return key
        return self.concatenate_key(key)

    def sign(self, msg):
        """Sign a message with the Lamport signature.
        
        Args:
            msg (str): Message to sign.
        
        Returns:
            (list): Signature of the message, sequence of 256 random numbers, 256×256 bits.
        
        """
        if self.used:
            raise ValueError("Private and public keys already used!")
        self.used = True
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
        
        Args:
            (str/bytearray): Data to hash.

        Returns:
            (bytearray): bytes of the hash.

        """
        if type(data) is not bytearray:
            data = data.encode('utf-8')
        return bytearray(hashlib.sha256(data).digest())


def main():
    for msg_sent, msg_to_check in (("abc", "abc"), ("abc", "aaa"), ("abc", "aabc")):
        lamport = LamportSignature()
        signature = lamport.sign(msg_sent)
        print(msg_sent, msg_to_check, LamportSignature.verify(msg_to_check, signature, lamport.public_key))


if __name__ == "__main__":
    main()
