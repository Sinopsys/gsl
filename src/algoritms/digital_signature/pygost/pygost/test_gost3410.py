# coding: utf-8
# PyGOST -- Pure Python GOST cryptographic functions library
# Copyright (C) 2015-2018 Sergey Matveev <stargrave@stargrave.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from os import urandom
from unittest import TestCase

from pygost.gost3410 import CURVE_PARAMS
from pygost.gost3410 import GOST3410Curve
from pygost.gost3410 import public_key
from pygost.gost3410 import sign
from pygost.gost3410 import verify
from pygost.utils import bytes2long
from pygost.utils import long2bytes


class Test341001(TestCase):
    def test_rfc(self):
        """ Test vector from :rfc:`5832`
        """
        prv = bytes(bytearray((
            0x7A, 0x92, 0x9A, 0xDE, 0x78, 0x9B, 0xB9, 0xBE,
            0x10, 0xED, 0x35, 0x9D, 0xD3, 0x9A, 0x72, 0xC1,
            0x1B, 0x60, 0x96, 0x1F, 0x49, 0x39, 0x7E, 0xEE,
            0x1D, 0x19, 0xCE, 0x98, 0x91, 0xEC, 0x3B, 0x28
        )))
        pub_x = bytes(bytearray((
            0x7F, 0x2B, 0x49, 0xE2, 0x70, 0xDB, 0x6D, 0x90,
            0xD8, 0x59, 0x5B, 0xEC, 0x45, 0x8B, 0x50, 0xC5,
            0x85, 0x85, 0xBA, 0x1D, 0x4E, 0x9B, 0x78, 0x8F,
            0x66, 0x89, 0xDB, 0xD8, 0xE5, 0x6F, 0xD8, 0x0B
        )))
        pub_y = bytes(bytearray((
            0x26, 0xF1, 0xB4, 0x89, 0xD6, 0x70, 0x1D, 0xD1,
            0x85, 0xC8, 0x41, 0x3A, 0x97, 0x7B, 0x3C, 0xBB,
            0xAF, 0x64, 0xD1, 0xC5, 0x93, 0xD2, 0x66, 0x27,
            0xDF, 0xFB, 0x10, 0x1A, 0x87, 0xFF, 0x77, 0xDA
        )))
        digest = bytes(bytearray((
            0x2D, 0xFB, 0xC1, 0xB3, 0x72, 0xD8, 0x9A, 0x11,
            0x88, 0xC0, 0x9C, 0x52, 0xE0, 0xEE, 0xC6, 0x1F,
            0xCE, 0x52, 0x03, 0x2A, 0xB1, 0x02, 0x2E, 0x8E,
            0x67, 0xEC, 0xE6, 0x67, 0x2B, 0x04, 0x3E, 0xE5
        )))
        signature = bytes(bytearray((
            0x41, 0xAA, 0x28, 0xD2, 0xF1, 0xAB, 0x14, 0x82,
            0x80, 0xCD, 0x9E, 0xD5, 0x6F, 0xED, 0xA4, 0x19,
            0x74, 0x05, 0x35, 0x54, 0xA4, 0x27, 0x67, 0xB8,
            0x3A, 0xD0, 0x43, 0xFD, 0x39, 0xDC, 0x04, 0x93,
            0x01, 0x45, 0x6C, 0x64, 0xBA, 0x46, 0x42, 0xA1,
            0x65, 0x3C, 0x23, 0x5A, 0x98, 0xA6, 0x02, 0x49,
            0xBC, 0xD6, 0xD3, 0xF7, 0x46, 0xB6, 0x31, 0xDF,
            0x92, 0x80, 0x14, 0xF6, 0xC5, 0xBF, 0x9C, 0x40
        )))
        prv = bytes2long(prv)
        signature = signature[32:] + signature[:32]

        c = GOST3410Curve(*CURVE_PARAMS["GostR3410_2001_TestParamSet"])
        pubX, pubY = public_key(c, prv)
        self.assertEqual(long2bytes(pubX), pub_x)
        self.assertEqual(long2bytes(pubY), pub_y)
        s = sign(c, prv, digest)
        self.assertTrue(verify(c, (pubX, pubY), digest, s))
        self.assertTrue(verify(c, (pubX, pubY), digest, signature))

    def test_sequence(self):
        c = GOST3410Curve(*CURVE_PARAMS["GostR3410_2001_TestParamSet"])
        prv = bytes2long(urandom(32))
        pubX, pubY = public_key(c, prv)
        for _ in range(20):
            digest = urandom(32)
            s = sign(c, prv, digest, mode=2001)
            self.assertTrue(verify(c, (pubX, pubY), digest, s, mode=2001))


class Test34102012(TestCase):
    def test_gcl3(self):
        """ Test vector from libgcl3
        """
        p = bytes(bytearray((
            0x45, 0x31, 0xAC, 0xD1, 0xFE, 0x00, 0x23, 0xC7,
            0x55, 0x0D, 0x26, 0x7B, 0x6B, 0x2F, 0xEE, 0x80,
            0x92, 0x2B, 0x14, 0xB2, 0xFF, 0xB9, 0x0F, 0x04,
            0xD4, 0xEB, 0x7C, 0x09, 0xB5, 0xD2, 0xD1, 0x5D,
            0xF1, 0xD8, 0x52, 0x74, 0x1A, 0xF4, 0x70, 0x4A,
            0x04, 0x58, 0x04, 0x7E, 0x80, 0xE4, 0x54, 0x6D,
            0x35, 0xB8, 0x33, 0x6F, 0xAC, 0x22, 0x4D, 0xD8,
            0x16, 0x64, 0xBB, 0xF5, 0x28, 0xBE, 0x63, 0x73
        )))
        q = bytes(bytearray((
            0x45, 0x31, 0xAC, 0xD1, 0xFE, 0x00, 0x23, 0xC7,
            0x55, 0x0D, 0x26, 0x7B, 0x6B, 0x2F, 0xEE, 0x80,
            0x92, 0x2B, 0x14, 0xB2, 0xFF, 0xB9, 0x0F, 0x04,
            0xD4, 0xEB, 0x7C, 0x09, 0xB5, 0xD2, 0xD1, 0x5D,
            0xA8, 0x2F, 0x2D, 0x7E, 0xCB, 0x1D, 0xBA, 0xC7,
            0x19, 0x90, 0x5C, 0x5E, 0xEC, 0xC4, 0x23, 0xF1,
            0xD8, 0x6E, 0x25, 0xED, 0xBE, 0x23, 0xC5, 0x95,
            0xD6, 0x44, 0xAA, 0xF1, 0x87, 0xE6, 0xE6, 0xDF
        )))
        a = bytes(bytearray((
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x07
        )))
        b = bytes(bytearray((
            0x1C, 0xFF, 0x08, 0x06, 0xA3, 0x11, 0x16, 0xDA,
            0x29, 0xD8, 0xCF, 0xA5, 0x4E, 0x57, 0xEB, 0x74,
            0x8B, 0xC5, 0xF3, 0x77, 0xE4, 0x94, 0x00, 0xFD,
            0xD7, 0x88, 0xB6, 0x49, 0xEC, 0xA1, 0xAC, 0x43,
            0x61, 0x83, 0x40, 0x13, 0xB2, 0xAD, 0x73, 0x22,
            0x48, 0x0A, 0x89, 0xCA, 0x58, 0xE0, 0xCF, 0x74,
            0xBC, 0x9E, 0x54, 0x0C, 0x2A, 0xDD, 0x68, 0x97,
            0xFA, 0xD0, 0xA3, 0x08, 0x4F, 0x30, 0x2A, 0xDC
        )))
        x = bytes(bytearray((
            0x24, 0xD1, 0x9C, 0xC6, 0x45, 0x72, 0xEE, 0x30,
            0xF3, 0x96, 0xBF, 0x6E, 0xBB, 0xFD, 0x7A, 0x6C,
            0x52, 0x13, 0xB3, 0xB3, 0xD7, 0x05, 0x7C, 0xC8,
            0x25, 0xF9, 0x10, 0x93, 0xA6, 0x8C, 0xD7, 0x62,
            0xFD, 0x60, 0x61, 0x12, 0x62, 0xCD, 0x83, 0x8D,
            0xC6, 0xB6, 0x0A, 0xA7, 0xEE, 0xE8, 0x04, 0xE2,
            0x8B, 0xC8, 0x49, 0x97, 0x7F, 0xAC, 0x33, 0xB4,
            0xB5, 0x30, 0xF1, 0xB1, 0x20, 0x24, 0x8A, 0x9A
        )))
        y = bytes(bytearray((
            0x2B, 0xB3, 0x12, 0xA4, 0x3B, 0xD2, 0xCE, 0x6E,
            0x0D, 0x02, 0x06, 0x13, 0xC8, 0x57, 0xAC, 0xDD,
            0xCF, 0xBF, 0x06, 0x1E, 0x91, 0xE5, 0xF2, 0xC3,
            0xF3, 0x24, 0x47, 0xC2, 0x59, 0xF3, 0x9B, 0x2C,
            0x83, 0xAB, 0x15, 0x6D, 0x77, 0xF1, 0x49, 0x6B,
            0xF7, 0xEB, 0x33, 0x51, 0xE1, 0xEE, 0x4E, 0x43,
            0xDC, 0x1A, 0x18, 0xB9, 0x1B, 0x24, 0x64, 0x0B,
            0x6D, 0xBB, 0x92, 0xCB, 0x1A, 0xDD, 0x37, 0x1E
        )))
        prv = bytes(bytearray((
            0x0B, 0xA6, 0x04, 0x8A, 0xAD, 0xAE, 0x24, 0x1B,
            0xA4, 0x09, 0x36, 0xD4, 0x77, 0x56, 0xD7, 0xC9,
            0x30, 0x91, 0xA0, 0xE8, 0x51, 0x46, 0x69, 0x70,
            0x0E, 0xE7, 0x50, 0x8E, 0x50, 0x8B, 0x10, 0x20,
            0x72, 0xE8, 0x12, 0x3B, 0x22, 0x00, 0xA0, 0x56,
            0x33, 0x22, 0xDA, 0xD2, 0x82, 0x7E, 0x27, 0x14,
            0xA2, 0x63, 0x6B, 0x7B, 0xFD, 0x18, 0xAA, 0xDF,
            0xC6, 0x29, 0x67, 0x82, 0x1F, 0xA1, 0x8D, 0xD4
        )))
        pub_x = bytes(bytearray((
            0x11, 0x5D, 0xC5, 0xBC, 0x96, 0x76, 0x0C, 0x7B,
            0x48, 0x59, 0x8D, 0x8A, 0xB9, 0xE7, 0x40, 0xD4,
            0xC4, 0xA8, 0x5A, 0x65, 0xBE, 0x33, 0xC1, 0x81,
            0x5B, 0x5C, 0x32, 0x0C, 0x85, 0x46, 0x21, 0xDD,
            0x5A, 0x51, 0x58, 0x56, 0xD1, 0x33, 0x14, 0xAF,
            0x69, 0xBC, 0x5B, 0x92, 0x4C, 0x8B, 0x4D, 0xDF,
            0xF7, 0x5C, 0x45, 0x41, 0x5C, 0x1D, 0x9D, 0xD9,
            0xDD, 0x33, 0x61, 0x2C, 0xD5, 0x30, 0xEF, 0xE1
        )))
        pub_y = bytes(bytearray((
            0x37, 0xC7, 0xC9, 0x0C, 0xD4, 0x0B, 0x0F, 0x56,
            0x21, 0xDC, 0x3A, 0xC1, 0xB7, 0x51, 0xCF, 0xA0,
            0xE2, 0x63, 0x4F, 0xA0, 0x50, 0x3B, 0x3D, 0x52,
            0x63, 0x9F, 0x5D, 0x7F, 0xB7, 0x2A, 0xFD, 0x61,
            0xEA, 0x19, 0x94, 0x41, 0xD9, 0x43, 0xFF, 0xE7,
            0xF0, 0xC7, 0x0A, 0x27, 0x59, 0xA3, 0xCD, 0xB8,
            0x4C, 0x11, 0x4E, 0x1F, 0x93, 0x39, 0xFD, 0xF2,
            0x7F, 0x35, 0xEC, 0xA9, 0x36, 0x77, 0xBE, 0xEC
        )))
        digest = bytes(bytearray((
            0x37, 0x54, 0xF3, 0xCF, 0xAC, 0xC9, 0xE0, 0x61,
            0x5C, 0x4F, 0x4A, 0x7C, 0x4D, 0x8D, 0xAB, 0x53,
            0x1B, 0x09, 0xB6, 0xF9, 0xC1, 0x70, 0xC5, 0x33,
            0xA7, 0x1D, 0x14, 0x70, 0x35, 0xB0, 0xC5, 0x91,
            0x71, 0x84, 0xEE, 0x53, 0x65, 0x93, 0xF4, 0x41,
            0x43, 0x39, 0x97, 0x6C, 0x64, 0x7C, 0x5D, 0x5A,
            0x40, 0x7A, 0xDE, 0xDB, 0x1D, 0x56, 0x0C, 0x4F,
            0xC6, 0x77, 0x7D, 0x29, 0x72, 0x07, 0x5B, 0x8C
        )))
        signature = bytes(bytearray((
            0x2F, 0x86, 0xFA, 0x60, 0xA0, 0x81, 0x09, 0x1A,
            0x23, 0xDD, 0x79, 0x5E, 0x1E, 0x3C, 0x68, 0x9E,
            0xE5, 0x12, 0xA3, 0xC8, 0x2E, 0xE0, 0xDC, 0xC2,
            0x64, 0x3C, 0x78, 0xEE, 0xA8, 0xFC, 0xAC, 0xD3,
            0x54, 0x92, 0x55, 0x84, 0x86, 0xB2, 0x0F, 0x1C,
            0x9E, 0xC1, 0x97, 0xC9, 0x06, 0x99, 0x85, 0x02,
            0x60, 0xC9, 0x3B, 0xCB, 0xCD, 0x9C, 0x5C, 0x33,
            0x17, 0xE1, 0x93, 0x44, 0xE1, 0x73, 0xAE, 0x36,
            0x10, 0x81, 0xB3, 0x94, 0x69, 0x6F, 0xFE, 0x8E,
            0x65, 0x85, 0xE7, 0xA9, 0x36, 0x2D, 0x26, 0xB6,
            0x32, 0x5F, 0x56, 0x77, 0x8A, 0xAD, 0xBC, 0x08,
            0x1C, 0x0B, 0xFB, 0xE9, 0x33, 0xD5, 0x2F, 0xF5,
            0x82, 0x3C, 0xE2, 0x88, 0xE8, 0xC4, 0xF3, 0x62,
            0x52, 0x60, 0x80, 0xDF, 0x7F, 0x70, 0xCE, 0x40,
            0x6A, 0x6E, 0xEB, 0x1F, 0x56, 0x91, 0x9C, 0xB9,
            0x2A, 0x98, 0x53, 0xBD, 0xE7, 0x3E, 0x5B, 0x4A
        )))
        prv = bytes2long(prv)
        signature = signature[64:] + signature[:64]

        c = GOST3410Curve(p, q, a, b, x, y)
        pubX, pubY = public_key(c, prv)
        self.assertEqual(long2bytes(pubX), pub_x)
        self.assertEqual(long2bytes(pubY), pub_y)
        s = sign(c, prv, digest, mode=2012)
        self.assertTrue(verify(c, (pubX, pubY), digest, s, mode=2012))
        self.assertTrue(verify(c, (pubX, pubY), digest, signature, mode=2012))

    def test_sequence(self):
        c = GOST3410Curve(*CURVE_PARAMS["GostR3410_2012_TC26_ParamSetA"])
        prv = bytes2long(urandom(64))
        pubX, pubY = public_key(c, prv)
        for _ in range(20):
            digest = urandom(64)
            s = sign(c, prv, digest, mode=2012)
            self.assertTrue(verify(c, (pubX, pubY), digest, s, mode=2012))
            self.assertNotIn(b"\x00" * 8, s)
