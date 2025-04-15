
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

// NOTE: THE HASH IS SAVED BIG ENDIAN
void xhash (const void* restrict data, uint size, u64 hash[2]) {

    // SIZE DEPENDENT
    u64 A = 0b0101010101010101010101010101010101010101010101010101010101010101ULL * size, // 01
        B = 0b1101000010111110011100001111010001110101000000111001110000100110ULL * size,
        C = 0b0000101000101000010010010100110100000100011100001111101111001111ULL * size,
        D = 0b0010001001101001111001001000110010100111011101111010011110011000ULL * size,
        E = 0b1010101010101010101010101010101010101010101010101010101010101010ULL * size, // 10
        F = 0b1110011010010111111010110000011100010101000111111010000101100010ULL * size,
        G = 0b0111111011010110110100101100010001000101110110011111010111110110ULL * size,
        H = 0b0100011111011111100111001000111000011010001101011111000110111010ULL * size,
        x = 0b0110011010101000100111001101110111100010011000101101101010001101ULL * size;

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

        // VALUE DEPENDENT
        x += x * popcount64(x);

        // ACCUMULATE AND MIX ALL
        H += G ^= F += E ^= x += D ^= C += B ^= A += x;
        F += H ^= D += B ^= x += A ^= E += G ^= C += x;
        A += B ^= C += D ^= x += E ^= F += G ^= H += x;

        // POSITION DEPENDENT
        x += x * size;
    }

    // DIFFERENT WAYS OF SEEING OUR WORDS
    hash[0] = BE64((((((((x * B) + D) * F) + H) * A) + C) * E) + G);
    hash[1] = BE64((((((((x * G) + E) * C) + A) * H) + F) * D) + B);
}

// FOR SMALL THINGS
// NOTE: AQUI O ENDIANESS É LOCAL
// NOTE: NAO USA STACK
u64 xcsum (const void* restrict data, uint size) {

    u64 A = 0b0101010101010101010101010101010101010101010101010101010101010101ULL, // 01
        B = 0b1101000010111110011100001111010001110101000000111001110000100110ULL,
        C = 0b1010101010101010101010101010101010101010101010101010101010101010ULL, // 10
        D = 0b1110011010010111111010110000011100010101000111111010000101100010ULL;

    while (size) {

        u64 x;

        if (size >= sizeof(u64)) {
            size -= sizeof(u64);
            x = BE64(*(u64*)data);
            data += sizeof(u64);
        } else {
            size -= sizeof(u8);
            x = BE8(*(u8*)data);
            data += sizeof(u8);
        }

        // ACCUMULATE ALL, POSITION DEPENDENT
        A += B ^= x += C ^= D += x * size;
    }

    //
    return ((A + C) * B) + D;
}
