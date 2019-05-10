import x11_hash
from binascii import hexlify


class myhashing:
    def __init__(self):
        self.hasher = x11_hash

    def update(self, s):
        self.string = s

    def hexdigest(self):
        return hexlify(self.hasher.getPoWHash(self.string)).decode()

