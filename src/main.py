#!/usr/bin/env python
# coding:utf-8
"""
  Purpose:  Main file.
  Created:  19/04/2017
"""

from lamport import LamportSignature
from merkle_tree import MerkleTree
from sys import getsizeof


def main():
    N = 4  # Limited number of messages

    # Generate 'N' private/public key pairs (Xi, Yi) from the Lamport signature scheme
    key_pairs = [LamportSignature() for _ in range(N)]  # Private key of the Merkle signature scheme

    # The leaves of the tree are the hashed values of the public keys Y0, ..., YN
    mk = MerkleTree(n_leaves=N)
    for i in range(N):
        mk.add_node(key_pairs[i].get_key('public', concatenate=True), (0, i), hashed=False)

    # Build Merkle tree
    mk.generate_tree()
    pub = mk.get_root()  # Public key of the Merkle signature scheme

    # Merkle signature generation using a chosen pair of keys (Xi, Yi) from the Lamport signature scheme
    # sig = concatenate(sig_prime, Yi, auth(0), ..., auth(n-1))
    # see https://en.wikipedia.org/wiki/Merkle_signature_scheme
    pair = 0  # (Xi, Yi) pair number
    sig = []
    M = "test"
    sig_prime = key_pairs[pair].sign(M)
    sig.append(sig_prime)  # Add sig_prime to the signature 'sig'.
    sig.append(key_pairs[pair].get_key('public', concatenate=True))  # Add Yi to the signature 'sig'.
    sig.append(mk.get_authentification_path_hashes(pair))  # Add auth(0), ..., auth(n-1) to the signature 'sig'.

    ######################################################################
    # Merkle signature verification.
    # Receiver knows the public key 'pub' (tree root), the message 'M' and the Merkle signature 'sig'.
    pub_receiver = pub
    M_receiver = M
    sig_receiver = sig

    # First, the receiver verifies the one time signature 'sig_prime' of the message 'M' using the Lamport key 'Yi'.
    print("Check one time signature of the received message: " + M_receiver)
    result = LamportSignature.verify(M_receiver, sig_receiver[0], LamportSignature.decatenate_key(sig_receiver[1]))
    print("One-time signature is: " + str(result))

    # If 'sig_prime' is a valid signature of 'M', the receiver computes the leaf corresponding to the Lamport key 'Yi'.
    if result:
        mk_receiver = MerkleTree(n_leaves=N)
        mk_receiver.add_node(sig_receiver[1], (0, pair), hashed=False)
        mk_receiver.generate_tree()

        # The nodes of the authentification path are computed.
        for i, (level, index) in enumerate(mk_receiver.get_authentification_path(pair)):
            mk_receiver.add_node(sig_receiver[2][i], (level, index), hashed=True)
        mk_receiver.generate_tree()

        # If the tree's root equals the public key 'pub' the signature is valid.
        result = mk_receiver.get_root() == pub_receiver
        print("Merkle signature is: " + str(result))


if __name__ == "__main__":
    main()
