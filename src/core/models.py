import struct
from dataclasses import dataclass

# ! = network byte order (big-endian)
# I = unsigned 32-bit int (instrument_token, 4 bytes)
# d = 64-bit double float (timestamp epoch, 8 bytes)
# d = 64-bit double float (ltp, 8 bytes)
# Q = unsigned 64-bit int (volume, 8 bytes)
TICK_STRUCT = struct.Struct("!IddQ")
#reusable_buffer = bytearray(28)


@dataclass(slots=True)
class Tick:
    instrument_token: int
    timestamp: float
    ltp: float
    volume: int

    def to_bytes(self) -> bytes:
        return (TICK_STRUCT
                .pack(self.instrument_token, self.timestamp, self.ltp, self.volume)
                )

        TICK_STRUCT.pack_into(
            reusable_buffer,
            0,
            self.instrument_token,
            self.timestamp,
            self.ltp,
            self.volume,
        )

        return reusable_buffer

    @classmethod
    def from_bytes(cls, raw: bytes):
        token, ts, ltp, vol = TICK_STRUCT.unpack(raw)
        return cls(token, ts, ltp, vol)
