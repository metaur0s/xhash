#!/usr/bin/python

import time
import xxhash
import hashlib
import binascii

import cffi
import xhash

coisa = b'''
Etiam sodales finibus leo, convallis lobortis eros auctor non. Quisque mattis purus vel quam sodales, eu vulputate libero sodales. Aenean pulvinar ipsum magna. Nunc fringilla justo a nulla pretium sagittis. Quisque ornare felis ex, a dignissim ligula ultrices quis. Sed mi sem, viverra nec lectus ut, sodales interdum elit. Suspendisse ac justo accumsan, accumsan arcu sed, ultrices arcu. Pellentesque semper tincidunt lacus, quis commodo enim auctor sit amet.
'''

xhash64  = xhash.lib.xhash64

# NOTE: SINGLE THREAD ONLY
_xhash_buff128 = cffi.FFI().new('unsigned char [16]')
_xhash_buff256 = cffi.FFI().new('unsigned char [32]')

def xhash128 (v):
    xhash.lib.xhash128(v, len(v), _xhash_buff128)
    return bytes(_xhash_buff128)

def xhash256 (v):
    xhash.lib.xhash256(v, len(v), _xhash_buff256)
    return bytes(_xhash_buff256)

if False:
    # DEVELOPMENT

    # GENERATE TEST
    print(['0x%016X' % xhash64(coisa, 4 + i) for i in range(100) ])

    # SHOW A SAMPLE
    for i in range(16):
        print(i, '0x%016X' % xhash64(b'0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ', 3 + i))
        print(i, '0x%016X' % xhash64(b'0123556789ABCDEFGHIJKLMNOPQRSTUVWXYZ', 3 + i))

    for i in range(16):
        print(i, binascii.hexlify(xhash128(b'0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'[:3 + i]), sep=' ', bytes_per_sep=8).upper().decode())
        print(i, binascii.hexlify(xhash128(b'0123556789ABCDEFGHIJKLMNOPQRSTUVWXYZ'[:3 + i]), sep=' ', bytes_per_sep=8).upper().decode())

else:
    # PRODUCTION

    #
    assert xhash64(b'', 0) == 0

    # TEST
    assert ['0x%016X' % xhash64(coisa, 4 + i) for i in range(100) ] ==  [
        '0x9A88E86B32DF9EF4', '0x65805E9044E471B7', '0xA674BE077005F2DA', '0xD1037A2ACDC58A52', '0x43B7DF1473167B1E', '0x5267B7AD1D8DE0E0', '0x7D84091799788558', '0xA3934AFE902C064C', '0x92F1369171986638', '0x570C0F24CCA607C3', '0x56E25D1E9BCFB849', '0x0FBB48F976B592A6',
        '0x4B90FC0F3548AEA6', '0x769E2F01501C397F', '0x79B8BB5400DD5325', '0xB7F6A72BB02FF034', '0xA2AFFCB9860554B6', '0x8355768FE20FFBD4', '0x2055822DEEECEC6A', '0x8583A366BEFF9A9E', '0x4C2983F3E09EA8F3', '0xC6A7E6DF3EF4C7AD', '0xE0B62ACDFADC1FAE', '0x2A471502C6C094F8',
        '0x9763A5C13911721A', '0x7820A56F805E7E1D', '0xB00F616A1620226A', '0x1AC0EC2005F2AD4B', '0xFB02592BDC6A31BB', '0x804ED3094E983922', '0x640771B3618675E1', '0xBA28846D15E2B060', '0x4C312C5EDB9E8A20', '0x292820543B22B4AE', '0xD00F5EE92AFFCABA', '0x0797F49ED317FF2C',
        '0x5A566116A4EA6DBD', '0x64A281F4F1F47218', '0x31A1C6EC423DFC26', '0x664CEB6DA0CD6D0C', '0xDC6A92FA35276D09', '0x3D5ACD8A9E3FEA8A', '0x70AB2A6D3ED3AFF8', '0x776A7A0DD06A337E', '0x5986E28E2CEDCAA1', '0x3763C42007680F83', '0xDF07C57618E88BB9', '0x51E64082E2C85803',
        '0x14186A4CDDB31224', '0x487A6AA0B8CD29D1', '0x61887515A803D1EF', '0xACEC2FAB77ABCEE6', '0xFF87D3EE85D84C44', '0xCA94F8D7BDCCC00E', '0xDE77970A2AB3FD98', '0x2EF10C5E825B2197', '0xA362C78AEF69D84F', '0x5827B0082C350945', '0x30AE5F628FBDE90C', '0x8EBAC8EBF336F550',
        '0xC5B4E672F28B6A0F', '0x929415A916614194', '0xA26CF26FC9C489CF', '0xF1B35090540EAD3E', '0x9D9A1B87F68C1EFF', '0x6AF30B4BA57219A1', '0x4A8E9126A7E97D9D', '0x6DB4D9BCF421EB93', '0xAFED1C3797A25353', '0xE3AD52B8DAA752B6', '0x626D1E9FCD8DEA24', '0x55CE75CEB83F3C9D',
        '0x0A91317C68C04A3E', '0x7560BFA8376DC4C0', '0xC842BDABD7DD6670', '0xFAD11EBAF9660867', '0x73A6126972F500CD', '0x7958812C34AE8726', '0xD93948CC50B7EFD9', '0x9D0C9E09372ADD0A', '0xBC2A6BEB1473DEC1', '0xE4B7020D8A92271A', '0x906B11635CAF9F0B', '0xD16B5E3F4CB0809D',
        '0x4655B5C70857E7D9', '0xDD5A6500CA6F9D70', '0x97F9F9D2A65F7DD8', '0xA45BA99F8C081446', '0x96A6C75D63532ADB', '0xBE0808E4AE1C038D', '0x687302BFA39FA074', '0xE1763384EE2DD145', '0xFD9F0C992C252A5A', '0x37C22647E0646A08', '0x49B217AD13FD5022', '0x4F6DDE28BC22E750',
        '0xB8EFA85EB49C0713', '0x4E66A3844AF2426B', '0x6D221A488055A773', '0x88BD0411319C2E23'
    ]

TEST_ROUNDS = 65536
TEST_SIZE = 262144

sample = open('/dev/urandom', 'rb').read(TEST_SIZE)

t = time.time() ; sum(( 0 * xhash64(sample,len(sample))           for _ in range (TEST_ROUNDS) )) ; print('XHASH64',  time.time() - t)
t = time.time() ; sum(( 0 * len(xhash256(sample))                 for _ in range (TEST_ROUNDS) )) ; print('XHASH256', time.time() - t)
t = time.time() ; sum(( 0 * len(xhash128(sample))                 for _ in range (TEST_ROUNDS) )) ; print('XHASH128', time.time() - t)
t = time.time() ; sum(( 0 * xxhash.xxh64_intdigest(sample)        for _ in range (TEST_ROUNDS) )) ; print('XXH64',    time.time() - t)
t = time.time() ; sum(( 0 * xxhash.xxh128_intdigest(sample)       for _ in range (TEST_ROUNDS) )) ; print('XXH128',   time.time() - t)
t = time.time() ; sum(( 0 * len(hashlib.sha1(sample).digest())    for _ in range (TEST_ROUNDS) )) ; print('SHA1',     time.time() - t)
t = time.time() ; sum(( 0 * len(hashlib.sha256(sample).digest())  for _ in range (TEST_ROUNDS) )) ; print('SHA256',   time.time() - t)
t = time.time() ; sum(( 0 * len(hashlib.sha512(sample).digest())  for _ in range (TEST_ROUNDS) )) ; print('SHA512',   time.time() - t)
t = time.time() ; sum(( 0 * len(hashlib.blake2b(sample).digest()) for _ in range (TEST_ROUNDS) )) ; print('BLAKE2B',  time.time() - t)
