from Crypto.Hash import BLAKE2s
from binascii import hexlify

name = 'blake2s'
bit = '256'

class myhashing:
    def __init__(self):
        self.hasher = BLAKE2s.new(digest_bits=256)

    def update(self, s):
        self.hasher.update(s)

    def hexdigest(self):
        return self.hasher.hexdigest()

