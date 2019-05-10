import lyra2re2_hash
from binascii import hexlify


class myhashing:
    def __init__(self):
        self.hasher = lyra2re2_hash

    def update(self, s):
        self.string = s
        self.res = hexlify(self.hasher.getPoWHash(self.string))

    def hexdigest(self):
        return self.res.decode()

