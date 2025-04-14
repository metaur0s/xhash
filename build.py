#!/usr/bin

import os

from cffi import FFI

#
for f in ('xhashlib.c', 'xhashlib.o', 'xhashlib.so'):
    try:
        os.unlink(f)
    except FileNotFoundError:
        pass

ffi = FFI()

ffi.set_source("xhashlib", open('xhash.c').read(), libraries=[],
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

ffi.cdef('unsigned short xhash16 (const void* restrict, const unsigned int);')
ffi.cdef('unsigned long long xhash64 (const void* restrict, const unsigned int);')
ffi.cdef('void xhash128 (const void* restrict, const unsigned int, void* const restrict);')
ffi.cdef('void xhash256 (const void* restrict, const unsigned int, void* const restrict);')

ffi.compile(target=('xhashlib.so'))

#
for f in ('xhashlib.c', 'xhashlib.o'):
    try:
        os.unlink(f)
    except FileNotFoundError:
        pass

# VERIFY
assert 64 <= os.stat('xhashlib.so').st_size
