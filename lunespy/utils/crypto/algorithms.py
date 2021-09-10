class KeccakState(object):
    W = 5
    H = 5

    rangeW = range(W)
    rangeH = range(H)

    @staticmethod
    def zero():
        return [[0] * KeccakState.W for x in KeccakState.rangeH]

    @staticmethod
    def format(st):
        rows = []

        def fmt(x):
            return '%016x' % x

        for y in KeccakState.rangeH:
            row = []
            for x in rangeW:
                row.append(fmt(st[x][y]))
            rows.append(' '.join(row))
        return '\n'.join(rows)

    @staticmethod
    def lane2bytes(s, w):
        o = []
        for b in range(0, w, 8):
            o.append((s >> b) & 0xff)
        return o

    @staticmethod
    def bytes2lane(bb):
        r = 0
        for b in reversed(bb):
            r = r << 8 | b
        return r

    def __init__(self, bitrate, b):
        from lunespy.utils.crypto.converters import bits_to_bytes

        self.bitrate = bitrate
        self.b = b

        # only byte-aligned
        assert self.bitrate % 8 == 0
        self.bitrate_bytes = bits_to_bytes(self.bitrate)

        assert self.b % 25 == 0
        self.lanew = self.b // 25

        self.s = KeccakState.zero()

    def __str__(self):
        return KeccakState.format(self.s)

    def absorb(self, bb):
        from lunespy.utils.crypto.converters import bits_to_bytes

        assert len(bb) == self.bitrate_bytes

        bb += [0] * int(bits_to_bytes(self.b - self.bitrate))
        i = 0

        for y in self.rangeH:
            for x in self.rangeW:
                self.s[x][y] ^= KeccakState.bytes2lane(bb[i:i + 8])
                i += 8

    def squeeze(self):
        return self.get_bytes()[:self.bitrate_bytes]

    def get_bytes(self):
        from lunespy.utils.crypto.converters import bits_to_bytes

        out = [0] * int(bits_to_bytes(self.b))
        i = 0
        for y in self.rangeH:
            for x in self.rangeW:
                v = KeccakState.lane2bytes(self.s[x][y], self.lanew)
                out[i:i + 8] = v
                i += 8
        return out

    def set_bytes(self, bb):
        i = 0
        for y in self.rangeH:
            for x in self.rangeW:
                self.s[x][y] = KeccakState.bytes2lane(bb[i:i + 8])
                i += 8


class KeccakSponge(object):
    def __init__(self, bitrate, width, padfn, permfn):
        self.state = KeccakState(bitrate, width)
        self.padfn = padfn
        self.permfn = permfn
        self.buffer = []

    def copy(self):
        from copy import deepcopy
        
        return deepcopy(self)

    def absorb_block(self, bb):
        self.state.bitrate_bytes = int(self.state.bitrate_bytes)
        assert len(bb) == self.state.bitrate_bytes
        self.state.absorb(bb)
        self.permfn(self.state)

    def absorb(self, s):
        from lunespy.utils.crypto.converters import string_to_list

        self.buffer = string_to_list(s)

        while len(self.buffer) >= self.state.bitrate_bytes:
            self.absorb_block(self.buffer[:self.state.bitrate_bytes])
            self.buffer = self.buffer[self.state.bitrate_bytes:]

    def absorb_final(self):
        padded = self.buffer + self.padfn(len(self.buffer), self.state.bitrate_bytes)
        self.absorb_block(padded)
        self.buffer = []

    def squeeze_once(self):
        rc = self.state.squeeze()
        self.permfn(self.state)
        return rc

    def squeeze(self, l):
        Z = self.squeeze_once()
        while len(Z) < l:
            Z += self.squeeze_once()
        return Z[:int(l)]


class KeccakHash(object):
    def __init__(self):
        from lunespy.utils.crypto.converters import bits_to_bytes
        from lunespy.utils.crypto.converters import keccak_f
        from lunespy.utils.crypto.converters import multirate_padding

        bitrate_bits = 1088
        capacity_bits = 512
        output_bits = 256
        self.sponge = KeccakSponge(
            bitrate_bits,
            bitrate_bits + capacity_bits,
            multirate_padding,
            keccak_f)
        self.digest_size = bits_to_bytes(output_bits)
        self.block_size = bits_to_bytes(bitrate_bits)

    def __repr__(self):
        info = (
            self.sponge.state.bitrate,
            self.sponge.state.b - self.sponge.state.bitrate,
            self.digest_size * 8
        )
        return "<KeccakHash with r=%d, c=%d, image=%d>" % info

    def digest(self, string: str) -> str:
        self.sponge.absorb(string)
        finalised = self.sponge.copy()
        finalised.absorb_final()
        digest = finalised.squeeze(self.digest_size)
        return ''.join(map(chr, digest))


