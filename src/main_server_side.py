#!/usr/bin/env python
# coding:utf-8
"""
  Purpose:  Main server side file.
  Created:  27/04/2017
  Note:     Run this file before running 'main_client_side.py'.
"""

import pickle
from socket_client_server import Server
from lamport import LamportSignature
from merkle_tree import MerkleTree


def main():
    # Merkle signature verification.
    server = Server()
    data = server.receive()
    server.close()
    data = pickle.loads(data)

    # Receiver knows the public key 'pub' (tree root), the message 'M' and the Merkle signature 'sig'.
    N, pair, pub_receiver, M_receiver, sig_receiver = data

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
