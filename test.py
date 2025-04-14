#!/usr/bin/python

import time

from hashlib import sha1, sha256, sha512, blake2b
from xxhash import xxh64_intdigest, xxh128_intdigest
from xhash import xhash64, xhash128, xhash256

# BENCHMARK

TEST_ROUNDS = 65536
TEST_SIZE = 262144

sample = open('/dev/urandom', 'rb').read(TEST_SIZE)

t = time.time() ; sum(( 0 * xhash64(sample)               for _ in range (TEST_ROUNDS) )) ; print('XHASH64',  time.time() - t)
t = time.time() ; sum(( 0 * len(xhash256(sample))         for _ in range (TEST_ROUNDS) )) ; print('XHASH256', time.time() - t)
t = time.time() ; sum(( 0 * len(xhash128(sample))         for _ in range (TEST_ROUNDS) )) ; print('XHASH128', time.time() - t)
t = time.time() ; sum(( 0 * xxh64_intdigest(sample)       for _ in range (TEST_ROUNDS) )) ; print('XXH64',    time.time() - t)
t = time.time() ; sum(( 0 * xxh128_intdigest(sample)      for _ in range (TEST_ROUNDS) )) ; print('XXH128',   time.time() - t)
t = time.time() ; sum(( 0 * len(sha1(sample).digest())    for _ in range (TEST_ROUNDS) )) ; print('SHA1',     time.time() - t)
t = time.time() ; sum(( 0 * len(sha256(sample).digest())  for _ in range (TEST_ROUNDS) )) ; print('SHA256',   time.time() - t)
t = time.time() ; sum(( 0 * len(sha512(sample).digest())  for _ in range (TEST_ROUNDS) )) ; print('SHA512',   time.time() - t)
t = time.time() ; sum(( 0 * len(blake2b(sample).digest()) for _ in range (TEST_ROUNDS) )) ; print('BLAKE2B',  time.time() - t)
