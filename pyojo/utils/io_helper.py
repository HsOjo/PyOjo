import struct

from pyojo import common


def read_all(io, default=None):
    if io is not None:
        io.seek(0)
        content = io.read()
        io.seek(0, 2)
    else:
        content = default
    return content


def read_range(io, offset=0, size=-1):
    io.seek(offset)
    return io.read(size)


def read_ascii_string(io, max_size=-1, ignore_zero=False):
    result = ''
    zero_break = not ignore_zero and max_size != -1

    while max_size == -1 or len(result) < max_size:
        [char] = read_struct(io, 'B')
        if char == 0 and zero_break:
            break

        result += chr(char)
    return result


def read_struct(io, fmt, zfill=True):
    struct_size = struct.calcsize(fmt)
    data = io.read(struct_size)

    if zfill:
        data = common.zfill_bytes(data, struct_size)
    elif len(data) == 0:
        return None

    result = struct.unpack(fmt, data)
    return result


def write_ascii_string(io, content: str):
    data = content.encode('ascii') + b'\x00'
    return io.write(data)


def write_struct(io, fmt, *values):
    data = struct.pack(fmt, *values)
    return io.write(data)
