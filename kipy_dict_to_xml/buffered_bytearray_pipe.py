def buffered_bytearray_pipe(data_generator, buffer_size=8 * 1024):
    buffer = bytearray(buffer_size)
    p = 0

    for d in data_generator:
        b = bytes(d, "utf-8")
        l = len(b)

        if l == 0:
            pass
        elif p + l <= buffer_size:
            buffer[p:p+l] = b
            p = p + l
        else:
            chunk_size = buffer_size - p  # Remaining Length
            buffer[p:buffer_size] = b[0:chunk_size]
            ix = chunk_size
            while True:
                yield buffer
                buffer = bytearray(buffer_size)
                chunk_size = min(buffer_size, l - ix)
                buffer[0:chunk_size] = b[ix:ix+chunk_size]
                ix = ix + chunk_size
                p = chunk_size
                if ix >= l:
                    break
    if p > 0:
        yield buffer[0:p]

