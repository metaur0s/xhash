
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
void __attribute__((optimize("-O3", "-ffast-math", "-fstrict-aliasing"))) xhash (const void* restrict data, uint size, u64 hash[9]) {

    // SIZE DEPENDENT
    register u64 A = 0b0101010101010101010101010101010101010101010101010101010101010101ULL * size; // 01
    register u64 B = 0b1101000010111110011100001111010001110101000000111001110000100110ULL * size;
    register u64 C = 0b0000101000101000010010010100110100000100011100001111101111001111ULL * size;
    register u64 D = 0b0010001001101001111001001000110010100111011101111010011110011000ULL * size;
    register u64 E = 0b1010101010101010101010101010101010101010101010101010101010101010ULL * size; // 10
    register u64 F = 0b1110011010010111111010110000011100010101000111111010000101100010ULL * size;
    register u64 G = 0b0111111011010110110100101100010001000101110110011111010111110110ULL * size;
    register u64 H = 0b0100011111011111100111001000111000011010001101011111000110111010ULL * size;

    register u64 x = 0b0110011010101000100111001101110111100010011000101101101010001101ULL * size;

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
        A += E += x += G += C += x * popcount64(x);
        F += H += x += D += B += x * popcount64(x);

        // ACCUMULATE AND MIX ALL
        H += G ^= F += E ^= x += D ^= C += B ^= A += swap64(x);
        A += B ^= C += D ^= x += E ^= F += G ^= H += swap64(x);

        // POSITION DEPENDENT
        x = swap64(x + size);
    }

    // ALL WORDS CONTAIN THE INFO
    A += B += C += D += E += F += G += H +=
        swap64(swap64(swap64(swap64(swap64(swap64(swap64(x + H) + G) + F) + E) + D) + C) + B) + A;

    // SAVE
    hash[0] = BE64(A); hash[1] = BE64(B);
    hash[2] = BE64(C); hash[3] = BE64(D);
    hash[4] = BE64(E); hash[5] = BE64(F);
    hash[6] = BE64(G); hash[7] = BE64(H);
    hash[8] = BE64(x);
}

// FOR SMALL THINGS
void __attribute__((optimize("-O3", "-ffast-math", "-fstrict-aliasing"))) xcsum (const void* restrict data, uint size, u64 sum[8]) {

    register u64 A = 0b0101010101010101010101010101010101010101010101010101010101010101ULL; // 01
    register u64 B = 0b1101000010111110011100001111010001110101000000111001110000100110ULL;
    register u64 C = 0b0000101000101000010010010100110100000100011100001111101111001111ULL;
    register u64 D = 0b0010001001101001111001001000110010100111011101111010011110011000ULL;
    register u64 E = 0b1010101010101010101010101010101010101010101010101010101010101010ULL; // 10
    register u64 F = 0b1110011010010111111010110000011100010101000111111010000101100010ULL;
    register u64 G = 0b0111111011010110110100101100010001000101110110011111010111110110ULL;
    register u64 H = 0b0100011111011111100111001000111000011010001101011111000110111010ULL;

    while (size) {

        register u64 x;

        if (size >= sizeof(u64)) {
            size -= sizeof(u64);
            x = BE64(*(u64*)data);
            data += sizeof(u64);
        } else {
            size -= sizeof(u8);
            x = BE8(*(u8*)data);
            data += sizeof(u8);
        }

        // ACCUMULATE ALL
        A += B ^= C += D ^= x += E ^= F += G ^= H += x * popcount64(x);
    }

    // ALL WORDS CONTAIN THE INFO
    A += B += C += D += E += F += G += H +=
        ((((((H + G) * F) + E) * D) + C) * B) + A;

    // SAVE
    sum[0] = BE64(A); sum[1] = BE64(B);
    sum[2] = BE64(C); sum[3] = BE64(D);
    sum[4] = BE64(E); sum[5] = BE64(F);
    sum[6] = BE64(G); sum[7] = BE64(H);
}
