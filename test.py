#!/usr/bin/python

import time
import cffi
import xstreamlib

from xstream import xcsum, xhash

#
TEST_BUFF_SIZE = 256*1024*1024

# SAMPLE DATA
sample = open('/dev/urandom', 'rb').read(TEST_BUFF_SIZE)

#
print('xcsum() = 0x%016X' % xcsum(sample))
print('xhash() = ', xhash(sample))

# BENCHMARK

# HASH OF THE SAMPLE DATA
shash = cffi.FFI().new('unsigned char [16]')

for FUNC, func, arg in (
    ('XHASH', xstreamlib.lib.xhash, shash),
    ('XCSUM', xstreamlib.lib.xcsum, 0),
):

    print(f'----- {FUNC}')

    for size, rounds in (
        ( 64,          5000000),
        (128,          5000000),
        (256,          3500000),
        (1024,         1000000),
        (65536,          20000),
        (256*1024,        8000),
        (64*1024*1024,     100),
        (128*1024*1024,     10),
    ):

        assert size <= TEST_BUFF_SIZE

        t = time.time()

        for _ in range (rounds):
            func(sample, size, arg)
            #return bytes(shash)
            # xstreamlib.lib.xhash(v, len(v), _hash)

        t = time.time() - t

        ms = int(t * 1000)

        print('SIZE %9d ROUNDS %8d MS %5d MB/S %5d' %
            (size, rounds, ms, (size * rounds) / (t * 1024 * 1024)))

    print()
