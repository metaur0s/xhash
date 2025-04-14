#!/usr/bin/python

import time
import cffi
import xstreamlib

from xstream import xcsum, xhash

#
TEST_BUFF_SIZE = 262144

# SAMPLE DATA
sample = open('/dev/urandom', 'rb').read(TEST_BUFF_SIZE)

#
print(xcsum(sample))
print(xhash(sample))

# BENCHMARK

# HASH OF THE SAMPLE DATA
shash = cffi.FFI().new('unsigned char [16]')

for func in (
    xstreamlib.lib.xcsum,
    xstreamlib.lib.xhash,
):

    for size, rounds in (
        (128,          1000),
        (256,          1000),
        (1024,         1000),
        (65536,        10),
        (256*1024,     10),
        (64*1024*1024, 10),
    ):

        t = time.time()

        for _ in range (rounds):
            func(sample, size, shash)
            #return bytes(shash)

        t = time.time() - t

        print(f'{func} SIZE {size} ROUNDS {rounds} TOOK {t} SECONDS')
