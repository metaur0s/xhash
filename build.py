#!/usr/bin

import os

from cffi import FFI

#
for f in ('xstreamlib.c', 'xstreamlib.o', 'xstreamlib.so'):
    try:
        os.unlink(f)
    except FileNotFoundError:
        pass

ffi = FFI()

ffi.set_source("xstreamlib", open('xstream.c').read(), libraries=[],
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

ffi.cdef('unsigned long long xcsum (const void* restrict, const unsigned int, unsigned long long);')
ffi.cdef('void xhash (const void* restrict, const unsigned int, void* const restrict);')

ffi.compile(target=('xstreamlib.so'))

#
for f in ('xstreamlib.c', 'xstreamlib.o'):
    try:
        os.unlink(f)
    except FileNotFoundError:
        pass

# VERIFY
assert 64 <= os.stat('xstreamlib.so').st_size
