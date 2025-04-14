#!/usr/bin/python

import cffi
import xstreamlib

# NOTE: SINGLE THREAD ONLY
_hash = cffi.FFI().new('unsigned char [16]')

def xcsum (v, cur=0):
    assert isinstance(cur, int) and 0 <= cur <= 0xFFFFFFFFFFFFFFFF
    assert isinstance(v, (bytes, bytearray, memoryview))
    # TODO:
    if not isinstance(v, (bytes, bytearray)):
        v = bytes(v)
    return xstreamlib.lib.xcsum(v, len(v), cur)

NATIVE = 'little'

def xhash_128 (v):
    assert isinstance(v, (bytes, bytearray, memoryview))
    xstreamlib.lib.xhash(v, len(v), _hash)
    return int.from_bytes(_hash, byteorder=NATIVE, signed=False)


assert 0x0000000000000000 == xcsum(b'')
assert 0x1234567890ABCDEF == xcsum(b'', 0x1234567890ABCDEF)
assert 0xF347B88EFF315942 == xcsum(b'\x00\x00\x00\x00\x00\x00\x00\x00')
assert 0xE04CDD083E035B60 == xcsum(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
assert 0xBF69CF2D5121B0EC == xcsum(b'D}R\xe2\x17\x8c\x04\n\xf6\xd0{o\xc9m\\\x81\x93G\xbd\xdbO\x14\x8b\x96\xcc\x8b\x10\xda\xf0D\xa3b\xbeu=\x92\x1d')
assert 0x13F01810B02A4063 == xcsum(b'D}R\xe2\x17\x8c\x04\n\xf6\xd0{o\xc9m\\\x81\x93G\xbd\xdbO\x14\x8b\x96\xcc\x8b\x10\xda\xf0D\xa3b\xbeu=\x92\x1d', 0x1234567890ABCDEF)


#
assert 0x27C1D6EEF37B86491327F4C4C8DE7A92 == xhash_128(b'')
assert 0x299A36812BB883BBB39BB9E9D019AD2E == xhash_128(b'\x00\x00\x00\x00\x00\x00\x00\x00')
assert 0xE147695578D294812F1D42BCFFC611C2 == xhash_128(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
assert 0x6B952202453C5FF04F950FD098B5FEC0 == xhash_128(b'\x01\x02\x03\x04\x05\x06\x07\x08')
assert 0x0F407F628B003535871FF7D9684F5EB6 == xhash_128(b'D}R\xe2\x17\x8c\x04\n\xf6\xd0{o\xc9m\\\x81\x93G\xbd\xdbO\x14\x8b\x96\xcc\x8b\x10\xda\xf0D\xa3b\xbeu=\x92\x1d')
assert 0x2ADD9B3A27B3648C81D6F4A9DE0B7D68 == xhash_128(b'D}R\xe2\x17\x8c\x04\n\xf6\xd0{o\xc9m\\\x81\x93G\xbd\xdbO\x14\x8b\x96\xcc\x8b\x10\xda')


# print('0x%032X' % )

'''
assert 0x3DE7 == xhash16(b'abcdefghijklmnopqrstuvwxyz')
assert 0xE31C == xhash16(b'abcdefghijklmnopqrstuvwxyz0123456789')
assert 0x9D22 == xhash16(b'ABCDEFGHIJKLMNOPQRSTUVWXYZ')
assert 0x9DB6 == xhash16(b'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')

assert 0x5FED == xhash16(b'ABACATE')
assert 0x2367 == xhash16(b'CENOURA')
assert 0xF097 == xhash16(b'ALFACE')
assert 0xB06A == xhash16(b'BETERRABA')

assert 0x3E85D1C3472194DF == xhash64(b'abcdefghijklmnopqrstuvwxyz')
assert 0xB0EC7AA97BA92D41 == xhash64(b'abcdefghijklmnopqrstuvwxyz0123456789')
assert 0xDDA0F4C5129778F5 == xhash64(b'ABCDEFGHIJKLMNOPQRSTUVWXYZ')
assert 0x709A1D95A190F463 == xhash64(b'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')

assert 0xFA24DA0E912BDDDF == xhash64(b'ABACATE')
assert 0x1FDB8771F28B27A4 == xhash64(b'CENOURA')
assert 0x3CB6217C29A913E0 == xhash64(b'ALFACE')
assert 0x93192927FC38A76C == xhash64(b'BETERRABA')
'''
