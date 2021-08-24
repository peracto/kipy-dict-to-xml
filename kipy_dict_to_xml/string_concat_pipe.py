def string_concat_pipe(data_generator, buffer_size=8 * 1024):
    c = []
    p = 0
    for d in data_generator:
        if len(d) == 0:
            continue

        p = p + len(d)
        if p < buffer_size:
            c.append(d)
        else:
            if len(c) > 0:
                yield ''.join(c)
            if len(d) >= buffer_size:
                yield d
                c = []
            else:
                c = [d]

    if len(c) > 0:
        yield ''.join(c)


def string_concat_byte_pipe(data_generator, buffer_size=8 * 1024):
    c = []
    p = 0
    for d in data_generator:
        if len(d) == 0:
            continue

        p = p + len(d)

        if p < buffer_size:
            c.append(d)
            continue

        if len(c) > 0:
            yield bytes(''.join(c), 'utf-8')

        if len(d) >= buffer_size:
            yield bytes(d, 'utf-8')
            c = []
        else:
            c = [d]

    if len(c) > 0:
        yield bytes(''.join(c), 'utf-8')
