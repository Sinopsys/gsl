from pyscrypt import hash
from binascii import hexlify
from uuid import uuid4

name = 'scrypt'
bit = '256'

class myhashing:
    def __init__(self):
        self.hasher = hash

    def update(self, s):
        self.string = s
        self.random_str = str(uuid4())

    def hexdigest(self):
        return hexlify(hash(self.string, self.random_str.encode('utf-8'), 16, 16, 16, 16)).decode()

