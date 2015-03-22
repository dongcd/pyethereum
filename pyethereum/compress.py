from rlp.utils import decode_hex, encode_hex, ascii_chr


NULLSHA3 = decode_hex('c5d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a470')


def compress(data):
    o = ''
    i = 0
    while i < len(data):
        if data[i] == '\xfe':
            o += '\xfe\x00'
        elif data[i:i + 32] == NULLSHA3:
            o += '\xfe\x01'
            i += 31
        elif data[i:i + 2] == '\x00\x00':
            p = 2
            while p < 255 and i + p < len(data) and data[i + p] == '\x00':
                p += 1
            o += '\xfe' + ascii_chr(p)
            i += p - 1
        else:
            o += data[i]
        i += 1
    return o


def decompress(data):
    from pyethereum.utils import safe_ord
    o = ''
    i = 0
    while i < len(data):
        if data[i] == '\xfe':
            if i == len(data) - 1:
                raise Exception("Invalid encoding, \\xfe at end")
            elif data[i + 1] == '\x00':
                o += '\xfe'
            elif data[i + 1] == '\x01':
                o += NULLSHA3
            else:
                o += '\x00' * safe_ord(data[i + 1])
            i += 1
        else:
            o += data[i]
        i += 1
    return o
