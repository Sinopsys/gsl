import lyra2re2_hash
import weakref
import binascii
import StringIO
import hashlib
import struct

from binascii import unhexlify, hexlify
from struct import *

def reverse(text):
    a = ""
    for i in range(1, len(text) + 1):
        a += text[len(text) - i]
    return a

def swap_order(hex_word):
    harr = list(reverse(hex_word));
    x="";

    for i in xrange(0,len(harr),2):
        x += (harr[i+1] + harr[i]);

    return x;

def little_endian(value):
    return hexlify(pack("L", value))[0:8];

# STRAKS BLOCK 10
header_hex = ( little_endian(536870912) + 
 swap_order("00000491760a7e6cf8fb72ef96626eae4b10242b2999c629336175252582e33a") +
 swap_order("15b4d0b16c968c98a7f61ac344925398a7a1466620271e0abd28e823d547c9f6") +
 little_endian(1510792864) +
 little_endian(504122572) +
 little_endian(53233) )

print "header_hex:", header_hex;

header_bin = unhexlify(header_hex)
hash_bin = lyra2re2_hash.getPoWHash(header_bin)

unswapped_hhash = hexlify(hash_bin)
header_hash = swap_order(hexlify(hash_bin))

print unswapped_hhash
print header_hash

print ">> matches target hash:", header_hash == "0000025f19e1714fd575bfe9e18e137625e731036da615f416d79f7edbdc1e81";
