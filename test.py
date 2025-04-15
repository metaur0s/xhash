#!/usr/bin/python

import time
import cffi
import xstreamlib

from xstream import xcsum, xhash, xhash_64, xhash_128

#
TEST_BUFF_SIZE = 256*1024*1024

# SAMPLE DATA
sample = open('/dev/urandom', 'rb').read(TEST_BUFF_SIZE)

#
print('xcsum()     = ', xcsum(sample))
print('xhash_64()  = 0x%016X' % xhash_64(sample))
print('xhash_128() = 0x%032X' % xhash_128(sample))
print('xhash()     = ', xhash(sample))

# BENCHMARK

# HASH OF THE SAMPLE DATA
shash = cffi.FFI().new('unsigned char [72]')

for FUNC, func in (
    ('XHASH', xstreamlib.lib.xhash),
    ('XCSUM', xstreamlib.lib.xcsum),
):

    print(f'----- {FUNC}')

    for size, rounds in (
        ( 64,          5000000),
        (128,          5000000),
        (256,          5000000),
        (1024,         4000000),
        (65536,         120000),
        (256*1024,       50000),
        (64*1024*1024,     200),
        (128*1024*1024,    100),
    ):

        assert size <= TEST_BUFF_SIZE

        t = time.time()

        for _ in range (rounds):
            func(sample, size, shash)
            #return bytes(shash)
            # xstreamlib.lib.xhash(v, len(v), _hash)

        t = time.time() - t

        ms = int(t * 1000)

        print('SIZE %9d ROUNDS %8d MS %5d MB/S %5d' %
            (size, rounds, ms, (size * rounds) / (t * 1024 * 1024)))

    print()
