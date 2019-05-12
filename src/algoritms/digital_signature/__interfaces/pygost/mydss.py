import base64
from binascii import hexlify, unhexlify
from pygost.gost3410 import CURVE_PARAMS
from pygost.gost3410 import GOST3410Curve
from pygost.gost3410 import bytes2long
curve = GOST3410Curve(*CURVE_PARAMS['GostR3410_2012_TC26_ParamSetA'])
from os import urandom
# prv_raw = urandom(32)
from pygost.gost3410 import prv_unmarshal
# prv = prv_unmarshal(prv_raw)
from pygost.gost3410 import public_key
# pub = public_key(curve, prv)
from pygost.gost3410 import pub_marshal
from pygost.utils import hexenc
from pygost.utils import hexdec
# print('Public key is:', hexenc(pub_marshal(pub)))
from pygost import gost34112012256
# data_for_signing = b'some data'
# dgst = gost34112012256.new(data_for_signing).digest()
from pygost.gost3410 import sign
# signature = sign(curve, prv, dgst, mode=2012)
from pygost.gost3410 import verify
# verify(curve, pub, dgst, signature, mode=2012)

name = 'gost'
bit = '256'

class sk_:
    def __init__(self, prv, pub=0000):
        self.prv = prv
        self.pub = pub

    def to_string(self, pub=False):
        if pub:
            return hexenc(pub_marshal(self.pub))
        return self.prv

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
        prv_raw = urandom(32)
        prv = prv_unmarshal(prv_raw)
        pub = public_key(curve, prv)
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
