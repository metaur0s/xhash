
#include <stdint.h>

typedef unsigned int uint;

typedef uint8_t   u8;
typedef uint32_t u32;
typedef uint16_t u16;
typedef uint64_t u64;

#define popcount64 __builtin_popcountll

// TODO:
#if 1
#define BE64 __builtin_bswap64
#else
#define BE64
#endif
#define BE8

static inline u64 swap64q (const u64 x, const uint q) {

    return (x >> q) | (x << (64 - q));
}

static inline u64 swap64 (const u64 x) {

    return swap64q(x, popcount64(x));
}

void xhash (const void* restrict data, uint size, u64 hash[2]) {

    u64 A = 0x5F62C0DECB051668ULL, B = 0xD0BE70F475039C26ULL, C = 0x0A28494D0470FBCFULL, D = 0x2269E48CA777A798ULL,
        E = 0x0C6771D8D076FAEDULL, F = 0xE697EB07151FA162ULL, G = 0x7ED6D2C445D9F5F6ULL, H = 0x47DF9C8E1A35F1BAULL;

    u64 x = size;

    while (size) {

        if (size >= sizeof(u64)) {
            size -= sizeof(u64);
            x += BE64(*(u64*)data);
            data += sizeof(u64);
        } else {
            size -= sizeof(u8);
            x += BE8(*(u8*)data);
            data += sizeof(u8);
        }

        //
        x = swap64((swap64((swap64((swap64((x + A) ^ B) + C) ^ D) + E) ^ F) + G) ^ H);

        // ACCUMULATE AND MIX ALL
        A += (x += H) * C;
        B += (x += G) * D;
        C += (x += F) * E;
        D += (x += E) * F;
        E += (x += D) * G;
        F += (x += C) * H;
        G += (x += B) * A;
        H += (x += A) * B;

        // PARANOIA
        x *= size;
    }

    hash[0] = ((((((A + B) * C) + D) * E) + F) * G) + H;
    hash[1] = ((((((H + F) * D) + B) * A) + C) * E) + G;
}

// FOR SMALL THINGS
u64 xcsum (const void* restrict data, uint size, u64 x) {

    u64 A = 0x5F62C0DECB051668ULL, B = 0xD0BE70F475039C26ULL,
        C = 0x0C6771D8D076FAEDULL, D = 0xE697EB07151FA162ULL;

    while (size) {

        if (size >= sizeof(u64)) {
            size -= sizeof(u64);
            x += BE64(*(u64*)data);
            data += sizeof(u64);
        } else {
            size -= sizeof(u8);
            x += BE8(*(u8*)data);
            data += sizeof(u8);
        }

        // ACCUMULATE AND MIX ALL
        A += B += (x += D) * C;
        C += D += (x += B) * A;

        //
        x += x * size;
    }

    return x;
}
