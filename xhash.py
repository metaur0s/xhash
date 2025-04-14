#!/usr/bin/python

import cffi
import xhashlib

# NOTE: SINGLE THREAD ONLY
_xhash_buff128 = cffi.FFI().new('unsigned char [16]')
_xhash_buff256 = cffi.FFI().new('unsigned char [32]')

def xhash16 (v):
    assert isinstance(v, (bytes, bytearray, memoryview))
    # TODO:
    if not isinstance(v, (bytes, bytearray)):
        v = bytes(v)
    return xhashlib.lib.xhash16(v, len(v))

def xhash64 (v):
    assert isinstance(v, (bytes, bytearray, memoryview))
    # TODO:
    if not isinstance(v, (bytes, bytearray)):
        v = bytes(v)
    return xhashlib.lib.xhash64(v, len(v))

def xhash128 (v):
    assert isinstance(v, (bytes, bytearray, memoryview))
    xhashlib.lib.xhash128(v, len(v), _xhash_buff128)
    return bytes(_xhash_buff128)

def xhash256 (v):
    assert isinstance(v, (bytes, bytearray, memoryview))
    xhashlib.lib.xhash256(v, len(v), _xhash_buff256)
    return bytes(_xhash_buff256)

assert xhash16(b'') == 0
assert xhash64(b'') == 0

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
