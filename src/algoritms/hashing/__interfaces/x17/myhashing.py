import x17_hash
from binascii import hexlify

name = 'x17'
bit = '512'

class myhashing:
    def __init__(self):
        self.hasher = x17_hash

    def update(self, s):
        self.string = s

    def hexdigest(self):
        return hexlify(self.hasher.x17_gethash(self.string)).decode()

