"""MD5 implementation không dùng thư viện"""
import struct

# MD5 constants
s = [7,12,17,22]*4 + [5,9,14,20]*4 + [4,11,16,23]*4 + [6,10,15,21]*4
K = [int(abs(__import__('math').sin(i+1)) * 2**32) & 0xFFFFFFFF for i in range(64)]

def left_rotate(x, c):
    return ((x << c) | (x >> (32-c))) & 0xFFFFFFFF


def md5(message):
    msg = message.encode() if isinstance(message, str) else message
    orig_len_bits = (8 * len(msg)) & 0xFFFFFFFFFFFFFFFF
    msg += b'\x80'
    while (len(msg) % 64) != 56:
        msg += b'\x00'
    msg += struct.pack('<Q', orig_len_bits)

    a0 = 0x67452301
    b0 = 0xEFCDAB89
    c0 = 0x98BADCFE
    d0 = 0x10325476

    for chunk_offset in range(0, len(msg), 64):
        A, B, C, D = a0, b0, c0, d0
        chunk = msg[chunk_offset:chunk_offset+64]
        M = struct.unpack('<16I', chunk)

        for i in range(64):
            if 0 <= i <= 15:
                F = (B & C) | (~B & D)
                g = i
            elif 16 <= i <= 31:
                F = (D & B) | (~D & C)
                g = (5*i + 1) % 16
            elif 32 <= i <= 47:
                F = B ^ C ^ D
                g = (3*i + 5) % 16
            elif 48 <= i <= 63:
                F = C ^ (B | ~D)
                g = (7*i) % 16

            F = (F + A + K[i] + M[g]) & 0xFFFFFFFF
            A, D, C, B = D, C, B, (B + left_rotate(F, s[i])) & 0xFFFFFFFF

        a0 = (a0 + A) & 0xFFFFFFFF
        b0 = (b0 + B) & 0xFFFFFFFF
        c0 = (c0 + C) & 0xFFFFFFFF
        d0 = (d0 + D) & 0xFFFFFFFF

    return ''.join(format(x, '02x') for x in struct.pack('<4I', a0, b0, c0, d0))

if __name__ == '__main__':
    samples = ['','abc','The quick brown fox jumps over the lazy dog']
    for s in samples:
        print(f"MD5('{s}') = {md5(s)}")
