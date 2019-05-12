import ethash
from binascii import hexlify

name = 'ethash'
bit = '256'

class myhashing:
    def __init__(self):
        self.hasher = ethash.keccak256

    def update(self, s):
        self.string = s

    def hexdigest(self):
        return hexlify(self.hasher(self.string)).decode()

