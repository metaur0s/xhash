#!/usr/bin

import os

from cffi import FFI

#
for f in ('xhash.c', 'xhash.o', 'xhash.so'):
    try:
        os.unlink(f)
    except FileNotFoundError:
        pass

ffi = FFI()

ffi.set_source("xhash", open('xhash-src.c').read(), libraries=[],
    extra_compile_args=[
        "-std=gnu11",
        "-Wall",
        "-Wextra",
        "-Werror",
        "-Wfatal-errors",
        "-O2",
        "-march=native",
      # "-fstrict-aliasing"
    ]
)

ffi.cdef('unsigned long long xhash64 (const void* restrict, const unsigned int);')
ffi.cdef('void xhash128 (const void* restrict, const unsigned int, void* const restrict);')
ffi.cdef('void xhash256 (const void* restrict, const unsigned int, void* const restrict);')

ffi.compile(target=('xhash.so'))

#
for f in ('xhash.c', 'xhash.o'):
    try:
        os.unlink(f)
    except FileNotFoundError:
        pass

# VERIFY
assert 64 <= os.stat('xhash.so').st_size
