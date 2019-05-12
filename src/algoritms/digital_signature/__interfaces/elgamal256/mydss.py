import base64
from binascii import hexlify, unhexlify
from elgamal import elgamal

name = 'elgamal'


class sk_:
    def __init__(self, prv, pub=0000):
        self.prv = prv
        self.pub = pub

    def to_string(self, pub=False):
        if pub:
            return (str(self.pub.p) + str(self.pub.g) + str(self.pub.h) + str(256)).encode()
        return str(self.prv.p) + str(self.prv.g) + str(self.prv.x) + str(256)

    def get_verifying_key(self):
        return self.pub

    def sign(self, bmsg):
        dgst = gost34112012256.new(bmsg).digest()
        signature = sign(curve, int(self.prv), dgst, mode=2012)
        return signature


class vk_:
    def __init__(self, pub):
        self.pub = pub

    def verify(self, signature, b_msg):
        self.dgst = gost34112012256.new(b_msg).digest()
        return verify(curve, self.pub, self.dgst, signature, mode=2012)


class SigningKey:
    def __init__(self):
        pass

    def generate(self):
        keys = elgamal.generate_keys()
        pub = keys['publicKey']
        prv = keys['privateKey']
        return sk_(prv, pub)

    def from_string(self, prv):
        return sk_(prv)


class VerifyingKey:
    def __init__(self):
        pass

    def hex_to_pub(self, hex_pub):
        hex_pub = hexdec(hex_pub)[::-1]
        l = len(hex_pub) // 2
        first = bytes2long(hex_pub[l:])
        second = bytes2long(hex_pub[:l])
        return first, second

    def from_string(self, b_pub):
        pub = hexlify(b_pub)
        pub = self.hex_to_pub(pub)
        return vk_(pub)
