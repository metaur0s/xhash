#!/usr/bin/python

import cffi
import xhashlib

# NOTE: SINGLE THREAD ONLY
_xhash_buff128 = cffi.FFI().new('unsigned char [16]')
_xhash_buff256 = cffi.FFI().new('unsigned char [32]')

def xhash64 (v):
    assert isinstance(v, (bytes, bytearray, memoryview))
    return xhashlib.lib.xhash64(v, len(v))

def xhash128 (v):
    assert isinstance(v, (bytes, bytearray, memoryview))
    xhashlib.lib.xhash128(v, len(v), _xhash_buff128)
    return bytes(_xhash_buff128)

def xhash256 (v):
    assert isinstance(v, (bytes, bytearray, memoryview))
    xhashlib.lib.xhash256(v, len(v), _xhash_buff256)
    return bytes(_xhash_buff256)

assert xhash64(b'') == 0

assert 0xD360E6745FE9B7A8 == xhash64(b'ALFACE')
assert 0xD953E52AEA5FDD11 == xhash64(b'CENOURA')
assert 0x6B9111C11B1B6261 == xhash64(b'ABACATE')
assert 0xAF7EABC34406008F == xhash64(b'BETERRABA')
