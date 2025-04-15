#!/usr/bin/python

import cffi
import xstreamlib

# NOTE: SINGLE THREAD ONLY
_hash = cffi.FFI().new('unsigned char [72]')
_csum = cffi.FFI().new('unsigned char [64]')

def xhash_128 (v):
    assert isinstance(v, (bytes, bytearray, memoryview))
    xstreamlib.lib.xhash(v, len(v), _hash)
    h = int.from_bytes(_hash[0:16], byteorder='big', signed=False)
    # print('0x%032X' % h)
    return h

def xhash_64 (v):
    assert isinstance(v, (bytes, bytearray, memoryview))
    xstreamlib.lib.xhash(v, len(v), _hash)
    h = int.from_bytes(_hash[0:8], byteorder='big', signed=False)
    # print('0x%016X' % h)
    return h

def xhash (v):
    assert isinstance(v, (bytes, bytearray, memoryview))
    xstreamlib.lib.xhash(v, len(v), _hash)
    return _hash

def xcsum (v):
    assert isinstance(v, (bytes, bytearray, memoryview))
    xstreamlib.lib.xcsum(v, len(v), _csum)
    return _csum

'''
assert 0x15D97A12A01C053C == xcsum(b'')
assert 0x10FF00E0A93EA69C == xcsum(b'\x00\x00\x00\x00\x00\x00\x00\x00')
assert 0x35F79E3F6348EF66 == xcsum(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
assert 0xDB1F826D4F2C5B26 == xcsum(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
assert 0x26068EE82D34D887 == xcsum(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01')
assert 0xFAE5691686A0BE18 == xcsum(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02')
assert 0x598A8021ED992046 == xcsum(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x20')
assert 0x3F7B077BCA41D410 == xcsum(b'D}R\xe2\x17\x8c\x04\n\xf6\xd0{o\xc9m\\\x81\x93G\xbd\xdbO\x14\x8b\x96\xcc\x8b\x10\xda\xf0D\xa3b\xbeu=\x92\x1d')
assert 0x8D3225C6A6084010 == xcsum(b'D}R\xe2\x17\x8c\x05\n\xf6\xd0{o\xc9m\\\x81\x93G\xbd\xdbO\x14\x8b\x96\xcc\x8b\x10\xda\xf0D\xa3b\xbeu=\x92\x1d')


assert 0x0000000000000000 == xhash_64(b'')
assert 0x584389899B3C4ED6 == xhash_64(b'\x00\x00\x00\x00\x00\x00\x00\x00')
assert 0xB8D53E268E69A1FB == xhash_64(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
assert 0x17DF3CAFB7C52517 == xhash_64(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
assert 0x8F53D6CA5A1D1F24 == xhash_64(b'\x01\x02\x03\x04\x05\x06\x07\x08')
assert 0x4772487DF3A4EFC8 == xhash_64(b'\x01\x02\x03\x04\x05\x06\x07\x07')
assert 0xC77E35C4B030FB30 == xhash_64(b'\x01\x02\x03\x05\x05\x06\x07\x08')
assert 0x41194B939CB1858C == xhash_64(b'\x01\x02\x03\x04\x05\x06\x07\x09')
assert 0x6FA38BCD3F51068C == xhash_64(b'D}R\xe2\x17\x8c\x04\n\xf6\xd0{o\xc9m\\\x81\x93G\xbd\xdbO\x14\x8b\x96\xcc\x8b\x10\xda\xf0D\xa3b\xbeu=\x92\x1d')
assert 0x000A745A73F782E7 == xhash_64(b'D}R\xe2\x17\x8c\x04\n\xf6\xd0{o\xc9m\\\x81\x93G\xbd\xdbO\x14\x8b\x96\xcc\x8b\x10\xda')

assert 0x00000000000000000000000000000000 == xhash_128(b'')
assert 0x584389899B3C4ED67DC1F60002A2DF51 == xhash_128(b'\x00\x00\x00\x00\x00\x00\x00\x00')
assert 0xB8D53E268E69A1FB409784903F3BC909 == xhash_128(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
assert 0x17DF3CAFB7C52517A29E3ED631E1CEAC == xhash_128(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
assert 0x8F53D6CA5A1D1F24FF0FDF4D86AA24CE == xhash_128(b'\x01\x02\x03\x04\x05\x06\x07\x08')
assert 0x4772487DF3A4EFC8019E85F60CBB4AA3 == xhash_128(b'\x01\x02\x03\x04\x05\x06\x07\x07')
assert 0xC77E35C4B030FB309E9962C9FC55F026 == xhash_128(b'\x01\x02\x03\x05\x05\x06\x07\x08')
assert 0x41194B939CB1858CE43C04CEDEFC9E7A == xhash_128(b'\x01\x02\x03\x04\x05\x06\x07\x09')
assert 0x6FA38BCD3F51068C1B30FCD6FC41EEBD == xhash_128(b'D}R\xe2\x17\x8c\x04\n\xf6\xd0{o\xc9m\\\x81\x93G\xbd\xdbO\x14\x8b\x96\xcc\x8b\x10\xda\xf0D\xa3b\xbeu=\x92\x1d')
assert 0x000A745A73F782E747D4C6FD701A868A == xhash_128(b'D}R\xe2\x17\x8c\x04\n\xf6\xd0{o\xc9m\\\x81\x93G\xbd\xdbO\x14\x8b\x96\xcc\x8b\x10\xda')
'''
