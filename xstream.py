#!/usr/bin/python

import cffi
import xstreamlib

# NOTE: SINGLE THREAD ONLY
_hash = cffi.FFI().new('unsigned char [16]')

def xcsum (v):
    assert isinstance(v, (bytes, bytearray, memoryview))
    # TODO:
    if not isinstance(v, (bytes, bytearray)):
        v = bytes(v)
    h = xstreamlib.lib.xcsum(v, len(v))
    # print('0x%016X' % h)
    return h

def xhash_128 (v):
    assert isinstance(v, (bytes, bytearray, memoryview))
    xstreamlib.lib.xhash(v, len(v), _hash)
    h = int.from_bytes(_hash, byteorder='big', signed=False)
    # print('0x%016X' % h)
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

# assert 0x15D97A12A01C053C == xcsum(b'')
# assert 0x10FF00E0A93EA69C == xcsum(b'\x00\x00\x00\x00\x00\x00\x00\x00')
# assert 0x35F79E3F6348EF66 == xcsum(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
# assert 0xDB1F826D4F2C5B26 == xcsum(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
# assert 0x6CFB27A2E259339C == xcsum(b'D}R\xe2\x17\x8c\x04\n\xf6\xd0{o\xc9m\\\x81\x93G\xbd\xdbO\x14\x8b\x96\xcc\x8b\x10\xda\xf0D\xa3b\xbeu=\x92\x1d')

assert 0x0000000000000000 == xhash_64(b'')
assert 0x5AD86EC2619357F8 == xhash_64(b'\x00\x00\x00\x00\x00\x00\x00\x00')
assert 0x3DE17336B02F2A90 == xhash_64(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
assert 0xD5C1DD9F49C7FF92 == xhash_64(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
assert 0x62944B4BF25B5628 == xhash_64(b'\x01\x02\x03\x04\x05\x06\x07\x08')
assert 0x3244F49E8D9C5D4E == xhash_64(b'D}R\xe2\x17\x8c\x04\n\xf6\xd0{o\xc9m\\\x81\x93G\xbd\xdbO\x14\x8b\x96\xcc\x8b\x10\xda\xf0D\xa3b\xbeu=\x92\x1d')
assert 0x70B74A30B04B90F9 == xhash_64(b'D}R\xe2\x17\x8c\x04\n\xf6\xd0{o\xc9m\\\x81\x93G\xbd\xdbO\x14\x8b\x96\xcc\x8b\x10\xda')

assert 0x00000000000000000000000000000000 == xhash_128(b'')
assert 0x5AD86EC2619357F8EAC4B2BEA15BEF70 == xhash_128(b'\x00\x00\x00\x00\x00\x00\x00\x00')
assert 0x3DE17336B02F2A9033858157D64D36C0 == xhash_128(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
assert 0xD5C1DD9F49C7FF928BBE1F10A8C548B7 == xhash_128(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
assert 0x62944B4BF25B56283C673E4F8B0FAB50 == xhash_128(b'\x01\x02\x03\x04\x05\x06\x07\x08')
assert 0x3244F49E8D9C5D4E80350551364AA8FD == xhash_128(b'D}R\xe2\x17\x8c\x04\n\xf6\xd0{o\xc9m\\\x81\x93G\xbd\xdbO\x14\x8b\x96\xcc\x8b\x10\xda\xf0D\xa3b\xbeu=\x92\x1d')
assert 0x70B74A30B04B90F96C837DCCC5A2A3B9 == xhash_128(b'D}R\xe2\x17\x8c\x04\n\xf6\xd0{o\xc9m\\\x81\x93G\xbd\xdbO\x14\x8b\x96\xcc\x8b\x10\xda')
